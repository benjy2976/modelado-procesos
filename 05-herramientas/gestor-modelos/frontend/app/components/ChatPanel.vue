<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import DOMPurify from 'dompurify'
import MarkdownIt from 'markdown-it'

// Chat con el agente mesa-chat de OpenClaw (DEC-068) a través de la API y el relevo; respuesta en streaming (SSE).
const props = defineProps<{ code: string; reference: string; elementName: string }>()

type Mensaje = { rol: 'usuario' | 'asistente' | 'error'; texto: string }
const markdown = new MarkdownIt({ html: false, linkify: true })
const configurado = ref<boolean | null>(null)
const mensajes = ref<Mensaje[]>([])
const borrador = ref('')
const enviando = ref(false)
const lista = ref<HTMLElement | null>(null)

const claveConversacion = computed(() => `mesa.chat.${props.code}`)
const conversacion = ref('')

function nuevaConversacion() {
  const aleatorio = Math.random().toString(36).slice(2, 10)
  conversacion.value = `M-${props.code}-${Date.now().toString(36)}-${aleatorio}`
  sessionStorage.setItem(claveConversacion.value, conversacion.value)
  mensajes.value = []
}

function cargarConversacion() {
  conversacion.value = sessionStorage.getItem(claveConversacion.value) || ''
  if (!conversacion.value) nuevaConversacion()
  mensajes.value = []
}

onMounted(async () => {
  cargarConversacion()
  try {
    const respuesta = await fetch('/api/chat/estado')
    configurado.value = respuesta.ok ? Boolean((await respuesta.json()).configurado) : false
  } catch {
    configurado.value = false
  }
})
watch(() => props.code, cargarConversacion)

function html(texto: string) {
  return DOMPurify.sanitize(markdown.render(texto))
}

async function bajar() {
  await nextTick()
  lista.value?.scrollTo({ top: lista.value.scrollHeight })
}

async function enviar() {
  const texto = borrador.value.trim()
  if (!texto || enviando.value) return
  borrador.value = ''
  enviando.value = true
  mensajes.value.push({ rol: 'usuario', texto })
  const respuesta: Mensaje = { rol: 'asistente', texto: '' }
  mensajes.value.push(respuesta)
  await bajar()
  try {
    const pedido = await fetch(`/api/procesos/${encodeURIComponent(props.code)}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
      body: JSON.stringify({
        conversacion: conversacion.value,
        mensaje: texto,
        contexto: { caja: props.reference || null, nombre: props.elementName || null }
      })
    })
    if (!pedido.ok || !pedido.body) {
      const detalle = await pedido.json().catch(() => null) as { error?: { message?: string } } | null
      throw new Error(detalle?.error?.message || `El chat respondió ${pedido.status}`)
    }
    const lector = pedido.body.getReader()
    const decodificador = new TextDecoder()
    let resto = ''
    for (;;) {
      const { done, value } = await lector.read()
      if (done) break
      resto += decodificador.decode(value, { stream: true })
      const lineas = resto.split('\n')
      resto = lineas.pop() || ''
      for (const linea of lineas) {
        if (!linea.startsWith('data:')) continue
        const dato = linea.slice(5).trim()
        if (!dato || dato === '[DONE]') continue
        let trozo: { choices?: { delta?: { content?: string } }[]; error?: { message?: string } }
        try {
          trozo = JSON.parse(dato)
        } catch {
          continue // Una línea SSE incompleta o ajena al formato se ignora; el texto acumulado sigue válido.
        }
        if (trozo.error) throw new Error(`El agente no pudo responder: ${trozo.error.message || 'error del Gateway'}`)
        respuesta.texto += trozo.choices?.[0]?.delta?.content || ''
      }
      await bajar()
    }
    if (!respuesta.texto) respuesta.texto = '_(sin respuesta)_'
  } catch (causa) {
    mensajes.value.pop()
    mensajes.value.push({ rol: 'error', texto: causa instanceof Error ? causa.message : 'No se pudo enviar el mensaje.' })
  } finally {
    enviando.value = false
    await bajar()
  }
}

function teclado(evento: KeyboardEvent) {
  if (evento.key === 'Enter' && !evento.shiftKey) {
    evento.preventDefault()
    void enviar()
  }
}
</script>

<template>
  <div class="chat-panel">
    <p v-if="configurado === false" class="muted">El asistente no está configurado en este servidor: falta el relevo hacia OpenClaw.</p>
    <template v-else>
      <div class="chat-toolbar">
        <small class="muted">{{ reference ? `Contexto: caja ${reference}` : 'Contexto: diagrama completo' }}</small>
        <button type="button" class="secondary-button" :disabled="enviando" @click="nuevaConversacion">Nueva conversación</button>
      </div>
      <div ref="lista" class="chat-messages" aria-live="polite">
        <p v-if="!mensajes.length" class="muted">Pregunte o pida una variación del modelo. El asistente prepara los cambios en una copia; usted los revisa y aplica en «Editar copia».</p>
        <div v-for="(mensaje, index) in mensajes" :key="index" class="chat-message" :class="`chat-message--${mensaje.rol}`">
          <!-- eslint-disable-next-line vue/no-v-html -- markdown sin HTML, saneado con DOMPurify -->
          <div v-if="mensaje.rol === 'asistente'" class="rich-content" v-html="html(mensaje.texto || '…')" />
          <p v-else>{{ mensaje.texto }}</p>
        </div>
      </div>
      <div class="chat-input">
        <textarea v-model="borrador" rows="3" maxlength="8000" placeholder="Escriba su mensaje (Enter envía, Mayús+Enter salto de línea)" :disabled="enviando" @keydown="teclado" />
        <button type="button" class="primary-link" :disabled="enviando || !borrador.trim()" @click="enviar">{{ enviando ? 'Respondiendo…' : 'Enviar' }}</button>
      </div>
    </template>
  </div>
</template>
