<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { colorizeBpmn, markEventSubprocesses } from '~/utils/bpmnPresentation'
import type { BpmnRegistry } from '~/utils/bpmnPresentation'

const props = defineProps<{ xmlUrl: string; selectedId: string | null; numbers: Record<string, string>; changes?: Record<string, 'agregado' | 'modificado'>; refreshToken?: number }>()
const emit = defineEmits<{ select: [id: string]; error: [message: string] }>()
const host = ref<HTMLElement | null>(null)

type ViewBox = { x: number; y: number; width: number; height: number }
type CanvasService = {
  zoom: (value?: number | 'fit-viewport', center?: { x: number; y: number }) => number
  viewbox: (box?: ViewBox) => ViewBox
  addMarker: (id: string, marker: string) => void
  removeMarker: (id: string, marker: string) => void
}
type EventBusService = { on: (name: string, handler: (event: { element?: { id: string; labelTarget?: { id: string } } }) => void) => void }
type Viewer = { importXML: (xml: string) => Promise<unknown>; get: (name: string) => unknown; destroy: () => void }

let viewer: Viewer | null = null
let currentMarker: string | null = null
let changeMarkers: [string, string][] = []

function canvas(): CanvasService | null {
  return viewer?.get('canvas') as CanvasService | null
}

// keepView: recarga por un cambio hecho por otro editor; conserva encuadre, zoom y selección.
async function load(keepView = false) {
  if (!viewer || !props.xmlUrl) return
  const view = keepView ? canvas()?.viewbox() : undefined
  try {
    const response = await fetch(props.xmlUrl, { cache: 'no-store' })
    if (!response.ok) throw new Error(`No se pudo cargar el BPMN (${response.status}).`)
    await viewer.importXML(colorizeBpmn(await response.text()))
    const registry = viewer.get('elementRegistry') as BpmnRegistry
    markEventSubprocesses(registry)
    markNumbers()
    if (view) canvas()?.viewbox({ x: view.x, y: view.y, width: view.width, height: view.height })
    else canvas()?.zoom('fit-viewport')
    currentMarker = null
    changeMarkers = []
    markChanges()
    highlight(props.selectedId)
  } catch (error) {
    emit('error', error instanceof Error ? error.message : 'No se pudo abrir el BPMN.')
  }
}

function markNumbers() {
  const registry = viewer?.get('elementRegistry') as BpmnRegistry | undefined
  if (!registry) return
  for (const [id, number] of Object.entries(props.numbers)) {
    const element = registry.get(id)
    if (!element) continue
    const visual = registry.getGraphics(element)?.querySelector('.djs-visual')
    if (!visual) continue
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text')
    text.setAttribute('x', '4')
    text.setAttribute('y', '12')
    text.setAttribute('fill', '#17365d')
    text.setAttribute('font-size', '11')
    text.setAttribute('font-weight', 'bold')
    text.setAttribute('pointer-events', 'none')
    text.setAttribute('data-numero-referencia', number)
    text.textContent = number
    visual.appendChild(text)
  }
}

// Cajas cambiadas en una versión (plan B): verde si se agregó, ámbar si se modificó.
function markChanges() {
  const service = canvas()
  if (!service) return
  for (const [id, marker] of changeMarkers) service.removeMarker(id, marker)
  changeMarkers = []
  const registry = viewer?.get('elementRegistry') as BpmnRegistry | undefined
  for (const [id, kind] of Object.entries(props.changes || {})) {
    if (!registry?.get(id)) continue
    const marker = kind === 'agregado' ? 'change-added' : 'change-modified'
    service.addMarker(id, marker)
    changeMarkers.push([id, marker])
  }
}

function highlight(id: string | null) {
  const service = canvas()
  if (!service) return
  if (currentMarker) service.removeMarker(currentMarker, 'selected-node')
  currentMarker = id
  if (id) service.addMarker(id, 'selected-node')
}

function zoom(factor: number, center?: { x: number; y: number }) {
  const service = canvas()
  if (!service) return
  service.zoom(Math.max(0.2, Math.min(4, service.zoom() * factor)), center)
}

function onWheel(event: WheelEvent) {
  if (!host.value || event.deltaY === 0) return
  event.preventDefault()
  event.stopImmediatePropagation()
  const bounds = host.value.getBoundingClientRect()
  zoom(event.deltaY < 0 ? 1.12 : 1 / 1.12, {
    x: event.clientX - bounds.left,
    y: event.clientY - bounds.top
  })
}

onMounted(async () => {
  if (!host.value) return
  const { default: NavigatedViewer } = await import('bpmn-js/lib/NavigatedViewer')
  viewer = new NavigatedViewer({ container: host.value }) as Viewer
  const eventBus = viewer.get('eventBus') as EventBusService
  eventBus.on('element.click', (event) => {
    const element = event.element?.labelTarget ?? event.element
    if (element) emit('select', element.id)
  })
  host.value.addEventListener('wheel', onWheel, { capture: true, passive: false })
  await load()
})

watch(() => props.xmlUrl, () => load())
watch(() => props.refreshToken, () => load(true))
watch(() => props.selectedId, highlight)
watch(() => props.changes, markChanges)

onBeforeUnmount(() => {
  host.value?.removeEventListener('wheel', onWheel, true)
  viewer?.destroy()
})
</script>

<template>
  <div class="diagram-surface">
    <div class="diagram-toolbar" aria-label="Controles del diagrama">
      <button type="button" title="Acercar" @click="zoom(1.2)">+</button>
      <button type="button" title="Alejar" @click="zoom(1 / 1.2)">−</button>
      <button type="button" title="Ajustar diagrama" @click="canvas()?.zoom('fit-viewport')">Ajustar</button>
    </div>
    <div ref="host" class="diagram-canvas" aria-label="Diagrama BPMN; arrastre para moverse y use la rueda para ampliar" />
  </div>
</template>
