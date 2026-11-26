<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import type { components } from '~/types/api'

// Versiones livianas (plan B): cada integración es una versión; se ve su cambio por caja y su diagrama.
type Listado = components['schemas']['ListadoVersiones']
type Resumen = components['schemas']['VersionResumen']
type Detalle = components['schemas']['VersionDetalle']
type Cambiado = components['schemas']['ElementoCambiado']
export type VistaVersion = { numero: number; url: string; cambios: Record<string, 'agregado' | 'modificado'> }

const props = defineProps<{ code: string; viewing: number | null; refreshToken?: number; abrirVersion?: { numero: number; token: number } | null }>()
const emit = defineEmits<{ view: [vista: VistaVersion | null]; select: [id: string] }>()
const versiones = ref<Resumen[]>([])
const detalle = ref<Detalle | null>(null)
const cargando = ref(false)
const error = ref('')

const base = computed(() => `/api/procesos/${encodeURIComponent(props.code)}/versiones`)
const fecha = (valor: string) => new Date(valor).toLocaleString('es-PE', { dateStyle: 'short', timeStyle: 'short' })

async function pedir<T>(url: string): Promise<T> {
  const respuesta = await fetch(url)
  const datos = await respuesta.json()
  if (!respuesta.ok) throw new Error(datos.error?.message || `Error HTTP ${respuesta.status}`)
  return datos as T
}

async function cargar() {
  cargando.value = true
  error.value = ''
  detalle.value = null
  try {
    versiones.value = (await pedir<Listado>(base.value)).versiones
  } catch (causa) {
    error.value = causa instanceof Error ? causa.message : 'No se pudieron cargar las versiones.'
  } finally {
    cargando.value = false
  }
}

async function abrir(numero: number) {
  error.value = ''
  try {
    detalle.value = await pedir<Detalle>(`${base.value}/${numero}`)
  } catch (causa) {
    error.value = causa instanceof Error ? causa.message : 'No se pudo abrir la versión.'
  }
}

function verDiagrama() {
  if (!detalle.value) return
  const cambios: VistaVersion['cambios'] = {}
  for (const item of detalle.value.elementos.agregados) if (item.bpmn_id) cambios[item.bpmn_id] = 'agregado'
  for (const item of detalle.value.elementos.modificados) if (item.bpmn_id) cambios[item.bpmn_id] = 'modificado'
  emit('view', { numero: detalle.value.numero, url: `${base.value}/${detalle.value.numero}/bpmn`, cambios })
}

function seleccionar(item: Cambiado) {
  if (item.bpmn_id) emit('select', item.bpmn_id)
}

const total = (v: Resumen) => v.conteo.agregados + v.conteo.retirados + v.conteo.modificados

// Desde una observación resuelta se pide ver su versión: se abre y se muestra en el lienzo.
async function abrirPedida() {
  if (!props.abrirVersion) return
  await abrir(props.abrirVersion.numero)
  verDiagrama()
}
onMounted(async () => {
  await cargar()
  await abrirPedida()
})
watch(() => props.abrirVersion?.token, () => { void abrirPedida() })
watch(() => props.code, cargar)
// Un cambio integrado por otro editor agrega versiones; se recarga la lista sin cerrar la versión abierta.
watch(() => props.refreshToken, async () => {
  const abierta = detalle.value?.numero
  await cargar()
  if (abierta) await abrir(abierta)
})
</script>

<template>
  <section class="history-panel">
    <p v-if="error" class="form-error" role="alert">{{ error }}</p>
    <p v-if="cargando" class="muted">Cargando versiones…</p>
    <p v-else-if="!versiones.length" class="muted">Aún no hay versiones: se crean al integrar un cambio desde «Editar copia» o por un agente.</p>

    <template v-if="!detalle">
      <ul class="history-list">
        <li v-for="v in versiones" :key="v.numero">
          <button type="button" @click="abrir(v.numero)">
            <strong>v{{ v.numero }}</strong>
            <span>{{ fecha(v.fecha) }} · {{ v.titular || 'sin titular' }}</span>
            <span v-if="v.motivo" class="history-reason">{{ v.motivo }}</span>
            <span class="history-counts">
              <span v-if="v.conteo.agregados" class="added">+{{ v.conteo.agregados }}</span>
              <span v-if="v.conteo.modificados" class="modified">~{{ v.conteo.modificados }}</span>
              <span v-if="v.conteo.retirados" class="removed">−{{ v.conteo.retirados }}</span>
              <span v-if="!total(v)">{{ v.documentos.sustento ? 'Solo sustento' : 'Sin cambios en cajas' }}</span>
            </span>
          </button>
        </li>
      </ul>
    </template>

    <template v-else>
      <div class="history-head">
        <button type="button" class="secondary-button" @click="detalle = null">← Versiones</button>
        <strong>v{{ detalle.numero }}</strong>
      </div>
      <p class="muted">{{ fecha(detalle.fecha) }} · {{ detalle.titular || 'sin titular' }}<span v-if="detalle.observacion"> · observación {{ detalle.observacion }}</span></p>
      <p v-if="detalle.motivo">{{ detalle.motivo }}</p>
      <div class="history-actions">
        <button v-if="props.viewing !== detalle.numero" type="button" class="primary-link" @click="verDiagrama">Ver diagrama de esta versión</button>
        <button v-else type="button" class="primary-link" @click="emit('view', null)">Volver al diagrama vigente</button>
      </div>

      <section v-if="detalle.elementos.agregados.length" class="history-group">
        <h3 class="added">Agregadas</h3>
        <button v-for="item in detalle.elementos.agregados" :key="item.id" type="button" class="history-item" @click="seleccionar(item)">{{ item.numero || item.id }} · {{ item.nombre }}</button>
      </section>
      <section v-if="detalle.elementos.modificados.length" class="history-group">
        <h3 class="modified">Modificadas</h3>
        <div v-for="item in detalle.elementos.modificados" :key="item.id" class="history-change">
          <button type="button" class="history-item" @click="seleccionar(item)">{{ item.numero || item.id }} · {{ item.nombre }}</button>
          <dl>
            <template v-for="(valores, campo) in item.campos || {}" :key="campo">
              <dt>{{ campo }}</dt>
              <dd><del>{{ valores[0] || '—' }}</del><ins>{{ valores[1] || '—' }}</ins></dd>
            </template>
          </dl>
        </div>
      </section>
      <section v-if="detalle.elementos.retirados.length" class="history-group">
        <h3 class="removed">Retiradas</h3>
        <p v-for="item in detalle.elementos.retirados" :key="item.id" class="history-item">{{ item.numero || item.id }} · {{ item.nombre }}</p>
      </section>
      <p v-if="detalle.secciones?.Pools || detalle.secciones?.Mensajes" class="muted">También cambiaron {{ [detalle.secciones?.Pools ? 'pools o carriles' : '', detalle.secciones?.Mensajes ? 'mensajes' : ''].filter(Boolean).join(' y ') }}.</p>
      <details v-if="detalle.diff.tabla"><summary>Diferencias de la tabla</summary><pre>{{ detalle.diff.tabla }}</pre></details>
      <details v-if="detalle.diff.sustento"><summary>Diferencias del sustento</summary><pre>{{ detalle.diff.sustento }}</pre></details>
    </template>
  </section>
</template>
