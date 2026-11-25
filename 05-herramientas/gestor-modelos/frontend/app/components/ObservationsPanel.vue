<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import DOMPurify from 'dompurify'
import type { Definicion } from './ResolutionPanel.vue'
import type { components } from '~/types/api'

type Listado = components['schemas']['ListadoObservaciones']
type Registro = components['schemas']['ObservacionVista']
type Trabajo = components['schemas']['TrabajoVista']
type ListadoTrabajos = components['schemas']['ListadoTrabajos']

const props = defineProps<{ code: string; elementId: string | null; reference: string }>()
// Informa a la pestaña cuántas observaciones siguen abiertas tras cada carga.
const emit = defineEmits<{ abiertas: [cantidad: number] }>()
const list = ref<Listado | null>(null)
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const author = ref('')
const text = ref('')
const kind = ref<'OBSERVACION' | 'COMENTARIO'>('OBSERVACION')
const scope = ref<'elemento' | 'diagrama'>('diagrama')
const filter = ref<'todas' | 'abiertas' | 'resueltas' | 'por-definir' | 'definidas' | 'seleccion'>('todas')
const replyId = ref<string | null>(null)
const replyText = ref('')
const formOpen = ref(false)
const formCard = ref<HTMLElement | null>(null)
const AUTHOR_KEY = 'mesa.observaciones.autor'
// Solo se muestran las etiquetas de formato que también acepta el servidor.
const ALLOWED_TAGS = ['h3', 'h4', 'p', 'br', 'strong', 'b', 'em', 'i', 'u', 's', 'del', 'ul', 'ol', 'li', 'blockquote']

function rich(content: string, format?: string) {
  return format === 'html' ? DOMPurify.sanitize(content, { ALLOWED_TAGS, ALLOWED_ATTR: [] }) : ''
}

async function toggleForm() {
  formOpen.value = !formOpen.value
  if (formOpen.value) {
    await nextTick()
    formCard.value?.querySelector<HTMLElement>('input, select, [contenteditable]')?.focus()
  }
}

const observations = computed(() => {
  const all = list.value?.observaciones || []
  if (filter.value === 'abiertas') return all.filter(item => item.estado === 'ABIERTA')
  if (filter.value === 'resueltas') return all.filter(item => item.estado === 'RESUELTA')
  if (filter.value === 'por-definir') return all.filter(item => item.etapa === 'PROPUESTA')
  if (filter.value === 'definidas') return all.filter(item => ['DEFINIDA', 'EN-CORRECCION'].includes(item.etapa || ''))
  if (filter.value === 'seleccion') return all.filter(item => item.elemento === (props.elementId || ''))
  return all
})

watch(() => props.elementId, value => { scope.value = value ? 'elemento' : 'diagrama' }, { immediate: true })
watch(() => props.code, () => { void load() })
onMounted(() => {
  author.value = localStorage.getItem(AUTHOR_KEY) || ''
  void load()
})
watch(author, value => { localStorage.setItem(AUTHOR_KEY, value) })
watch(list, value => { if (value) emit('abiertas', value.observaciones.filter(item => item.estado === 'ABIERTA').length) })

async function load() {
  loading.value = true
  error.value = ''
  try {
    const response = await fetch(`/api/procesos/${encodeURIComponent(props.code)}/observaciones`)
    if (!response.ok) throw new Error('No se pudieron cargar las observaciones.')
    list.value = await response.json() as Listado
    const jobs = await fetch(`/api/procesos/${encodeURIComponent(props.code)}/trabajos`)
    trabajos.value = jobs.ok ? (await jobs.json() as ListadoTrabajos).trabajos : []
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : 'No se pudieron cargar las observaciones.'
  } finally {
    loading.value = false
  }
}

async function mutate(path: string, method: 'POST' | 'PATCH', body: Record<string, unknown>) {
  if (!list.value || saving.value) return false
  saving.value = true
  error.value = ''
  try {
    const response = await fetch(path, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...body, revision_esperada: list.value.revision })
    })
    if (!response.ok) {
      const payload = await response.json().catch(() => null) as { error?: { message?: string } } | null
      throw new Error(response.status === 409
        ? 'Las observaciones cambiaron. Se recargó la lista; revise antes de guardar de nuevo.'
        : payload?.error?.message || `No se pudo guardar (${response.status}).`)
    }
    await load()
    return true
  } catch (cause) {
    const message = cause instanceof Error ? cause.message : 'No se pudo guardar.'
    await load()
    error.value = message
    return false
  } finally {
    saving.value = false
  }
}

async function add() {
  if (!text.value.trim() || !author.value.trim()) { error.value = 'Indique autor o equipo y el texto de la observación.'; return }
  const saved = await mutate(`/api/procesos/${encodeURIComponent(props.code)}/observaciones`, 'POST', {
    elemento: scope.value === 'elemento' ? props.elementId || '' : '',
    referencia: scope.value === 'elemento' ? props.reference : '',
    texto: text.value,
    autor: author.value,
    tipo: kind.value,
    formato: 'html'
  })
  if (saved) { text.value = ''; formOpen.value = false }
}

async function reply(item: Registro) {
  if (!replyText.value.trim() || !author.value.trim()) { error.value = 'Indique autor o equipo y una respuesta.'; return }
  const saved = await mutate(
    `/api/procesos/${encodeURIComponent(props.code)}/observaciones/${encodeURIComponent(item.id)}/respuestas`,
    'POST', { texto: replyText.value, autor: author.value, formato: 'html' }
  )
  if (saved) { replyText.value = ''; replyId.value = null }
}

const trabajos = ref<Trabajo[]>([])
const jobsFor = (id: string) => trabajos.value.filter(job => job.observacion === id)

async function requestAnalysis(item: Registro, nota: string) {
  if (!author.value.trim()) { error.value = 'Indique su nombre o equipo antes de solicitar el análisis.'; return }
  await mutate(
    `/api/procesos/${encodeURIComponent(props.code)}/observaciones/${encodeURIComponent(item.id)}/solicitud-analisis`,
    'POST', { autor: author.value, nota }
  )
}

const resolved = computed(() => (list.value?.observaciones || []).filter(item => item.estado === 'RESUELTA'))

async function define(item: Registro, value: Definicion) {
  if (!author.value.trim()) { error.value = 'Indique su nombre o equipo antes de definir la respuesta.'; return }
  await mutate(
    `/api/procesos/${encodeURIComponent(props.code)}/observaciones/${encodeURIComponent(item.id)}/definicion`,
    'POST', { ...value, autor: author.value }
  )
}

async function toggle(item: Registro) {
  await mutate(
    `/api/procesos/${encodeURIComponent(props.code)}/observaciones/${encodeURIComponent(item.id)}`,
    'PATCH', { estado: item.estado === 'ABIERTA' ? 'RESUELTA' : 'ABIERTA', autor: author.value }
  )
}
</script>

<template>
  <div class="observations-panel">
    <p v-if="error" class="form-error" role="alert">{{ error }}</p>
    <button
      type="button" class="form-toggle" :aria-expanded="formOpen" aria-controls="new-observation-form"
      @click="toggleForm"
    ><span aria-hidden="true">{{ formOpen ? '−' : '+' }}</span> {{ formOpen ? 'Ocultar formulario' : 'Nueva observación' }}</button>
    <div v-show="formOpen" id="new-observation-form" ref="formCard" class="form-card">
      <h3>Nueva observación</h3>
      <label>Autor o equipo<input v-model="author" maxlength="100" autocomplete="name" placeholder="Nombre o equipo responsable" /></label>
      <label>Alcance
        <select v-model="scope">
          <option value="diagrama">Diagrama completo</option>
          <option v-if="elementId" value="elemento">Elemento {{ reference || elementId }}</option>
        </select>
      </label>
      <label>Tipo
        <select v-model="kind"><option value="OBSERVACION">Observación</option><option value="COMENTARIO">Comentario</option></select>
      </label>
      <div class="field-label">Texto</div>
      <RichTextEditor v-model="text" label="Texto de la observación" placeholder="Describa el cambio o la duda con precisión" />
      <div class="form-buttons">
        <button type="button" class="primary-link" :disabled="saving" @click="add">Registrar observación</button>
        <button type="button" class="secondary-button" @click="formOpen = false">Cancelar</button>
      </div>
    </div>

    <div class="observation-list-heading">
      <h3>Lista de revisión <span>{{ observations.length }}</span></h3>
      <select v-model="filter" aria-label="Filtrar observaciones">
        <option value="todas">Todas</option><option value="abiertas">Abiertas</option><option value="por-definir">Por definir</option>
        <option value="definidas">Definidas</option><option value="resueltas">Resueltas</option>
        <option value="seleccion">{{ elementId ? 'Elemento seleccionado' : 'Diagrama' }}</option>
      </select>
    </div>
    <p v-if="loading" class="muted">Cargando observaciones…</p>
    <p v-else-if="!observations.length" class="muted">No hay observaciones en este filtro.</p>
    <article v-for="item in observations" :key="item.id" class="observation-card">
      <div class="observation-meta"><span :class="item.estado === 'ABIERTA' ? 'state-open' : 'state-closed'">{{ item.estado }}</span><span>{{ item.referencia || (item.elemento ? 'Elemento' : 'Diagrama') }}</span></div>
      <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
      <div v-if="item.formato === 'html'" class="rich-content" v-html="rich(item.texto, item.formato)" />
      <p v-else>{{ item.texto }}</p>
      <small>{{ item.autor }} · {{ new Date(item.fecha).toLocaleString('es-PE') }}</small>
      <ResolutionPanel :item="item" :resolved="resolved" :saving="saving" :jobs="jobsFor(item.id)" @define="define(item, $event)" @request-analysis="requestAnalysis(item, $event)" />
      <div v-if="item.respuestas?.length" class="replies">
        <div v-for="answer in item.respuestas" :key="answer.id">
          <strong>{{ answer.autor }}</strong>
          <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
          <div v-if="answer.formato === 'html'" class="rich-content" v-html="rich(answer.texto, answer.formato)" />
          <p v-else>{{ answer.texto }}</p>
        </div>
      </div>
      <details v-if="item.historial?.length"><summary>Historial ({{ item.historial.length }})</summary><ul><li v-for="(event, index) in item.historial" :key="index">{{ event.accion }} · {{ event.estado || event.autor || '' }} · {{ new Date(event.fecha).toLocaleString('es-PE') }}</li></ul></details>
      <div class="observation-actions">
        <button type="button" @click="replyId = replyId === item.id ? null : item.id">Responder</button>
        <button type="button" :disabled="saving" @click="toggle(item)">{{ item.estado === 'ABIERTA' ? 'Marcar resuelta' : 'Reabrir' }}</button>
      </div>
      <div v-if="replyId === item.id" class="reply-form">
        <label>Autor o equipo<input v-model="author" maxlength="100" autocomplete="name" placeholder="Nombre o equipo responsable" /></label>
        <RichTextEditor v-model="replyText" label="Respuesta" placeholder="Escriba una respuesta" />
        <button type="button" :disabled="saving" @click="reply(item)">Guardar respuesta</button>
      </div>
    </article>
  </div>
</template>
