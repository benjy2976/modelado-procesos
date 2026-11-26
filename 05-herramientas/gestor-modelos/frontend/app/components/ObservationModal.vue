<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import DOMPurify from 'dompurify'
import type { components } from '~/types/api'
import { type Definicion, estadoVisual, pasosObservacion, resumenObservacion } from '~/utils/estadoObservacion'
import RichTextEditor from './RichTextEditor.vue'

// Detalle de una observación (rediseño 2026-11-26, «Responder y decidir»): la persona escribe su decisión en
// lenguaje natural y el agente la aplica (aclara, declara que no procede, corrige o deja pendiente de evidencia)
// o la devuelve con una pregunta. Los comentarios aportan al tema sin decidir y alimentan un reanálisis.
type Registro = components['schemas']['ObservacionVista']
type Trabajo = components['schemas']['TrabajoVista']
type ListadoVersiones = components['schemas']['ListadoVersiones']

const props = defineProps<{ code: string; item: Registro; jobs: Trabajo[]; saving: boolean }>()
const author = defineModel<string>('author', { required: true })
const emit = defineEmits<{
  close: []; define: [value: Definicion]; requestAnalysis: [nota: string]; reply: [texto: string]; reabrir: []; version: [numero: number]
}>()

const ALLOWED_TAGS = ['h3', 'h4', 'p', 'br', 'strong', 'b', 'em', 'i', 'u', 's', 'del', 'ul', 'ol', 'li', 'blockquote']
const rich = (content?: string | null, format?: string | null) => format === 'html'
  ? DOMPurify.sanitize(content || '', { ALLOWED_TAGS, ALLOWED_ATTR: [] })
  : DOMPurify.sanitize(content || '', { ALLOWED_TAGS: [] })
const fechaLarga = (valor?: string | null) => valor ? new Date(valor).toLocaleString('es-PE', { dateStyle: 'medium', timeStyle: 'short' }) : ''
const vacio = (html: string) => !html.replace(/<[^>]+>/g, '').trim()
const EFECTOS: Record<string, string> = {
  'CAMBIO-MODELO': 'Cambia el diagrama', 'CAMBIO-SUSTENTO': 'Explica en el sustento', DECISION: 'Decisión del equipo',
  ACLARACION: 'Aclaración', 'NO-PROCEDE': 'No procede', 'PENDIENTE-EVIDENCIA': 'Falta evidencia'
}

const visual = computed(() => estadoVisual(props.item, props.jobs))
const pasos = computed(() => pasosObservacion(props.item, visual.value))
const resumen = computed(() => resumenObservacion(props.item))
const resolucion = computed(() => props.item.resolucion || null)
const propuesta = computed(() => resolucion.value?.propuesta || null)
const abierta = computed(() => props.item.estado === 'ABIERTA')
const etapa = computed(() => props.item.etapa || 'REGISTRADA')
const decidible = computed(() => abierta.value && ['REGISTRADA', 'EN-ANALISIS', 'PROPUESTA', 'PENDIENTE-EVIDENCIA'].includes(etapa.value))
const devuelta = computed(() => decidible.value ? resolucion.value?.decisiones_devueltas?.at(-1) || null : null)
const comentarios = computed(() => props.item.respuestas || [])
const analisisActivo = computed(() => props.jobs.some(job => job.tipo === 'ANALISIS' && ['PENDIENTE', 'EN-CURSO'].includes(job.estado)))
const puedeReanalizar = computed(() => ['REGISTRADA', 'EN-ANALISIS', 'PROPUESTA'].includes(etapa.value) && abierta.value && !analisisActivo.value)

// Versión creada al aplicar esta observación: se busca por la sesión que la integró.
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

// «Responder y decidir»: atajos que rellenan el inicio de la respuesta; la persona completa el porqué.
const decision = ref('')
const editorDecision = ref(0)
const atajos = computed(() => [
  { texto: 'Es una aclaración', html: '<p><strong>Es una aclaración:</strong> </p>' },
  { texto: 'No procede', html: '<p><strong>No procede:</strong> </p>' },
  { texto: 'Falta evidencia', html: '<p><strong>Falta evidencia:</strong> </p>' },
  ...(propuesta.value?.opciones || []).map(o => ({ texto: `Aplicar opción ${o.id}`, html: `<p><strong>Aplicar la opción ${o.id}</strong> («${o.titulo}»). </p>` }))
])
function usarAtajo(html: string) {
  decision.value = html
  editorDecision.value++
}
function enviarDecision() {
  if (vacio(decision.value) || !author.value.trim()) return
  emit('define', { tipo: 'MANUAL', opciones: [], texto: decision.value, formato: 'html', vinculada_a: '' })
  decision.value = ''
  editorDecision.value++
}

const comentario = ref('')
const editorComentario = ref(0)
function enviarComentario() {
  if (vacio(comentario.value) || !author.value.trim()) return
  emit('reply', comentario.value)
  comentario.value = ''
  editorComentario.value++
}

const notaReanalisis = ref('')
function pedirReanalisis() {
  const base = comentarios.value.length ? `Reanalizar considerando los ${comentarios.value.length} comentarios del hilo.` : 'Reanalizar.'
  emit('requestAnalysis', notaReanalisis.value.trim() ? `${base} ${notaReanalisis.value.trim()}` : base)
  notaReanalisis.value = ''
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
  <div class="modal-backdrop" @click.self="emit('close')" @keydown.esc="emit('close')">
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
          <p>No hay decisión ni cambio en el modelo. Reábrala para responder y decidir.</p>
        </section>

        <section v-else-if="resolucion?.cierre || resolucion?.definicion" class="solution" :style="{ borderColor: visual.barra, background: visual.fondo }">
          <strong :style="{ color: visual.color }">{{ visual.texto }}</strong>
          <template v-if="resolucion?.cierre">
            <small>{{ resolucion.cierre.autor }} · {{ fechaLarga(resolucion.cierre.fecha) }}</small>
            <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
            <div class="rich-content" v-html="rich(resolucion.cierre.texto, resolucion.cierre.formato)" />
          </template>
          <template v-if="resolucion?.definicion">
            <small>Decisión de {{ resolucion.definicion.autor }} · {{ fechaLarga(resolucion.definicion.fecha) }}</small>
            <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
            <div v-if="resolucion.definicion.texto" class="rich-content" v-html="rich(resolucion.definicion.texto, resolucion.definicion.formato)" />
            <p v-if="resolucion.definicion.opciones?.length">Opciones elegidas: {{ resolucion.definicion.opciones.join(', ') }}</p>
          </template>
          <template v-if="resolucion?.aplicacion">
            <small>Aplicada por {{ resolucion.aplicacion.autor }} · {{ fechaLarga(resolucion.aplicacion.fecha) }}<template v-if="resolucion.aplicacion.cambios?.length"> · {{ resolucion.aplicacion.cambios.join(', ') }}</template></small>
            <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
            <div class="rich-content" v-html="rich(resolucion.aplicacion.texto, resolucion.aplicacion.formato)" />
            <button v-if="version" type="button" class="primary-link solution-version" @click="emit('version', version)">Ver la versión v{{ version }} en el diagrama</button>
          </template>
          <p v-else-if="resolucion?.definicion" class="muted">Claudia leerá la decisión y la aplicará: si es una aclaración o no procede, la cierra sin tocar el modelo; si hay que corregir, lo hace en su sesión y aquí aparecerá la versión. Si no le queda claro, le preguntará.</p>
        </section>

        <section v-if="devuelta" class="solution solution--question" role="note">
          <strong>Claudia pidió precisar la decisión</strong>
          <small>Decisión anterior de {{ devuelta.autor }}:</small>
          <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
          <div class="rich-content" v-html="rich(devuelta.texto, devuelta.formato)" />
          <small>Pregunta:</small>
          <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
          <div class="rich-content" v-html="rich(devuelta.pregunta, devuelta.pregunta_formato)" />
        </section>

        <section v-if="propuesta" class="modal-section">
          <h3>Propuesta de Claudia (referencia)</h3>
          <ul class="proposal-list">
            <li v-for="o in propuesta.opciones" :key="o.id" :class="{ 'proposal--recommended': o.recomendada }">
              <div class="proposal-head">
                <strong>{{ o.id }}. {{ o.titulo }}</strong>
                <span class="proposal-effect">{{ EFECTOS[o.efecto] || o.efecto }}</span>
                <span v-if="o.recomendada" class="proposal-badge">Recomendada</span>
              </div>
              <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
              <div class="rich-content" v-html="rich(o.detalle, o.formato)" />
            </li>
          </ul>
          <details v-if="resolucion?.analisis" class="analysis-details">
            <summary>Por qué lo propone (análisis, fuentes y alternativas)</summary>
            <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
            <div class="rich-content" v-html="rich(resolucion.analisis.texto, resolucion.analisis.formato)" />
            <p v-if="resolucion.analisis.fuentes?.length" class="muted">Fuentes: {{ resolucion.analisis.fuentes.join('; ') }}</p>
          </details>
        </section>
        <p v-else-if="analisisActivo" class="muted" role="status">Claudia está analizando esta observación.</p>

        <section v-if="decidible" class="decision-box">
          <h3>Responder y decidir</h3>
          <p class="muted">Escriba su decisión con sus palabras. Claudia la aplicará: si es una aclaración o no procede, la cierra; si hay que corregir, cambia el modelo; si falta evidencia, la deja pendiente.</p>
          <div class="decision-shortcuts" role="group" aria-label="Empezar la respuesta con">
            <button v-for="a in atajos" :key="a.texto" type="button" @click="usarAtajo(a.html)">{{ a.texto }}</button>
          </div>
          <RichTextEditor :key="`decision-${editorDecision}`" v-model="decision" label="Su decisión" placeholder="Por ejemplo: «No procede: en contrata el inventario lo hace la SGGOS…»" />
          <label>Quién decide<input v-model="author" maxlength="100" autocomplete="name" placeholder="Nombre o equipo"></label>
          <button type="button" class="primary-link" :disabled="saving || !author.trim() || !decision.replace(/<[^>]+>/g, '').trim()" @click="enviarDecision">Enviar decisión</button>
        </section>

        <section class="modal-section">
          <h3>Comentarios ({{ comentarios.length }})</h3>
          <p v-if="!comentarios.length" class="muted">Aún no hay comentarios. Los comentarios aportan al tema sin decidir; varias personas pueden comentar.</p>
          <div v-for="answer in comentarios" :key="answer.id" class="modal-reply">
            <strong>{{ answer.autor }}</strong> <small class="muted">{{ fechaLarga(answer.fecha) }}</small>
            <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
            <div class="rich-content" v-html="rich(answer.texto, answer.formato)" />
          </div>
          <div class="comment-form">
            <RichTextEditor :key="`comentario-${editorComentario}`" v-model="comentario" label="Comentario" placeholder="Aporte un dato, una duda o una fuente (no decide)" />
            <div class="comment-actions">
              <input v-model="author" maxlength="100" autocomplete="name" placeholder="Su nombre" aria-label="Autor del comentario">
              <button type="button" class="secondary-button" :disabled="saving || !author.trim() || !comentario.replace(/<[^>]+>/g, '').trim()" @click="enviarComentario">Agregar comentario</button>
            </div>
          </div>
          <div v-if="puedeReanalizar" class="reanalysis">
            <label>Nota para el reanálisis (opcional)<input v-model="notaReanalisis" maxlength="300" placeholder="Qué debería revisar de nuevo"></label>
            <button type="button" class="secondary-button" :disabled="saving || !author.trim()" @click="pedirReanalisis">{{ comentarios.length ? 'Pedir reanálisis con los comentarios' : 'Pedir análisis a Claudia' }}</button>
          </div>
        </section>

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

      <footer v-if="!abierta" class="modal-footer">
        <button type="button" class="secondary-button" :disabled="saving" @click="emit('reabrir')">Reabrir</button>
      </footer>
    </div>
  </div>
</template>
