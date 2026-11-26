<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import type { components } from '~/types/api'
import type { Definicion } from './ResolutionPanel.vue'
import RichTextEditor from './RichTextEditor.vue'

// Cerrar con decisión (rediseño 2026-11-26): reemplaza «Marcar resuelta». Cada forma de cierre pide lo suyo y
// dice qué pasará; los cambios de modelo o sustento se definen para que el agente los aplique.
type Registro = components['schemas']['ObservacionVista']
export type Cierre = { tipo: 'ACLARADA' | 'NO-PROCEDE' | 'PENDIENTE-EVIDENCIA'; texto: string }
type Forma = 'diagrama' | 'sustento' | 'aclarada' | 'noprocede' | 'evidencia' | 'vincular'

const props = defineProps<{ item: Registro; resolved: Registro[]; saving: boolean }>()
const author = defineModel<string>('author', { required: true })
const emit = defineEmits<{ cancel: []; define: [value: Definicion]; cerrar: [value: Cierre] }>()

const FORMAS: { id: Forma; titulo: string; ayuda: string; color: string; nota: string; boton: string; consecuencia: string }[] = [
  { id: 'diagrama', titulo: 'Cambiar el diagrama', ayuda: 'Se elige una opción de la propuesta; el agente la aplica en su sesión.', color: '#1d5aa6', nota: 'Indicaciones para el agente', boton: 'Definir y encargar el cambio', consecuencia: 'Pasa a «En aplicación». Se cierra sola cuando el agente integre el cambio, con la versión y las cajas afectadas.' },
  { id: 'sustento', titulo: 'Solo explicarlo en el sustento', ayuda: 'El diagrama queda igual; se agrega la explicación o la fuente.', color: '#40586a', nota: 'Qué debe decir el sustento', boton: 'Definir y encargar la explicación', consecuencia: 'El agente actualiza el sustento en su sesión; queda una versión sin cajas cambiadas.' },
  { id: 'aclarada', titulo: 'Aclarada, sin cambios', ayuda: 'La respuesta resuelve la duda; no hay que tocar nada.', color: '#1f6b3f', nota: 'Respuesta (obligatoria)', boton: 'Cerrar como aclarada', consecuencia: 'Se cierra ahora con la respuesta visible en la tarjeta y en el historial.' },
  { id: 'noprocede', titulo: 'No procede', ayuda: 'La observación no aplica o parte de un supuesto equivocado.', color: '#5b6b7a', nota: 'Motivo (obligatorio)', boton: 'Cerrar como no procede', consecuencia: 'Se cierra ahora con el motivo visible; no se toca el modelo.' },
  { id: 'evidencia', titulo: 'Falta evidencia', ayuda: 'No se puede decidir hasta tener un documento o una confirmación.', color: '#6b3fa0', nota: 'Qué falta y quién lo consigue (obligatorio)', boton: 'Dejar pendiente de evidencia', consecuencia: 'Sigue abierta con la etiqueta «Falta evidencia».' },
  { id: 'vincular', titulo: 'Se resuelve con otra observación', ayuda: 'Otra observación ya resuelta de este proceso cubre el cambio.', color: '#0f6e74', nota: 'Comentario (opcional)', boton: 'Vincular', consecuencia: 'Pasa a «En aplicación» vinculada; el agente registra el cierre con la referencia.' }
]

const opciones = computed(() => props.item.resolucion?.propuesta?.opciones || [])
const recomendada = computed(() => opciones.value.find(o => o.recomendada) || null)
const inicial = (): Forma => {
  const efecto = recomendada.value?.efecto
  if (efecto === 'CAMBIO-SUSTENTO') return 'sustento'
  if (efecto === 'ACLARACION') return 'aclarada'
  if (efecto === 'NO-PROCEDE') return 'noprocede'
  if (efecto === 'PENDIENTE-EVIDENCIA') return 'evidencia'
  return 'diagrama'
}
const forma = ref<Forma>(inicial())
const actual = computed(() => FORMAS.find(f => f.id === forma.value)!)
const texto = ref('')
const vinculada = ref('')
const efectoForma = computed(() => forma.value === 'diagrama' ? 'CAMBIO-MODELO' : 'CAMBIO-SUSTENTO')
const opcionesForma = computed(() => opciones.value.filter(o => o.efecto === efectoForma.value))
const opcion = ref(opcionesForma.value.find(o => o.recomendada)?.id || opcionesForma.value[0]?.id || '')
const candidatas = computed(() => props.resolved.filter(o => o.id !== props.item.id))
const distinta = computed(() => {
  const efecto = recomendada.value?.efecto
  if (!efecto) return false
  const mapa: Record<Forma, string> = { diagrama: 'CAMBIO-MODELO', sustento: 'CAMBIO-SUSTENTO', aclarada: 'ACLARACION', noprocede: 'NO-PROCEDE', evidencia: 'PENDIENTE-EVIDENCIA', vincular: '' }
  return mapa[forma.value] !== efecto
})
const textoVacio = computed(() => !texto.value.replace(/<[^>]+>/g, '').trim())
const listo = computed(() => {
  if (!author.value.trim()) return false
  if (forma.value === 'diagrama' || forma.value === 'sustento') return Boolean(opcion.value) || !textoVacio.value
  if (forma.value === 'vincular') return Boolean(vinculada.value)
  return !textoVacio.value
})

function elegir(id: Forma) {
  forma.value = id
  if (id === 'diagrama' || id === 'sustento') opcion.value = opcionesForma.value.find(o => o.recomendada)?.id || opcionesForma.value[0]?.id || ''
}

function confirmar() {
  if (!listo.value) return
  if (forma.value === 'diagrama' || forma.value === 'sustento') {
    emit('define', opcion.value
      ? { tipo: 'OPCION', opciones: [opcion.value], texto: textoVacio.value ? '' : texto.value, formato: 'html', vinculada_a: '' }
      : { tipo: 'MANUAL', opciones: [], texto: texto.value, formato: 'html', vinculada_a: '' })
  } else if (forma.value === 'vincular') {
    emit('define', { tipo: 'VINCULADA', opciones: [], texto: textoVacio.value ? '' : texto.value, formato: 'html', vinculada_a: vinculada.value })
  } else {
    emit('cerrar', { tipo: forma.value === 'aclarada' ? 'ACLARADA' : forma.value === 'noprocede' ? 'NO-PROCEDE' : 'PENDIENTE-EVIDENCIA', texto: texto.value })
  }
}

const dialogo = ref<HTMLElement | null>(null)
onMounted(() => dialogo.value?.querySelector<HTMLElement>('button[aria-pressed="true"]')?.focus())
</script>

<template>
  <div class="modal-backdrop modal-backdrop--top" @click.self="emit('cancel')" @keydown.esc="emit('cancel')">
    <div ref="dialogo" class="modal close-dialog" role="dialog" aria-modal="true" aria-labelledby="titulo-cierre">
      <header class="modal-header">
        <div>
          <small class="muted">{{ item.referencia || 'Diagrama completo' }}</small>
          <h2 id="titulo-cierre">¿Cómo se resolvió esta observación?</h2>
        </div>
        <button type="button" class="modal-close" aria-label="Cancelar" @click="emit('cancel')">×</button>
      </header>
      <div class="modal-body">
        <p v-if="recomendada && distinta" class="close-warning" role="note">
          La opción recomendada por Claudia era <strong>«{{ recomendada.titulo }}»</strong>. Si la cierra de otra forma, explique por qué.
        </p>
        <fieldset class="close-forms">
          <legend>Tipo de solución</legend>
          <button v-for="f in FORMAS" :key="f.id" type="button" class="close-form" :aria-pressed="forma === f.id" :style="{ borderColor: forma === f.id ? f.color : undefined }" @click="elegir(f.id)">
            <span class="close-dot" :style="{ background: f.color }" aria-hidden="true" />
            <span><strong>{{ f.titulo }}</strong><small>{{ f.ayuda }}</small></span>
          </button>
        </fieldset>
        <div v-if="(forma === 'diagrama' || forma === 'sustento') && opcionesForma.length" class="close-options">
          <span class="field-label">Opción de la propuesta</span>
          <label v-for="o in opcionesForma" :key="o.id" class="close-option">
            <input v-model="opcion" type="radio" name="opcion-cierre" :value="o.id">
            <span><strong>{{ o.id }}. {{ o.titulo }}</strong><em v-if="o.recomendada"> · recomendada</em></span>
          </label>
          <label class="close-option"><input v-model="opcion" type="radio" name="opcion-cierre" value=""><span>Otra: la describo abajo</span></label>
        </div>
        <label v-if="forma === 'vincular'">Observación resuelta que la cubre
          <select v-model="vinculada">
            <option value="">Elija una</option>
            <option v-for="o in candidatas" :key="o.id" :value="o.id">{{ o.referencia || 'Diagrama' }} · {{ o.texto.replace(/<[^>]+>/g, ' ').slice(0, 80) }}</option>
          </select>
        </label>
        <p v-if="forma === 'vincular' && !candidatas.length" class="muted">No hay observaciones resueltas en este proceso para vincular.</p>
        <label>Quién decide<input v-model="author" maxlength="100" autocomplete="name" placeholder="Nombre o equipo"></label>
        <div class="field-label">{{ actual.nota }}</div>
        <RichTextEditor v-model="texto" :label="actual.nota" placeholder="Escriba aquí" />
        <p class="close-consequence"><strong>Qué pasará:</strong> {{ actual.consecuencia }}</p>
      </div>
      <footer class="modal-footer">
        <button type="button" class="secondary-button" @click="emit('cancel')">Cancelar</button>
        <button type="button" class="primary-link" :style="{ background: actual.color }" :disabled="saving || !listo" @click="confirmar">{{ actual.boton }}</button>
      </footer>
    </div>
  </div>
</template>
