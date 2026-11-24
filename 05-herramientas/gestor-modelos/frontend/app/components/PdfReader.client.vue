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
  segments?: { pagina: number; rol: string; rectangulos?: number[][] }[]
  anchorStatus?: string
}>(), {
  initialPage: 1,
  fragment: '',
  rectangles: () => [],
  segments: () => [],
  anchorStatus: 'SIN_COORDENADAS'
})

GlobalWorkerOptions.workerSrc = workerURL
GlobalWorkerOptions.rendererSrc = rendererURL

const pdf = shallowRef<PDFDocumentProxy | null>(null)
const canvases = ref<HTMLCanvasElement[]>([])
const segmentPages = [...new Set(props.segments.map(segment => segment.pagina))].sort((a, b) => a - b)
// Una referencia con tramos muestra juntas todas sus páginas; al navegar se vuelve a una sola página.
const pages = ref<number[]>(segmentPages.length ? segmentPages : [props.initialPage])
const pageNumber = ref(pages.value[0] ?? props.initialPage)
const pageCount = ref(0)
const scale = ref(1.2)
const loading = ref(true)
const error = ref('')
type Highlight = { left: number; top: number; width: number; height: number; role: string }
const highlights = ref<Highlight[][]>([])

function rectanglesFor(page: number): { rect: number[]; role: string }[] {
  if (props.anchorStatus !== 'DISPONIBLE') return []
  if (props.segments.length) {
    return props.segments
      .filter(segment => segment.pagina === page)
      .flatMap(segment => (segment.rectangulos ?? []).map(rect => ({ rect, role: segment.rol })))
  }
  return page === props.initialPage ? props.rectangles.map(rect => ({ rect, role: 'citado' })) : []
}

let loadingTask: PDFDocumentLoadingTask | null = null
let renderTask: RenderTask | null = null

async function drawPage(index: number, number: number): Promise<Highlight[]> {
  const target = canvases.value[index]
  if (!pdf.value || !target) return []
  const page = await pdf.value.getPage(number)
  const viewport = page.getViewport({ scale: scale.value })
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
  return rectanglesFor(number).map(({ rect: [x0, y0, x1, y1], role }) => ({
    left: x0! * viewport.width,
    top: y0! * viewport.height,
    width: (x1! - x0!) * viewport.width,
    height: (y1! - y0!) * viewport.height,
    role
  }))
}

async function draw() {
  if (!pdf.value) return
  if (renderTask) {
    renderTask.cancel()
    try { await renderTask.promise } catch { /* Se canceló para dibujar otra página. */ }
    renderTask = null
  }
  highlights.value = []
  await nextTick()
  const result: Highlight[][] = []
  for (const [index, number] of pages.value.entries()) result.push(await drawPage(index, number))
  highlights.value = result
}

async function changePage(next: number) {
  if (next < 1 || next > pageCount.value) return
  pageNumber.value = next
  pages.value = [next]
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
    const fuera = pages.value.find(page => page < 1 || page > pageCount.value)
    if (fuera !== undefined) {
      throw new Error(`La página registrada (${fuera}) no existe en este PDF.`)
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
      <span v-if="pages.length > 1">Páginas {{ pages.join(' y ') }} de {{ pageCount || '…' }}</span>
      <span v-else>Página {{ pageNumber }} de {{ pageCount || '…' }}</span>
      <button type="button" :disabled="pageNumber >= pageCount" @click="changePage(pageNumber + 1)">Siguiente</button>
      <span class="toolbar-spacer" />
      <button type="button" @click="changeZoom(1 / 1.2)">−</button>
      <span>{{ Math.round(scale * 100) }} %</span>
      <button type="button" @click="changeZoom(1.2)">+</button>
    </div>
    <p v-if="fragment || anchorStatus !== 'SIN_COORDENADAS'" class="reader-note">
      Pasaje registrado<span v-if="fragment">: «{{ fragment }}»</span>.
      <span v-if="anchorStatus === 'DISPONIBLE' && segmentPages.length > 1">
        La referencia abarca las páginas {{ segmentPages.join(' y ') }}: en amarillo el pasaje citado; en azul el antecedente necesario para entenderlo.
      </span>
      <span v-else-if="anchorStatus === 'DISPONIBLE'">Resaltado desde las coordenadas verificadas de la referencia.</span>
      <span v-else-if="anchorStatus === 'HASH_DISTINTO'">El PDF cambió; el resaltado se desactivó hasta revisar el enlace.</span>
      <span v-else>Esta referencia aún no tiene coordenadas de resaltado.</span>
    </p>
    <div v-if="loading" class="reader-wait">Cargando PDF…</div>
    <div v-if="error" class="reader-error" role="alert">{{ error }}</div>
    <div v-show="!loading && !error" class="pdf-scroll">
      <div v-for="(page, pageIndex) in pages" :key="page" class="pdf-page">
        <span v-if="pages.length > 1" class="pdf-page-label">Página {{ page }}</span>
        <div class="pdf-sheet">
        <canvas :ref="(element) => { if (element) canvases[pageIndex] = element as HTMLCanvasElement }" />
        <div
          v-for="(rect, index) in highlights[pageIndex] ?? []"
          :key="index"
          class="pdf-highlight"
          :class="{ antecedente: rect.role === 'antecedente' }"
          :style="{ left: `${rect.left}px`, top: `${rect.top}px`, width: `${rect.width}px`, height: `${rect.height}px` }"
        />
        </div>
      </div>
    </div>
  </div>
</template>
