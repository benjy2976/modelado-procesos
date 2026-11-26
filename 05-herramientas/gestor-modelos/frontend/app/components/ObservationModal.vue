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

// «Responder y decidir»: se elige una opción de Claudia, varias (si su propuesta lo permite) o una respuesta propia;
// la respuesta propia habilita el texto y lo vuelve obligatorio. Los atajos rellenan el inicio de ese texto.
const decision = ref('')
const editorDecision = ref(0)
const multiple = computed(() => propuesta.value?.seleccion === 'MULTIPLE')
const elegidas = ref<string[]>([])
const propia = ref(false)
const atajos = [
  { texto: 'Es una aclaración', html: '<p><strong>Es una aclaración:</strong> </p>' },
  { texto: 'No procede', html: '<p><strong>No procede:</strong> </p>' },
  { texto: 'Falta evidencia', html: '<p><strong>Falta evidencia:</strong> </p>' }
]
const conTexto = computed(() => propia.value || !propuesta.value)
const listaParaEnviar = computed(() => {
  if (!author.value.trim()) return false
  if (conTexto.value && vacio(decision.value)) return false
  return conTexto.value || elegidas.value.length > 0
})
function elegirUnica(id: string) {
  elegidas.value = id === 'propia' ? [] : [id]
  propia.value = id === 'propia'
}
function alternar(id: string) {
  elegidas.value = elegidas.value.includes(id) ? elegidas.value.filter(e => e !== id) : [...elegidas.value, id]
}
function usarAtajo(html: string) {
  decision.value = html
  editorDecision.value++
}
function enviarDecision() {
  if (!listaParaEnviar.value) return
  const texto = conTexto.value ? decision.value : ''
  const opciones = [...elegidas.value]
  emit('define', opciones.length
    ? { tipo: opciones.length > 1 ? 'OPCIONES' : 'OPCION', opciones, texto, formato: 'html', vinculada_a: '' }
    : { tipo: 'MANUAL', opciones: [], texto, formato: 'html', vinculada_a: '' })
  decision.value = ''
  elegidas.value = []
  propia.value = false
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

// Conversación en orden de fecha: observación, análisis de Claudia, comentarios, decisiones y aplicación.
type Clase = 'observacion' | 'comentario' | 'analisis' | 'pregunta' | 'decision' | 'resolucion'
type Mensaje = { id: string; clase: Clase; ia: boolean; autor: string; fecha: string; titulo: string; html: string; nota?: string; version?: boolean }
const esIA = (autor?: string | null) => (autor || '').trim().toLocaleLowerCase('es').startsWith('claudia')
const tituloOpciones = (ids?: string[] | null) => (ids || [])
  .map(id => { const o = propuesta.value?.opciones.find(x => x.id === id); return o ? `${o.id}. ${o.titulo}` : id })
const conversacion = computed<Mensaje[]>(() => {
  const r = resolucion.value
  const lista: Mensaje[] = [{
    id: 'observacion', clase: 'observacion', ia: esIA(props.item.autor), autor: props.item.autor, fecha: props.item.fecha,
    titulo: props.item.tipo === 'COMENTARIO' ? 'Comentario' : 'Observación', html: rich(props.item.texto, props.item.formato)
  }]
  if (r?.analisis) {
    lista.push({ id: 'analisis', clase: 'analisis', ia: true, autor: r.analisis.autor, fecha: r.analisis.fecha, titulo: 'Análisis',
      html: rich(r.analisis.texto, r.analisis.formato), nota: r.analisis.fuentes?.length ? `Fuentes: ${r.analisis.fuentes.join('; ')}` : '' })
  }
  for (const c of comentarios.value) {
    lista.push({ id: `c-${c.id}`, clase: esIA(c.autor) ? 'pregunta' : 'comentario', ia: esIA(c.autor), autor: c.autor, fecha: c.fecha, titulo: esIA(c.autor) ? 'Pregunta o nota de Claudia' : 'Comentario', html: rich(c.texto, c.formato) })
  }
  for (const [i, d] of (r?.decisiones_devueltas || []).entries()) {
    const elegidasD = tituloOpciones(d.opciones)
    lista.push({ id: `d-${i}`, clase: 'decision', ia: false, autor: d.autor, fecha: d.fecha, titulo: 'Decisión (devuelta por Claudia)',
      html: (elegidasD.length ? `<p><strong>Opciones:</strong> ${elegidasD.join('; ')}</p>` : '') + rich(d.texto, d.formato) })
  }
  if (r?.definicion) {
    const elegidasD = tituloOpciones(r.definicion.opciones)
    lista.push({ id: 'decision', clase: 'decision', ia: false, autor: r.definicion.autor, fecha: r.definicion.fecha, titulo: 'Decisión',
      html: (elegidasD.length ? `<p><strong>Opciones:</strong> ${rich(elegidasD.join('; '))}</p>` : '') + rich(r.definicion.texto, r.definicion.formato) })
  }
  if (r?.aplicacion) {
    lista.push({ id: 'aplicacion', clase: 'resolucion', ia: esIA(r.aplicacion.autor), autor: r.aplicacion.autor, fecha: r.aplicacion.fecha,
      titulo: visual.value.texto, html: rich(r.aplicacion.texto, r.aplicacion.formato),
      nota: r.aplicacion.cambios?.length ? `Cambios: ${r.aplicacion.cambios.join(', ')}` : '', version: Boolean(r.aplicacion.sesion) })
  }
  if (r?.cierre) {
    lista.push({ id: 'cierre', clase: 'resolucion', ia: false, autor: r.cierre.autor, fecha: r.cierre.fecha, titulo: visual.value.texto, html: rich(r.cierre.texto, r.cierre.formato) })
  }
  return lista.sort((a, b) => a.fecha.localeCompare(b.fecha))
})
const ETIQUETAS: Record<Clase, string> = {
  observacion: 'Observación', comentario: 'Comentario', analisis: 'Análisis de IA', pregunta: 'Pregunta de IA', decision: 'Decisión', resolucion: 'Resolución'
}
const comentando = ref(false)
const esperandoAgente = computed(() => Boolean(resolucion.value?.definicion) && !resolucion.value?.aplicacion)

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
            <span>{{ item.referencia || 'Diagrama completo' }} · {{ resumen.etiqueta }}</span>
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
        <ol class="thread" aria-label="Conversación de la observación">
          <li v-for="m in conversacion" :key="m.id" :class="['thread-message', m.ia ? 'thread-message--ia' : 'thread-message--persona']">
            <span class="thread-avatar" :aria-label="m.ia ? 'Inteligencia artificial' : 'Persona'" role="img">
              <svg v-if="m.ia" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z" /><path d="M18 15l.9 2.1L21 18l-2.1.9L18 21l-.9-2.1L15 18l2.1-.9z" /></svg>
              <svg v-else viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4" /><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7" /></svg>
            </span>
            <div :class="['thread-bubble', `thread-bubble--${m.clase}`]">
              <div class="thread-head">
                <span :class="['thread-kind', `thread-kind--${m.clase}`]">
                  <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path v-if="m.clase === 'observacion'" d="M12 3l9 16H3zM12 10v4M12 17v.5" />
                    <path v-else-if="m.clase === 'comentario'" d="M4 5h16v11H9l-5 4z" />
                    <path v-else-if="m.clase === 'analisis'" d="M10 4a6 6 0 1 0 0 12a6 6 0 0 0 0-12zM14.5 14.5L20 20" />
                    <path v-else-if="m.clase === 'pregunta'" d="M9 9a3 3 0 1 1 4 2.8c-.7.3-1 .9-1 1.7V14M12 17.5v.5" />
                    <path v-else-if="m.clase === 'decision'" d="M5 12l4 4L19 6" />
                    <path v-else d="M5 21V4h11l-2 4l2 4H5" />
                  </svg>
                  {{ ETIQUETAS[m.clase] }}
                </span>
                <strong>{{ m.autor }}</strong>
                <span v-if="m.titulo && m.titulo !== ETIQUETAS[m.clase]" class="thread-title">{{ m.titulo }}</span>
                <time>{{ fechaLarga(m.fecha) }}</time>
              </div>
              <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
              <div class="rich-content" v-html="m.html" />
              <small v-if="m.nota" class="thread-note">{{ m.nota }}</small>
              <button v-if="m.version && version" type="button" class="primary-link solution-version" @click="emit('version', version)">Ver la versión v{{ version }} en el diagrama</button>
            </div>
          </li>
          <li v-if="esperandoAgente" class="thread-message thread-message--ia thread-message--pending">
            <span class="thread-avatar" role="img" aria-label="Inteligencia artificial"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z" /></svg></span>
            <div class="thread-bubble"><em>Claudia aplicará la decisión: si es una aclaración o no procede la cierra; si hay que corregir, cambia el modelo y aquí aparecerá la versión; si no le queda clara, preguntará.</em></div>
          </li>
          <li v-else-if="analisisActivo" class="thread-message thread-message--ia thread-message--pending">
            <span class="thread-avatar" role="img" aria-label="Inteligencia artificial"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z" /></svg></span>
            <div class="thread-bubble"><em>Claudia está analizando esta observación…</em></div>
          </li>
        </ol>

        <section v-if="visual.clave === 'cerrada-sin-decision'" class="solution solution--warning" role="note">
          <strong>Se marcó como resuelta sin registrar cómo.</strong>
          <p>No hay decisión ni cambio en el modelo. Reábrala para responder y decidir.</p>
        </section>

        <section v-if="propuesta || decidible" class="proposal" :aria-label="decidible ? 'Elija cómo responder' : 'Propuesta de Claudia'">
          <h3>{{ decidible ? (multiple ? 'Propuesta de Claudia: elija una o varias opciones' : 'Propuesta de Claudia: elija una opción') : 'Propuesta de Claudia' }}</h3>
          <label v-for="o in propuesta?.opciones || []" :key="o.id" :class="['proposal-card', { 'proposal-card--on': elegidas.includes(o.id), 'proposal-card--static': !decidible }]">
            <input v-if="decidible" :type="multiple ? 'checkbox' : 'radio'" name="decision-opcion" :checked="elegidas.includes(o.id)" @change="multiple ? alternar(o.id) : elegirUnica(o.id)">
            <span class="proposal-content">
              <span class="proposal-head">
                <strong>{{ o.id }}. {{ o.titulo }}</strong>
                <span class="proposal-effect">{{ EFECTOS[o.efecto] || o.efecto }}</span>
                <span v-if="o.recomendada" class="proposal-badge">Recomendada</span>
              </span>
              <!-- eslint-disable-next-line vue/no-v-html -- HTML saneado en el servidor y con DOMPurify -->
              <span class="rich-content" v-html="rich(o.detalle, o.formato)" />
            </span>
          </label>
          <div v-if="decidible" :class="['proposal-card', 'proposal-card--own', { 'proposal-card--on': conTexto }]">
            <label class="proposal-own-head">
              <input v-if="propuesta" :type="multiple ? 'checkbox' : 'radio'" name="decision-opcion" :checked="propia" @change="multiple ? (propia = !propia) : elegirUnica('propia')">
              <strong>{{ propuesta ? `${String.fromCharCode(65 + (propuesta.opciones.length || 0))}. Respuesta propia` : 'Su respuesta' }}</strong>
              <span class="proposal-effect">{{ multiple && propuesta ? 'Se suma a las opciones elegidas' : 'Escriba su decisión' }}</span>
            </label>
            <div v-if="conTexto" class="proposal-own-body">
              <div class="decision-shortcuts" role="group" aria-label="Empezar la respuesta con">
                <button v-for="a in atajos" :key="a.texto" type="button" @click="usarAtajo(a.html)">{{ a.texto }}</button>
              </div>
              <RichTextEditor :key="`decision-${editorDecision}`" v-model="decision" label="Su respuesta (obligatoria)" placeholder="Por ejemplo: «No procede: en contrata el inventario lo hace la SGGOS…»" />
            </div>
          </div>
          <div v-if="decidible" class="proposal-submit">
            <label class="name-field">Quién decide (obligatorio)<input v-model="author" maxlength="100" autocomplete="name" placeholder="Nombre o equipo" required></label>
            <button type="button" class="primary-link" :disabled="saving || !listaParaEnviar" @click="enviarDecision">Enviar decisión</button>
          </div>
        </section>

        <section class="modal-section comment-zone">
          <button v-if="!comentando" type="button" class="secondary-button comment-open" @click="comentando = true">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v11H9l-5 4zM12 8v5M9.5 10.5h5" /></svg> Agregar comentario
          </button>
          <div v-else class="comment-form">
            <RichTextEditor :key="`comentario-${editorComentario}`" v-model="comentario" label="Comentario" placeholder="Aporte un dato, una duda o una fuente (no decide)" />
            <div class="comment-actions">
              <label class="name-field">Su nombre (obligatorio)<input v-model="author" maxlength="100" autocomplete="name" placeholder="Nombre o equipo" required></label>
              <button type="button" class="secondary-button" @click="comentando = false">Cancelar</button>
              <button type="button" class="primary-link" :disabled="saving || !author.trim() || !comentario.replace(/<[^>]+>/g, '').trim()" @click="enviarComentario(); comentando = false">Publicar comentario</button>
            </div>
          </div>
          <div v-if="puedeReanalizar" class="reanalysis">
            <label>Nota para el reanálisis (opcional)<input v-model="notaReanalisis" maxlength="300" placeholder="Qué debería revisar de nuevo"></label>
            <label class="name-field">Su nombre (obligatorio)<input v-model="author" maxlength="100" autocomplete="name" placeholder="Nombre o equipo" required></label>
            <button type="button" class="secondary-button" :disabled="saving || !author.trim()" @click="pedirReanalisis">{{ comentarios.length ? 'Pedir reanálisis con los comentarios' : 'Pedir análisis a Claudia' }}</button>
          </div>
        </section>

        <details v-if="item.historial?.length" class="modal-history">
          <summary>Historial técnico ({{ item.historial.length }})</summary>
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
        <label class="name-field">Su nombre (obligatorio)<input v-model="author" maxlength="100" autocomplete="name" placeholder="Nombre o equipo" required></label>
        <button type="button" class="secondary-button" :disabled="saving || !author.trim()" @click="emit('reabrir')">Reabrir</button>
      </footer>
    </div>
  </div>
</template>
