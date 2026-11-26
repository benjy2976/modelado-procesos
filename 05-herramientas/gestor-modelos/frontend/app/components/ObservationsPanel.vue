<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import type { Definicion } from './ResolutionPanel.vue'
import type { Cierre } from './CloseDialog.vue'
import type { components } from '~/types/api'
import { type ClaveEstado, estadoVisual, resumenObservacion } from '~/utils/estadoObservacion'

// Lista compacta de observaciones (rediseño 2026-11-26): contadores por estado, filtros, una fila por observación;
// el detalle, la decisión y el cierre se hacen en ObservationModal.
type Listado = components['schemas']['ListadoObservaciones']
type Registro = components['schemas']['ObservacionVista']
type Trabajo = components['schemas']['TrabajoVista']
type ListadoTrabajos = components['schemas']['ListadoTrabajos']

const props = defineProps<{ code: string; elementId: string | null; reference: string; focus?: { elemento: string; token: number } | null }>()
// Informa a la pestaña cuántas observaciones siguen abiertas tras cada carga y pide abrir una versión en el lienzo.
const emit = defineEmits<{ abiertas: [cantidad: number]; version: [numero: number] }>()
const list = ref<Listado | null>(null)
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const author = ref('')
const text = ref('')
const kind = ref<'OBSERVACION' | 'COMENTARIO'>('OBSERVACION')
const scope = ref<'elemento' | 'diagrama'>('diagrama')
const formOpen = ref(false)
const formCard = ref<HTMLElement | null>(null)
const query = ref('')
const AUTHOR_KEY = 'mesa.observaciones.autor'

type Filtro = 'atencion' | 'por-decidir' | 'en-curso' | 'resueltas' | 'todas' | 'seleccion'
const filter = ref<Filtro>('atencion')
const FILTROS: { id: Filtro; texto: string }[] = [
  { id: 'atencion', texto: 'Pendientes' }, { id: 'por-decidir', texto: 'Por decidir' }, { id: 'en-curso', texto: 'En curso' },
  { id: 'resueltas', texto: 'Resueltas' }, { id: 'todas', texto: 'Todas' }, { id: 'seleccion', texto: 'Caja seleccionada' }
]
const GRUPO: Record<ClaveEstado, Filtro[]> = {
  'por-decidir': ['atencion', 'por-decidir'],
  'cerrada-sin-decision': ['atencion'],
  'falta-evidencia': ['atencion', 'en-curso'],
  'en-analisis': ['atencion', 'en-curso'],
  'en-aplicacion': ['en-curso'],
  'resuelta-cambio': ['resueltas'],
  'resuelta-sin-cambio': ['resueltas']
}

const trabajos = ref<Trabajo[]>([])
const jobsFor = (id: string) => trabajos.value.filter(job => job.observacion === id)

const filas = computed(() => (list.value?.observaciones || []).map(item => ({
  item, visual: estadoVisual(item, jobsFor(item.id)), resumen: resumenObservacion(item),
  pie: pie(item)
})))
const contadores = computed(() => {
  const cuenta = (claves: ClaveEstado[]) => filas.value.filter(f => claves.includes(f.visual.clave)).length
  return [
    { id: 'por-decidir' as Filtro, n: cuenta(['por-decidir']), texto: 'Por decidir', color: '#9a4a00', fondo: '#fff7ea', borde: '#f1cf9b' },
    { id: 'en-curso' as Filtro, n: cuenta(['en-analisis', 'en-aplicacion', 'falta-evidencia']), texto: 'En curso o con evidencia pendiente', color: '#1d5aa6', fondo: '#eaf2fc', borde: '#bcd4f0' },
    { id: 'resueltas' as Filtro, n: cuenta(['resuelta-cambio', 'resuelta-sin-cambio']), texto: 'Resueltas con registro', color: '#1f6b3f', fondo: '#e8f5ec', borde: '#b5dcc2' },
    { id: 'atencion' as Filtro, n: cuenta(['cerrada-sin-decision']), texto: 'Cerradas sin decisión', color: '#a11d48', fondo: '#fdf0f4', borde: '#f1b9cb' }
  ]
})
const visibles = computed(() => {
  const texto = query.value.trim().toLocaleLowerCase('es')
  return filas.value.filter(f => {
    if (filter.value === 'seleccion' ? f.item.elemento !== (props.elementId || '') : filter.value !== 'todas' && !GRUPO[f.visual.clave].includes(filter.value)) return false
    return !texto || `${f.item.referencia} ${f.resumen.etiqueta} ${f.resumen.titulo}`.toLocaleLowerCase('es').includes(texto)
  })
})

function pie(item: Registro): string {
  const r = item.resolucion
  if (r?.cierre) return r.cierre.texto.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 120)
  if (r?.definicion) {
    const elegidas = (r.definicion.opciones || []).map(id => r.propuesta?.opciones.find(o => o.id === id)?.titulo).filter(Boolean)
    return `Definida: ${elegidas.join('; ') || 'respuesta propia'}`
  }
  const recomendada = r?.propuesta?.opciones.find(o => o.recomendada)
  if (recomendada) return `Recomendación: ${recomendada.titulo}`
  return `${item.autor} · ${new Date(item.fecha).toLocaleDateString('es-PE')}`
}

const abiertaId = ref<string | null>(null)
const abierta = computed(() => (list.value?.observaciones || []).find(item => item.id === abiertaId.value) || null)
const resolved = computed(() => (list.value?.observaciones || []).filter(item => item.estado === 'RESUELTA'))

async function toggleForm() {
  formOpen.value = !formOpen.value
  if (formOpen.value) {
    await nextTick()
    formCard.value?.querySelector<HTMLElement>('input, select, [contenteditable]')?.focus()
  }
}

watch(() => props.elementId, value => { scope.value = value ? 'elemento' : 'diagrama' }, { immediate: true })
watch(() => props.code, () => { abiertaId.value = null; void load() })
// Un clic en un marcador del diagrama abre la observación pendiente de esa caja (o filtra si hay varias).
watch(() => props.focus?.token, async () => {
  if (!props.focus) return
  if (!list.value) await load()
  const deCaja = filas.value.filter(f => f.item.elemento === props.focus!.elemento)
  const pendiente = deCaja.find(f => GRUPO[f.visual.clave].includes('atencion')) || deCaja[0]
  if (deCaja.length > 1) filter.value = 'seleccion'
  abiertaId.value = pendiente?.item.id || null
}, { immediate: true })
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

const base = (item: Registro) => `/api/procesos/${encodeURIComponent(props.code)}/observaciones/${encodeURIComponent(item.id)}`
const necesitaAutor = (accion: string) => {
  if (author.value.trim()) return false
  error.value = `Indique su nombre o equipo antes de ${accion}.`
  return true
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

async function reply(item: Registro, texto: string) {
  if (necesitaAutor('responder')) return
  await mutate(`${base(item)}/respuestas`, 'POST', { texto, autor: author.value, formato: 'html' })
}

async function requestAnalysis(item: Registro, nota: string) {
  if (necesitaAutor('solicitar el análisis')) return
  await mutate(`${base(item)}/solicitud-analisis`, 'POST', { autor: author.value, nota })
}

async function define(item: Registro, value: Definicion) {
  if (necesitaAutor('definir la respuesta')) return
  await mutate(`${base(item)}/definicion`, 'POST', { ...value, autor: author.value })
}

async function cerrar(item: Registro, value: Cierre) {
  if (necesitaAutor('cerrar la observación')) return
  await mutate(`${base(item)}/cierre`, 'POST', { ...value, formato: 'html', autor: author.value })
}

async function reabrir(item: Registro) {
  await mutate(base(item), 'PATCH', { estado: 'ABIERTA', autor: author.value })
}
</script>

<template>
  <div class="observations-panel">
    <p v-if="error" class="form-error" role="alert">{{ error }}</p>
    <div class="obs-counters">
      <button v-for="c in contadores" :key="c.id" type="button" class="obs-counter" :aria-pressed="filter === c.id" :style="{ color: c.color, background: c.fondo, borderColor: filter === c.id ? c.color : c.borde }" @click="filter = c.id">
        <strong>{{ c.n }}</strong><span>{{ c.texto }}</span>
      </button>
    </div>
    <div class="obs-toolbar">
      <label class="visually-hidden" for="buscar-observacion">Buscar observación</label>
      <input id="buscar-observacion" v-model="query" type="search" placeholder="Buscar por caja o tema">
      <button type="button" class="form-toggle" :aria-expanded="formOpen" aria-controls="new-observation-form" @click="toggleForm">
        <span aria-hidden="true">{{ formOpen ? '−' : '+' }}</span> {{ formOpen ? 'Ocultar' : 'Nueva' }}
      </button>
    </div>
    <div class="obs-filters" role="group" aria-label="Filtrar observaciones">
      <button v-for="f in FILTROS" :key="f.id" type="button" :aria-pressed="filter === f.id" :class="{ active: filter === f.id }" @click="filter = f.id">{{ f.texto }}</button>
    </div>
    <div v-show="formOpen" id="new-observation-form" ref="formCard" class="form-card">
      <h3>Nueva observación</h3>
      <label>Autor o equipo<input v-model="author" maxlength="100" autocomplete="name" placeholder="Nombre o equipo responsable"></label>
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

    <p v-if="loading && !list" class="muted">Cargando observaciones…</p>
    <p v-else-if="!visibles.length" class="muted">No hay observaciones en este filtro.</p>
    <ul class="obs-list">
      <li v-for="f in visibles" :key="f.item.id">
        <button type="button" class="obs-row" @click="abiertaId = f.item.id">
          <span class="obs-row-bar" :style="{ background: f.visual.barra }" aria-hidden="true" />
          <span class="obs-row-body">
            <span class="obs-row-meta">
              <span class="state-chip" :style="{ color: f.visual.color, background: f.visual.fondo }">{{ f.visual.texto }}</span>
              <span>{{ f.item.referencia || 'Diagrama completo' }} · {{ f.resumen.etiqueta }}</span>
            </span>
            <strong>{{ f.resumen.titulo }}</strong>
            <small>{{ f.pie }}</small>
          </span>
        </button>
      </li>
    </ul>

    <ObservationModal
      v-if="abierta" v-model:author="author" :code="code" :item="abierta" :jobs="jobsFor(abierta.id)" :resolved="resolved" :saving="saving"
      @close="abiertaId = null" @define="define(abierta, $event)" @request-analysis="requestAnalysis(abierta, $event)"
      @reply="reply(abierta, $event)" @cerrar="cerrar(abierta, $event)" @reabrir="reabrir(abierta)"
      @version="abiertaId = null; emit('version', $event)"
    />
  </div>
</template>
