<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import DOMPurify from 'dompurify'
import type { components } from '~/types/api'

// Etapas de resolución (DEC-065): muestra el análisis y las opciones del agente y permite que una persona defina.
type Registro = components['schemas']['ObservacionVista']
export type Definicion = { tipo: 'OPCION' | 'OPCIONES' | 'MANUAL' | 'VINCULADA'; opciones: string[]; texto: string; formato: 'html' | 'texto'; vinculada_a: string }

const props = defineProps<{ item: Registro; resolved: Registro[]; saving: boolean }>()
const emit = defineEmits<{ define: [value: Definicion] }>()

const ALLOWED_TAGS = ['h3', 'h4', 'p', 'br', 'strong', 'b', 'em', 'i', 'u', 's', 'del', 'ul', 'ol', 'li', 'blockquote']
const ETAPAS: Record<string, string> = {
  'REGISTRADA': 'Registrada', 'EN-ANALISIS': 'En análisis', 'PROPUESTA': 'Por definir', 'DEFINIDA': 'Definida',
  'EN-CORRECCION': 'En corrección', 'PENDIENTE-EVIDENCIA': 'Pendiente de evidencia', 'RESUELTA': 'Resuelta'
}
const EFECTOS: Record<string, string> = {
  'CAMBIO-MODELO': 'Cambio del modelo', 'CAMBIO-SUSTENTO': 'Cambio del sustento', 'DECISION': 'Decisión',
  'ACLARACION': 'Aclaración', 'NO-PROCEDE': 'No procede', 'PENDIENTE-EVIDENCIA': 'Pendiente de evidencia'
}

const mode = ref<'opciones' | 'manual' | 'vinculada'>(props.item.resolucion?.propuesta ? 'opciones' : 'manual')
const chosen = ref<string[]>([])
const manualText = ref('')
const linkedId = ref('')

const resolucion = computed(() => props.item.resolucion || null)
const propuesta = computed(() => resolucion.value?.propuesta || null)
const etapa = computed(() => props.item.etapa || (props.item.estado === 'RESUELTA' ? 'RESUELTA' : 'REGISTRADA'))
const multiple = computed(() => propuesta.value?.seleccion === 'MULTIPLE')
const canDefine = computed(() => ['REGISTRADA', 'EN-ANALISIS', 'PROPUESTA'].includes(etapa.value))
const candidates = computed(() => props.resolved.filter(other => other.id !== props.item.id))
const defined = computed(() => resolucion.value?.definicion || null)
const chosenTitles = computed(() => (defined.value?.opciones || [])
  .map(id => propuesta.value?.opciones.find(option => option.id === id))
  .filter(Boolean)
  .map(option => `${option!.id}. ${option!.titulo}`))

function rich(content: string, format?: string | null) {
  return format === 'html' ? DOMPurify.sanitize(content, { ALLOWED_TAGS, ALLOWED_ATTR: [] }) : DOMPurify.sanitize(content, { ALLOWED_TAGS: [] })
}

function toggle(id: string) {
  if (!multiple.value) { chosen.value = [id]; return }
  chosen.value = chosen.value.includes(id) ? chosen.value.filter(value => value !== id) : [...chosen.value, id]
}

function submit() {
  if (mode.value === 'opciones') {
    emit('define', { tipo: chosen.value.length > 1 ? 'OPCIONES' : 'OPCION', opciones: chosen.value, texto: '', formato: 'html', vinculada_a: '' })
  } else if (mode.value === 'manual') {
    emit('define', { tipo: 'MANUAL', opciones: [], texto: manualText.value, formato: 'html', vinculada_a: '' })
  } else {
    emit('define', { tipo: 'VINCULADA', opciones: [], texto: '', formato: 'html', vinculada_a: linkedId.value })
  }
}

watch(propuesta, value => { if (value && mode.value === 'manual' && !manualText.value) mode.value = 'opciones' })

const ready = computed(() => mode.value === 'opciones' ? chosen.value.length > 0
  : mode.value === 'manual' ? Boolean(manualText.value.trim()) : Boolean(linkedId.value))
</script>

<template>
  <section class="resolution" :aria-label="`Resolución: ${ETAPAS[etapa] || etapa}`">
    <div class="resolution-stage" :data-stage="etapa">{{ ETAPAS[etapa] || etapa }}</div>

    <details v-if="resolucion?.analisis" class="resolution-block" :open="etapa === 'PROPUESTA'">
      <summary>Análisis de {{ resolucion.analisis.autor }} · {{ resolucion.analisis.clase }}</summary>
      <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
      <div class="rich-content" v-html="rich(resolucion.analisis.texto, resolucion.analisis.formato)" />
      <p v-if="resolucion.analisis.fuentes?.length" class="resolution-sources">Consultado: {{ resolucion.analisis.fuentes.join(' · ') }}</p>
    </details>

    <div v-if="canDefine" class="resolution-form">
      <div class="resolution-modes" role="radiogroup" aria-label="Forma de responder">
        <button v-if="propuesta" type="button" role="radio" :aria-checked="mode === 'opciones'" :class="{ active: mode === 'opciones' }" @click="mode = 'opciones'">Opciones propuestas</button>
        <button type="button" role="radio" :aria-checked="mode === 'manual'" :class="{ active: mode === 'manual' }" @click="mode = 'manual'">Respuesta propia</button>
        <button type="button" role="radio" :aria-checked="mode === 'vinculada'" :class="{ active: mode === 'vinculada' }" @click="mode = 'vinculada'">Vincular a otra</button>
      </div>

      <template v-if="mode === 'opciones' && propuesta">
        <p class="muted">{{ multiple ? 'Puede elegir una o varias opciones.' : 'Elija una opción.' }}</p>
        <label v-for="option in propuesta.opciones" :key="option.id" class="resolution-option" :class="{ chosen: chosen.includes(option.id) }">
          <input :type="multiple ? 'checkbox' : 'radio'" :name="`opcion-${item.id}`" :value="option.id" :checked="chosen.includes(option.id)" @change="toggle(option.id)">
          <span class="resolution-option__body">
            <strong>{{ option.id }}. {{ option.titulo }}</strong>
            <span class="resolution-chips"><span class="chip">{{ EFECTOS[option.efecto] || option.efecto }}</span><span v-if="option.recomendada" class="chip chip--recommended">Recomendada</span></span>
            <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
            <span class="rich-content" v-html="rich(option.detalle, option.formato)" />
            <small v-if="option.elementos?.length">Cajas: {{ option.elementos.join(', ') }}</small>
          </span>
        </label>
      </template>
      <RichTextEditor v-else-if="mode === 'manual'" v-model="manualText" label="Respuesta propia" placeholder="Escriba cómo debe resolverse" />
      <label v-else-if="mode === 'vinculada'" class="resolution-link">Observación ya resuelta
        <select v-model="linkedId">
          <option value="">Seleccione…</option>
          <option v-for="other in candidates" :key="other.id" :value="other.id">{{ other.referencia || 'Diagrama' }} · {{ rich(other.texto).slice(0, 70) }}</option>
        </select>
        <small v-if="!candidates.length" class="muted">Aún no hay observaciones resueltas en este proceso.</small>
      </label>
      <button type="button" class="primary-link" :disabled="saving || !ready" @click="submit">Definir respuesta</button>
    </div>

    <div v-if="defined" class="resolution-block">
      <strong>Definida por {{ defined.autor }}</strong>
      <ul v-if="chosenTitles.length"><li v-for="title in chosenTitles" :key="title">{{ title }}</li></ul>
      <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
      <div v-if="defined.texto" class="rich-content" v-html="rich(defined.texto, defined.formato)" />
      <p v-if="defined.vinculada_a">Vinculada a {{ defined.vinculada_a.referencia || defined.vinculada_a.id }}</p>
    </div>

    <div v-if="resolucion?.aplicacion" class="resolution-block">
      <strong>{{ resolucion.aplicacion.cerrada ? 'Aplicada' : 'En espera de evidencia' }} por {{ resolucion.aplicacion.autor }}</strong>
      <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
      <div class="rich-content" v-html="rich(resolucion.aplicacion.texto, resolucion.aplicacion.formato)" />
      <small>
        <template v-if="resolucion.aplicacion.decision">Decisión {{ resolucion.aplicacion.decision }} · </template>
        <template v-if="resolucion.aplicacion.sesion">Sesión {{ resolucion.aplicacion.sesion.slice(0, 8) }} · </template>
        <template v-if="resolucion.aplicacion.cambios?.length">Cambios: {{ resolucion.aplicacion.cambios.join(', ') }}</template>
      </small>
    </div>
  </section>
</template>
