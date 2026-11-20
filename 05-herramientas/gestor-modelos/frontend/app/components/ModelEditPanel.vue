<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import type { components } from '~/types/api'

type Session = components['schemas']['SesionVista']
type Document = components['schemas']['DocumentoCopia']
type Preparation = components['schemas']['PreparacionSesion']
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
  await run(async () => {
    session.value = await request<Session | null>(`${base.value}/activa`)
    if (session.value) {
      const result = await request<Document>(`${sessionUrl.value}/documentos/${selected.value}`)
      document.value = result
      text.value = result.texto
    }
  })
}

async function start() {
  await run(async () => {
    session.value = await request<Session>(base.value, 'POST')
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
  })
}

onMounted(loadActive)
</script>

<template>
  <section class="edit-panel">
    <p>Edite la tabla, el sustento o las referencias en una copia. El modelo vigente cambia solo al integrar una preparación válida.</p>
    <p v-if="error" class="form-error" role="alert">{{ error }}</p>
    <p v-if="message" class="edit-message" role="status">{{ message }}</p>
    <button v-if="!session" class="primary-link" type="button" :disabled="busy" @click="start">Iniciar sesión recuperable</button>
    <template v-else>
      <div class="edit-session"><strong>Sesión {{ session.sesion.slice(0, 8) }}</strong><span>Revisión {{ session.revision }}</span></div>
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
