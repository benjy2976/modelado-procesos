<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import type { components } from '~/types/api'

type Listado = components['schemas']['ListadoObservaciones']
type Registro = components['schemas']['ObservacionVista']

const props = defineProps<{ code: string; elementId: string | null; reference: string }>()
const list = ref<Listado | null>(null)
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const author = ref('')
const text = ref('')
const kind = ref<'OBSERVACION' | 'COMENTARIO'>('OBSERVACION')
const scope = ref<'elemento' | 'diagrama'>('diagrama')
const filter = ref<'todas' | 'abiertas' | 'resueltas' | 'seleccion'>('todas')
const replyId = ref<string | null>(null)
const replyText = ref('')

const observations = computed(() => {
  const all = list.value?.observaciones || []
  if (filter.value === 'abiertas') return all.filter(item => item.estado === 'ABIERTA')
  if (filter.value === 'resueltas') return all.filter(item => item.estado === 'RESUELTA')
  if (filter.value === 'seleccion') return all.filter(item => item.elemento === (props.elementId || ''))
  return all
})

watch(() => props.elementId, value => { scope.value = value ? 'elemento' : 'diagrama' }, { immediate: true })
watch(() => props.code, () => { void load() })
onMounted(() => { void load() })

async function load() {
  loading.value = true
  error.value = ''
  try {
    const response = await fetch(`/api/procesos/${encodeURIComponent(props.code)}/observaciones`)
    if (!response.ok) throw new Error('No se pudieron cargar las observaciones.')
    list.value = await response.json() as Listado
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : 'No se pudieron cargar las observaciones.'
  } finally {
    loading.value = false
  }
}

async function mutate(path: string, method: 'POST' | 'PATCH', body: Record<string, string>) {
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
    tipo: kind.value
  })
  if (saved) text.value = ''
}

async function reply(item: Registro) {
  if (!replyText.value.trim() || !author.value.trim()) { error.value = 'Indique autor o equipo y una respuesta.'; return }
  const saved = await mutate(
    `/api/procesos/${encodeURIComponent(props.code)}/observaciones/${encodeURIComponent(item.id)}/respuestas`,
    'POST', { texto: replyText.value, autor: author.value }
  )
  if (saved) { replyText.value = ''; replyId.value = null }
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
    <div class="form-card">
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
      <label>Texto<textarea v-model="text" rows="4" maxlength="4000" placeholder="Describa el cambio o la duda con precisión" /></label>
      <button type="button" class="primary-link" :disabled="saving" @click="add">Registrar observación</button>
    </div>

    <div class="observation-list-heading">
      <h3>Lista de revisión <span>{{ observations.length }}</span></h3>
      <select v-model="filter" aria-label="Filtrar observaciones">
        <option value="todas">Todas</option><option value="abiertas">Abiertas</option><option value="resueltas">Resueltas</option>
        <option value="seleccion">{{ elementId ? 'Elemento seleccionado' : 'Diagrama' }}</option>
      </select>
    </div>
    <p v-if="loading" class="muted">Cargando observaciones…</p>
    <p v-else-if="!observations.length" class="muted">No hay observaciones en este filtro.</p>
    <article v-for="item in observations" :key="item.id" class="observation-card">
      <div class="observation-meta"><span :class="item.estado === 'ABIERTA' ? 'state-open' : 'state-closed'">{{ item.estado }}</span><span>{{ item.referencia || (item.elemento ? 'Elemento' : 'Diagrama') }}</span></div>
      <p>{{ item.texto }}</p>
      <small>{{ item.autor }} · {{ new Date(item.fecha).toLocaleString('es-PE') }}</small>
      <div v-if="item.respuestas?.length" class="replies">
        <div v-for="answer in item.respuestas" :key="answer.id"><strong>{{ answer.autor }}</strong><p>{{ answer.texto }}</p></div>
      </div>
      <details v-if="item.historial?.length"><summary>Historial ({{ item.historial.length }})</summary><ul><li v-for="(event, index) in item.historial" :key="index">{{ event.accion }} · {{ event.estado || event.autor || '' }} · {{ new Date(event.fecha).toLocaleString('es-PE') }}</li></ul></details>
      <div class="observation-actions">
        <button type="button" @click="replyId = replyId === item.id ? null : item.id">Responder</button>
        <button type="button" :disabled="saving" @click="toggle(item)">{{ item.estado === 'ABIERTA' ? 'Marcar resuelta' : 'Reabrir' }}</button>
      </div>
      <div v-if="replyId === item.id" class="reply-form"><textarea v-model="replyText" rows="3" maxlength="4000" placeholder="Escriba una respuesta" /><button type="button" :disabled="saving" @click="reply(item)">Guardar respuesta</button></div>
    </article>
  </div>
</template>
