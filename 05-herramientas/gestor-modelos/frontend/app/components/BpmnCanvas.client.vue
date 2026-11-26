<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { colorizeBpmn, markEventSubprocesses } from '~/utils/bpmnPresentation'
import type { BpmnRegistry } from '~/utils/bpmnPresentation'

const props = defineProps<{ xmlUrl: string; selectedId: string | null; numbers: Record<string, string>; changes?: Record<string, 'agregado' | 'modificado'>; refreshToken?: number; downloadName?: string; pins?: Record<string, Marcador> }>()
const emit = defineEmits<{ select: [id: string]; error: [message: string]; pin: [id: string] }>()
// Marcador de observaciones sobre una caja (rediseño 2026-11-26): cantidad, color del estado más urgente y resumen.
export type Marcador = { n: number; color: string; titulo: string }
const host = ref<HTMLElement | null>(null)

type ViewBox = { x: number; y: number; width: number; height: number }
type CanvasService = {
  zoom: (value?: number | 'fit-viewport', center?: { x: number; y: number }) => number
  viewbox: (box?: ViewBox) => ViewBox
  addMarker: (id: string, marker: string) => void
  removeMarker: (id: string, marker: string) => void
}
type OverlaysService = {
  add: (id: string, type: string, overlay: { position: { top?: number; right?: number }; html: HTMLElement }) => string
  remove: (filter: { type: string }) => void
}
type EventBusService = { on: (name: string, handler: (event: { element?: { id: string; labelTarget?: { id: string } } }) => void) => void }
type Viewer = { importXML: (xml: string) => Promise<unknown>; saveSVG: () => Promise<{ svg: string }>; get: (name: string) => unknown; destroy: () => void }

let viewer: Viewer | null = null
let currentMarker: string | null = null
let changeMarkers: [string, string][] = []
// XML tal como lo entregó el servidor (sin los colores de presentación), para descargarlo.
let originalXml = ''
const downloading = ref(false)

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
    originalXml = await response.text()
    await viewer.importXML(colorizeBpmn(originalXml))
    const registry = viewer.get('elementRegistry') as BpmnRegistry
    markEventSubprocesses(registry)
    markNumbers()
    if (view) canvas()?.viewbox({ x: view.x, y: view.y, width: view.width, height: view.height })
    else canvas()?.zoom('fit-viewport')
    currentMarker = null
    changeMarkers = []
    markChanges()
    markPins()
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

const mostrarMarcadores = ref(true)
function markPins() {
  const overlays = viewer?.get('overlays') as OverlaysService | undefined
  const registry = viewer?.get('elementRegistry') as BpmnRegistry | undefined
  if (!overlays || !registry) return
  overlays.remove({ type: 'observaciones' })
  if (!mostrarMarcadores.value) return
  for (const [id, marcador] of Object.entries(props.pins || {})) {
    if (!registry.get(id)) continue
    const boton = document.createElement('button')
    boton.type = 'button'
    boton.className = 'obs-pin'
    boton.style.background = marcador.color
    boton.textContent = String(marcador.n)
    boton.title = marcador.titulo
    boton.setAttribute('aria-label', `${marcador.n} observaciones: ${marcador.titulo}`)
    boton.addEventListener('click', (evento) => { evento.stopPropagation(); emit('pin', id) })
    overlays.add(id, 'observaciones', { position: { top: -11, right: 11 }, html: boton })
  }
}

function highlight(id: string | null) {
  const service = canvas()
  if (!service) return
  if (currentMarker) service.removeMarker(currentMarker, 'selected-node')
  currentMarker = id
  if (id) service.addMarker(id, 'selected-node')
}

function save(blob: Blob, extension: string, suffix = '') {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${props.downloadName || 'diagrama-proceso'}${suffix}.${extension}`
  link.click()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

function downloadBpmn() {
  if (originalXml) save(new Blob([originalXml], { type: 'application/xml' }), 'bpmn')
}

// Copia en el dialecto que importa Bizagi Modeler; la API la convierte al momento desde el mismo BPMN.
async function downloadBizagi() {
  if (downloading.value || !props.xmlUrl) return
  downloading.value = true
  try {
    const response = await fetch(props.xmlUrl.replace(/\/bpmn$/, '/bizagi'), { cache: 'no-store' })
    if (!response.ok) throw new Error(`No se pudo generar la copia para Bizagi (${response.status}).`)
    save(await response.blob(), 'bpmn', '-bizagi')
  } catch (error) {
    emit('error', error instanceof Error ? error.message : 'No se pudo descargar la copia para Bizagi.')
  } finally {
    downloading.value = false
  }
}

// Imagen del diagrama completo, como se ve (colores, números y marcas), a doble resolución.
async function downloadImage(kind: 'png' | 'jpeg') {
  if (!viewer || downloading.value) return
  downloading.value = true
  try {
    const { svg } = await viewer.saveSVG()
    const url = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' }))
    const image = new Image()
    await new Promise<void>((resolve, reject) => {
      image.onload = () => resolve()
      image.onerror = () => reject(new Error('No se pudo convertir el diagrama a imagen.'))
      image.src = url
    })
    URL.revokeObjectURL(url)
    const scale = Math.min(2, 16000 / Math.max(image.width, image.height, 1))
    const output = document.createElement('canvas')
    output.width = Math.round(image.width * scale)
    output.height = Math.round(image.height * scale)
    const context = output.getContext('2d')
    if (!context) throw new Error('El navegador no permite generar la imagen.')
    context.fillStyle = '#ffffff'
    context.fillRect(0, 0, output.width, output.height)
    context.drawImage(image, 0, 0, output.width, output.height)
    const blob = await new Promise<Blob | null>(resolve => output.toBlob(resolve, `image/${kind}`, 0.95))
    if (!blob) throw new Error('No se pudo generar la imagen.')
    save(blob, kind === 'jpeg' ? 'jpg' : 'png')
  } catch (error) {
    emit('error', error instanceof Error ? error.message : 'No se pudo descargar la imagen.')
  } finally {
    downloading.value = false
  }
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
watch([() => props.pins, mostrarMarcadores], markPins, { deep: true })

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
      <span class="toolbar-separator" aria-hidden="true" />
      <button type="button" :aria-pressed="mostrarMarcadores" title="Mostrar u ocultar los marcadores de observaciones" @click="mostrarMarcadores = !mostrarMarcadores">{{ mostrarMarcadores ? 'Ocultar marcas' : 'Ver marcas' }}</button>
      <details class="diagram-download">
        <summary title="Descargar el diagrama">{{ downloading ? 'Generando…' : 'Descargar' }}</summary>
        <div class="diagram-download-menu">
          <button type="button" @click="downloadBpmn">BPMN (XML editable)</button>
          <button type="button" :disabled="downloading" @click="downloadBizagi">Para Bizagi Modeler (.bpmn)</button>
          <button type="button" :disabled="downloading" @click="downloadImage('png')">Imagen PNG</button>
          <button type="button" :disabled="downloading" @click="downloadImage('jpeg')">Imagen JPG</button>
        </div>
      </details>
    </div>
    <div ref="host" class="diagram-canvas" aria-label="Diagrama BPMN; arrastre para moverse y use la rueda para ampliar" />
  </div>
</template>
