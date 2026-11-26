<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import DOMPurify from 'dompurify'
import type { components } from '~/types/api'
import { estadoVisual, pasosObservacion, resumenObservacion } from '~/utils/estadoObservacion'
import CloseDialog, { type Cierre } from './CloseDialog.vue'
import ResolutionPanel, { type Definicion } from './ResolutionPanel.vue'
import RichTextEditor from './RichTextEditor.vue'

// Detalle de una observación en ventana modal (rediseño 2026-11-26): etapas, pregunta, decisión y cómo se resolvió.
type Registro = components['schemas']['ObservacionVista']
type Trabajo = components['schemas']['TrabajoVista']
type ListadoVersiones = components['schemas']['ListadoVersiones']

const props = defineProps<{ code: string; item: Registro; jobs: Trabajo[]; resolved: Registro[]; saving: boolean }>()
const author = defineModel<string>('author', { required: true })
const emit = defineEmits<{
  close: []; define: [value: Definicion]; requestAnalysis: [nota: string]; reply: [texto: string]
  cerrar: [value: Cierre]; reabrir: []; version: [numero: number]
}>()

const ALLOWED_TAGS = ['h3', 'h4', 'p', 'br', 'strong', 'b', 'em', 'i', 'u', 's', 'del', 'ul', 'ol', 'li', 'blockquote']
const rich = (content?: string | null, format?: string | null) => format === 'html'
  ? DOMPurify.sanitize(content || '', { ALLOWED_TAGS, ALLOWED_ATTR: [] })
  : DOMPurify.sanitize(content || '', { ALLOWED_TAGS: [] })
const fechaLarga = (valor?: string | null) => valor ? new Date(valor).toLocaleString('es-PE', { dateStyle: 'medium', timeStyle: 'short' }) : ''

const visual = computed(() => estadoVisual(props.item, props.jobs))
const pasos = computed(() => pasosObservacion(props.item, visual.value))
const resumen = computed(() => resumenObservacion(props.item))
const resolucion = computed(() => props.item.resolucion || null)
const abierta = computed(() => props.item.estado === 'ABIERTA')
const decidible = computed(() => abierta.value && ['REGISTRADA', 'EN-ANALISIS', 'PROPUESTA', 'PENDIENTE-EVIDENCIA'].includes(props.item.etapa || 'REGISTRADA'))
const elegidas = computed(() => (resolucion.value?.definicion?.opciones || [])
  .map(id => resolucion.value?.propuesta?.opciones.find(o => o.id === id)).filter(Boolean))

// Versión creada por la aplicación de esta observación (plan B): se busca por la sesión que la integró.
const version = ref<number | null>(null)
async function buscarVersion() {
  version.value = null
  const sesion = resolucion.value?.aplicacion?.sesion
  if (!sesion) return
  try {
    const respuesta = await fetch(`/api/procesos/${encodeURIComponent(props.code)}/versiones`)
    if (!respuesta.ok) return
    version.value = (await respuesta.json() as ListadoVersiones).versiones.find(v => v.sesion === sesion)?.numero ?? null
  } catch {
    version.value = null
  }
}

const respondiendo = ref(false)
const respuesta = ref('')
const cerrando = ref(false)
function enviarRespuesta() {
  if (!respuesta.value.replace(/<[^>]+>/g, '').trim()) return
  emit('reply', respuesta.value)
  respuesta.value = ''
  respondiendo.value = false
}

const modal = ref<HTMLElement | null>(null)
onMounted(async () => {
  void buscarVersion()
  await nextTick()
  modal.value?.querySelector<HTMLElement>('.modal-close')?.focus()
})
watch(() => props.item.id, () => { void buscarVersion() })
</script>

<template>
  <div class="modal-backdrop" @click.self="emit('close')" @keydown.esc="cerrando ? (cerrando = false) : emit('close')">
    <div ref="modal" class="modal observation-modal" role="dialog" aria-modal="true" aria-labelledby="titulo-observacion">
      <header class="modal-header">
        <div class="modal-heading">
          <div class="modal-meta">
            <span>{{ item.referencia || 'Diagrama completo' }} · {{ resumen.etiqueta }} · {{ item.autor }}, {{ fechaLarga(item.fecha) }}</span>
            <span class="state-chip" :style="{ color: visual.color, background: visual.fondo }">{{ visual.texto }}</span>
          </div>
          <h2 id="titulo-observacion">{{ resumen.titulo }}</h2>
        </div>
        <button type="button" class="modal-close" aria-label="Cerrar" @click="emit('close')">×</button>
      </header>

      <ol class="stage-steps" aria-label="Etapas de la observación">
        <li v-for="paso in pasos" :key="paso.nombre" :class="`stage-step stage-step--${paso.estado}`">
          <span class="stage-bar" aria-hidden="true" />
          <strong>{{ paso.nombre }}</strong>
          <small>{{ paso.detalle }}</small>
        </li>
      </ol>

      <div class="modal-body">
        <section class="modal-section">
          <h3>La observación</h3>
          <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
          <div class="rich-content" v-html="rich(item.texto, item.formato)" />
        </section>

        <section v-if="visual.clave === 'cerrada-sin-decision'" class="solution solution--warning" role="note">
          <strong>Se marcó como resuelta sin registrar cómo.</strong>
          <p>No hay opción elegida, respuesta ni cambio en el modelo. Si hacía falta un cambio, reábrala y ciérrela con decisión.</p>
        </section>

        <section v-else-if="resolucion?.cierre" class="solution" :style="{ borderColor: visual.barra, background: visual.fondo }">
          <strong :style="{ color: visual.color }">{{ visual.texto }}</strong>
          <small>{{ resolucion.cierre.autor }} · {{ fechaLarga(resolucion.cierre.fecha) }}</small>
          <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
          <div class="rich-content" v-html="rich(resolucion.cierre.texto, resolucion.cierre.formato)" />
        </section>

        <section v-else-if="resolucion?.definicion" class="solution" :style="{ borderColor: visual.barra, background: visual.fondo }">
          <strong :style="{ color: visual.color }">{{ visual.texto }}</strong>
          <small>Definida por {{ resolucion.definicion.autor }} · {{ fechaLarga(resolucion.definicion.fecha) }}</small>
          <ul v-if="elegidas.length" class="solution-options"><li v-for="o in elegidas" :key="o!.id">{{ o!.id }}. {{ o!.titulo }}</li></ul>
          <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
          <div v-if="resolucion.definicion.texto" class="rich-content" v-html="rich(resolucion.definicion.texto, resolucion.definicion.formato)" />
          <p v-if="resolucion.definicion.vinculada_a">Vinculada a {{ resolucion.definicion.vinculada_a.referencia || 'otra observación' }}.</p>
          <template v-if="resolucion.aplicacion">
            <small>Aplicada por {{ resolucion.aplicacion.autor }} · {{ fechaLarga(resolucion.aplicacion.fecha) }}<template v-if="resolucion.aplicacion.cambios?.length"> · {{ resolucion.aplicacion.cambios.join(', ') }}</template></small>
            <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
            <div class="rich-content" v-html="rich(resolucion.aplicacion.texto, resolucion.aplicacion.formato)" />
            <button v-if="version" type="button" class="primary-link solution-version" @click="emit('version', version)">Ver la versión v{{ version }} en el diagrama</button>
          </template>
          <p v-else class="muted">El agente aplicará lo definido en su propia sesión; aquí aparecerá la versión resultante.</p>
        </section>

        <ResolutionPanel
          v-if="decidible || (abierta && !resolucion?.definicion)"
          :item="item" :resolved="resolved" :saving="saving" :jobs="jobs"
          @define="emit('define', $event)" @request-analysis="emit('requestAnalysis', $event)"
        />

        <section v-if="item.respuestas?.length" class="modal-section">
          <h3>Respuestas</h3>
          <div v-for="answer in item.respuestas" :key="answer.id" class="modal-reply">
            <strong>{{ answer.autor }}</strong> <small class="muted">{{ fechaLarga(answer.fecha) }}</small>
            <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
            <div class="rich-content" v-html="rich(answer.texto, answer.formato)" />
          </div>
        </section>
        <div v-if="respondiendo" class="reply-form">
          <label>Autor o equipo<input v-model="author" maxlength="100" autocomplete="name" placeholder="Nombre o equipo"></label>
          <RichTextEditor v-model="respuesta" label="Respuesta" placeholder="Escriba una respuesta" />
          <button type="button" class="primary-link" :disabled="saving || !author.trim()" @click="enviarRespuesta">Guardar respuesta</button>
        </div>

        <details v-if="item.historial?.length" class="modal-history">
          <summary>Historial ({{ item.historial.length }})</summary>
          <ul>
            <li v-for="(event, index) in item.historial" :key="index">
              {{ event.accion }}<template v-if="event.version"> v{{ event.version }}</template> · {{ event.autor || event.estado || '' }} · {{ fechaLarga(event.fecha) }}<template v-if="event.motivo"> · {{ event.motivo }}</template>
              <details v-if="event.texto_anterior" class="previous-text">
                <summary>Texto anterior</summary>
                <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
                <div class="rich-content" v-html="rich(event.texto_anterior, event.formato_anterior)" />
              </details>
            </li>
          </ul>
        </details>
      </div>

      <footer class="modal-footer">
        <button type="button" class="secondary-button" @click="respondiendo = !respondiendo">Responder</button>
        <button v-if="decidible" type="button" class="primary-link" @click="cerrando = true">Cerrar con decisión</button>
        <button v-if="!abierta" type="button" class="secondary-button" :disabled="saving" @click="emit('reabrir')">Reabrir</button>
      </footer>
    </div>
    <CloseDialog
      v-if="cerrando" v-model:author="author" :item="item" :resolved="resolved" :saving="saving"
      @cancel="cerrando = false" @define="cerrando = false; emit('define', $event)" @cerrar="cerrando = false; emit('cerrar', $event)"
    />
  </div>
</template>
