<script setup lang="ts">
import { nextTick, onBeforeUnmount, onMounted, ref, shallowRef } from 'vue'
import { getDocument, GlobalWorkerOptions, type PDFDocumentLoadingTask, type PDFDocumentProxy, type RenderTask } from 'pdfjs-dist'
import workerURL from 'pdfjs-dist/build/pdf.worker.min.mjs?url'
import rendererURL from 'pdfjs-dist/build/pdf.renderer.min.mjs?url'

const props = withDefaults(defineProps<{
  src: string
  initialPage?: number
  fragment?: string
  rectangles?: number[][]
  anchorStatus?: string
}>(), {
  initialPage: 1,
  fragment: '',
  rectangles: () => [],
  anchorStatus: 'SIN_COORDENADAS'
})

GlobalWorkerOptions.workerSrc = workerURL
GlobalWorkerOptions.rendererSrc = rendererURL

const pdf = shallowRef<PDFDocumentProxy | null>(null)
const canvas = ref<HTMLCanvasElement | null>(null)
const pageNumber = ref(props.initialPage)
const pageCount = ref(0)
const scale = ref(1.2)
const loading = ref(true)
const error = ref('')
const highlight = ref<{ left: number; top: number; width: number; height: number }[]>([])

let loadingTask: PDFDocumentLoadingTask | null = null
let renderTask: RenderTask | null = null

async function draw() {
  if (!pdf.value || !canvas.value) return
  if (renderTask) {
    renderTask.cancel()
    try { await renderTask.promise } catch { /* Se canceló para dibujar otra página. */ }
    renderTask = null
  }
  highlight.value = []
  const page = await pdf.value.getPage(pageNumber.value)
  const viewport = page.getViewport({ scale: scale.value })
  const target = canvas.value
  const context = target.getContext('2d')
  if (!context) throw new Error('No se pudo crear el lienzo del PDF.')
  const ratio = Math.min(window.devicePixelRatio || 1, 2)
  target.width = Math.floor(viewport.width * ratio)
  target.height = Math.floor(viewport.height * ratio)
  target.style.width = `${viewport.width}px`
  target.style.height = `${viewport.height}px`
  renderTask = page.render({ canvas: target, canvasContext: context, viewport, transform: [ratio, 0, 0, ratio, 0, 0] })
  await renderTask.promise
  renderTask = null

  if (pageNumber.value !== props.initialPage || props.anchorStatus !== 'DISPONIBLE') return
  highlight.value = props.rectangles.map(([x0, y0, x1, y1]) => ({
    left: x0! * viewport.width,
    top: y0! * viewport.height,
    width: (x1! - x0!) * viewport.width,
    height: (y1! - y0!) * viewport.height
  }))
}

async function changePage(next: number) {
  if (next < 1 || next > pageCount.value) return
  pageNumber.value = next
  try { await draw() } catch { error.value = 'No se pudo dibujar la página solicitada.' }
}

async function changeZoom(factor: number) {
  scale.value = Math.max(0.5, Math.min(2.5, scale.value * factor))
  try { await draw() } catch { error.value = 'No se pudo actualizar el zoom del PDF.' }
}

onMounted(async () => {
  try {
    loadingTask = getDocument({ url: props.src })
    pdf.value = await loadingTask.promise
    pageCount.value = pdf.value.numPages
    if (pageNumber.value < 1 || pageNumber.value > pageCount.value) {
      throw new Error(`La página registrada (${pageNumber.value}) no existe en este PDF.`)
    }
    loading.value = false
    await nextTick()
    await draw()
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : 'No se pudo leer el PDF.'
    loading.value = false
  }
})

onBeforeUnmount(() => {
  renderTask?.cancel()
  void loadingTask?.destroy()
})
</script>

<template>
  <div class="pdf-reader">
    <div class="reader-toolbar">
      <button type="button" :disabled="pageNumber <= 1" @click="changePage(pageNumber - 1)">Anterior</button>
      <span>Página {{ pageNumber }} de {{ pageCount || '…' }}</span>
      <button type="button" :disabled="pageNumber >= pageCount" @click="changePage(pageNumber + 1)">Siguiente</button>
      <span class="toolbar-spacer" />
      <button type="button" @click="changeZoom(1 / 1.2)">−</button>
      <span>{{ Math.round(scale * 100) }} %</span>
      <button type="button" @click="changeZoom(1.2)">+</button>
    </div>
    <p v-if="fragment || anchorStatus !== 'SIN_COORDENADAS'" class="reader-note">
      Pasaje registrado<span v-if="fragment">: «{{ fragment }}»</span>.
      <span v-if="anchorStatus === 'DISPONIBLE'">Resaltado desde las coordenadas verificadas de la referencia.</span>
      <span v-else-if="anchorStatus === 'HASH_DISTINTO'">El PDF cambió; el resaltado se desactivó hasta revisar el enlace.</span>
      <span v-else>Esta referencia aún no tiene coordenadas de resaltado.</span>
    </p>
    <div v-if="loading" class="reader-wait">Cargando PDF…</div>
    <div v-if="error" class="reader-error" role="alert">{{ error }}</div>
    <div v-show="!loading && !error" class="pdf-scroll">
      <div class="pdf-sheet">
        <canvas ref="canvas" />
        <div v-for="(rect, index) in highlight" :key="index" class="pdf-highlight" :style="{ left: `${rect.left}px`, top: `${rect.top}px`, width: `${rect.width}px`, height: `${rect.height}px` }" />
      </div>
    </div>
  </div>
</template>
