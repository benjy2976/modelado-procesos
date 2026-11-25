<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import type { components } from '~/types/api'

type Session = components['schemas']['SesionVista']
type Document = components['schemas']['DocumentoCopia']
type Preparation = components['schemas']['PreparacionSesion']
type ModelState = components['schemas']['EstadoModelo']
type Editable = 'tabla' | 'sustento' | 'fuentes_visor'

const props = defineProps<{ code: string }>()
const emit = defineEmits<{ integrated: [] }>()
const session = ref<Session | null>(null)
const selected = ref<Editable>('tabla')
const document = ref<Document | null>(null)
const text = ref('')
const busy = ref(false)
const message = ref('')
const error = ref('')
const dirty = computed(() => document.value !== null && text.value !== document.value.texto)
const base = computed(() => `/api/procesos/${encodeURIComponent(props.code)}/sesiones`)
const sessionUrl = computed(() => session.value ? `${base.value}/${session.value.sesion}` : '')
const preparation = computed<Preparation | null>(() => session.value?.preparacion ?? null)
// Bloqueo del modelo (DEC-069): quién lo tiene, hasta cuándo y qué borradores del asistente esperan revisión.
const AUTHOR_KEY = 'mesa.observaciones.autor'
const author = ref('')
const reason = ref('')
const releaseReason = ref('')
const state = ref<ModelState | null>(null)
const lockedByOther = computed(() => Boolean(state.value?.bloqueo && !session.value))
const hora = (fecha?: string | null) => fecha ? new Date(fecha).toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' }) : ''

async function loadState() {
  state.value = await request<ModelState>(`/api/procesos/${encodeURIComponent(props.code)}/edicion`)
}

async function request<T>(url: string, method = 'GET', body?: object): Promise<T> {
  const response = await fetch(url, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined
  })
  const data = await response.json()
  if (!response.ok) throw new Error(data.error?.message || `Error HTTP ${response.status}`)
  return data as T
}

async function run(task: () => Promise<void>) {
  busy.value = true
  error.value = ''
  message.value = ''
  try { await task() } catch (failure) {
    error.value = failure instanceof Error ? failure.message : 'No se pudo completar la operación.'
  } finally { busy.value = false }
}

async function loadDocument(name: Editable) {
  if (!session.value) return
  if (dirty.value && name !== selected.value) {
    error.value = 'Guarde el documento actual antes de cambiar de pestaña.'
    return
  }
  await run(async () => {
    const result = await request<Document>(`${sessionUrl.value}/documentos/${name}`)
    document.value = result
    text.value = result.texto
    selected.value = name
  })
}

async function loadActive() {
  author.value = localStorage.getItem(AUTHOR_KEY) || ''
  await run(async () => {
    await loadState()
    const active = await request<Session | null>(`${base.value}/activa`)
    // Solo se continúa la sesión propia; la de otro titular se muestra como bloqueo.
    session.value = active && active.titular === author.value.trim() ? active : null
    if (session.value) {
      const result = await request<Document>(`${sessionUrl.value}/documentos/${selected.value}`)
      document.value = result
      text.value = result.texto
    }
  })
}

async function openDraft(id: string) {
  await run(async () => {
    session.value = await request<Session>(`${base.value}/${id}`)
    const result = await request<Document>(`${sessionUrl.value}/documentos/tabla`)
    document.value = result
    text.value = result.texto
    selected.value = 'tabla'
    message.value = 'Borrador abierto. Se integra solo cuando el modelo está libre.'
  })
}

async function release() {
  await run(async () => {
    await request(`/api/procesos/${encodeURIComponent(props.code)}/edicion/liberacion`, 'POST', {
      autor: author.value.trim(),
      motivo: releaseReason.value.trim()
    })
    releaseReason.value = ''
    await loadState()
    message.value = 'Bloqueo liberado; la sesión anterior queda registrada como LIBERADA.'
  })
}

async function start() {
  if (!author.value.trim()) {
    error.value = 'Indique su nombre para tomar el modelo.'
    return
  }
  localStorage.setItem(AUTHOR_KEY, author.value.trim())
  await run(async () => {
    session.value = await request<Session>(base.value, 'POST', { titular: author.value.trim(), motivo: reason.value.trim() })
    const result = await request<Document>(`${sessionUrl.value}/documentos/tabla`)
    document.value = result
    text.value = result.texto
    selected.value = 'tabla'
    message.value = 'Copia creada a partir del estado actual, incluidos cambios sin commit.'
  })
}

async function save() {
  if (!session.value || !document.value) return
  await run(async () => {
    await request(`${sessionUrl.value}/documentos/${selected.value}`, 'PUT', {
      texto: text.value,
      revision_esperada: document.value?.revision
    })
    document.value = await request<Document>(`${sessionUrl.value}/documentos/${selected.value}`)
    session.value = await request<Session>(sessionUrl.value)
    message.value = 'Cambio guardado solo en la copia.'
  })
}

async function prepare() {
  if (!session.value || dirty.value) return
  await run(async () => {
    await request(`${sessionUrl.value}/preparacion`, 'POST')
    session.value = await request<Session>(sessionUrl.value)
    message.value = preparation.value?.aplicable
      ? 'Diff y validación listos para integración.'
      : 'La copia necesita corrección o no contiene cambios.'
  })
}

async function integrate() {
  if (!session.value || !preparation.value?.aplicable || dirty.value) return
  await run(async () => {
    await request(`${sessionUrl.value}/integracion`, 'POST', { revision_esperada: session.value?.revision })
    session.value = null
    document.value = null
    text.value = ''
    await loadState()
    emit('integrated')
  })
}

async function close() {
  if (!session.value) return
  await run(async () => {
    await request(`${sessionUrl.value}/cierre`, 'POST')
    session.value = null
    document.value = null
    text.value = ''
    message.value = 'Sesión cerrada. La instantánea y la copia permanecen en el almacén local.'
    await loadState()
  })
}

onMounted(loadActive)
</script>

<template>
  <section class="edit-panel">
    <p>Edite la tabla, el sustento o las referencias en una copia. El modelo vigente cambia solo al integrar una preparación válida.</p>
    <p v-if="error" class="form-error" role="alert">{{ error }}</p>
    <p v-if="message" class="edit-message" role="status">{{ message }}</p>
    <template v-if="!session">
      <p v-if="state?.estado === 'APROBADO'" class="edit-lock">El modelo está APROBADO y no se edita.</p>
      <div v-else-if="lockedByOther && state?.bloqueo" class="edit-lock" role="status">
        <strong>En edición por {{ state.bloqueo.titular }}</strong>
        <span v-if="state.bloqueo.motivo">{{ state.bloqueo.motivo }}</span>
        <span>Desde {{ hora(state.bloqueo.desde) }} · vence {{ hora(state.bloqueo.vence) }} si no hay actividad</span>
        <details>
          <summary>Liberar el bloqueo</summary>
          <p>Úselo solo si el titular dejó de trabajar (por ejemplo, un agente caído). La sesión queda registrada como LIBERADA.</p>
          <input v-model="author" class="edit-input" type="text" maxlength="120" placeholder="Su nombre">
          <input v-model="releaseReason" class="edit-input" type="text" maxlength="500" placeholder="Motivo (mín. 10 caracteres)">
          <button type="button" :disabled="busy || !author.trim() || releaseReason.trim().length < 10" @click="release">Liberar</button>
        </details>
      </div>
      <template v-else>
        <input v-model="author" class="edit-input" type="text" maxlength="120" placeholder="Su nombre (titular de la edición)">
        <input v-model="reason" class="edit-input" type="text" maxlength="500" placeholder="Motivo (opcional)">
        <button class="primary-link" type="button" :disabled="busy || !author.trim()" @click="start">Tomar el modelo y editar</button>
      </template>
      <section v-if="state?.borradores?.length" class="edit-drafts">
        <h3>Borradores del asistente</h3>
        <ul>
          <li v-for="draft in state.borradores" :key="draft.sesion">
            <span>{{ draft.motivo || 'Sin motivo' }} · {{ draft.titular }} · {{ hora(draft.creada) }}</span>
            <button type="button" :disabled="busy" @click="openDraft(draft.sesion)">Abrir</button>
          </li>
        </ul>
      </section>
    </template>
    <template v-else>
      <div class="edit-session"><strong>{{ session.modo === 'BORRADOR' ? 'Borrador' : 'Sesión' }} {{ session.sesion.slice(0, 8) }}</strong><span>{{ session.titular }} · revisión {{ session.revision }}</span></div>
      <div class="edit-tabs" role="tablist" aria-label="Documento editable">
        <button v-for="name in (['tabla', 'sustento', 'fuentes_visor'] as const)" :key="name" type="button" :class="{ active: selected === name }" :disabled="busy" @click="loadDocument(name)">{{ name === 'fuentes_visor' ? 'Fuentes' : name }}</button>
      </div>
      <label class="edit-label" for="model-text">Contenido de la {{ selected === 'fuentes_visor' ? 'referencias' : selected }}<span v-if="dirty"> · sin guardar</span></label>
      <textarea id="model-text" v-model="text" class="edit-text" spellcheck="false" :disabled="busy" />
      <button class="primary-link" type="button" :disabled="busy || !dirty" @click="save">Guardar en copia</button>
      <div class="edit-actions">
        <button type="button" :disabled="busy || dirty" @click="prepare">Preparar y validar</button>
        <button type="button" :disabled="busy || !preparation?.aplicable || dirty" @click="integrate">Integrar al proceso</button>
        <button type="button" :disabled="busy" @click="close">Cerrar sin integrar</button>
      </div>
      <section v-if="preparation" class="edit-report">
        <h3>Resultado de preparación</h3>
        <p>{{ preparation.aplicable ? 'Apta para integrar' : 'Pendiente de corrección' }} · {{ preparation.cambios.join(', ') || 'Sin cambios' }}</p>
        <details><summary>Validación D1–D5</summary><pre>{{ preparation.validacion.salida }}{{ preparation.validacion.errores }}</pre></details>
        <details open><summary>Comparar con la instantánea</summary><pre>{{ preparation.diff || 'Sin diferencias' }}</pre></details>
      </section>
    </template>
  </section>
</template>
