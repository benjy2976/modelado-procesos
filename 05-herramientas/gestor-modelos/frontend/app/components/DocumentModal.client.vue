<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'

const props = withDefaults(defineProps<{
  title: string
  url: string
  kind: 'markdown' | 'pdf' | 'text'
  page?: number
  fragment?: string
  location?: string
  rectangles?: number[][]
  anchorStatus?: string
}>(), { page: 1, fragment: '', location: '', rectangles: () => [], anchorStatus: 'SIN_COORDENADAS' })
const emit = defineEmits<{ close: [] }>()

const rendered = ref('')
const loading = ref(false)
const error = ref('')
const markdown = new MarkdownIt({ html: false, linkify: true, typographer: true })

function closeOnEscape(event: KeyboardEvent) {
  if (event.key === 'Escape') emit('close')
}

onMounted(async () => {
  window.addEventListener('keydown', closeOnEscape)
  if (props.kind === 'pdf') return
  loading.value = true
  try {
    const response = await fetch(props.url)
    if (!response.ok) throw new Error(`No se pudo abrir el documento (${response.status}).`)
    const content = await response.text()
    if (props.kind === 'markdown') {
      const body = content.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '')
      rendered.value = DOMPurify.sanitize(markdown.render(body))
    } else {
      rendered.value = DOMPurify.sanitize(`<pre>${markdown.utils.escapeHtml(content)}</pre>`)
    }
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : 'No se pudo leer el documento.'
  } finally {
    loading.value = false
  }
})

onBeforeUnmount(() => window.removeEventListener('keydown', closeOnEscape))
</script>

<template>
  <div class="modal-backdrop" @click.self="emit('close')">
    <section class="document-modal" role="dialog" aria-modal="true" :aria-label="title">
      <header class="modal-header">
        <div><span class="eyebrow">Documento de sustento</span><h2>{{ title }}</h2></div>
        <button type="button" class="modal-close" aria-label="Cerrar visor" @click="emit('close')">×</button>
      </header>
      <p v-if="location" class="modal-location">{{ location }}</p>
      <PdfReader v-if="kind === 'pdf'" :src="url" :initial-page="page" :fragment="fragment" :rectangles="rectangles" :anchor-status="anchorStatus" />
      <div v-else class="markdown-scroll">
        <p v-if="loading">Cargando documento…</p>
        <p v-else-if="error" role="alert">{{ error }}</p>
        <article v-else class="markdown-body" v-html="rendered" />
      </div>
    </section>
  </div>
</template>
