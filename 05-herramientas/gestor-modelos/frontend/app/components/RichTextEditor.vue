<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'

// Editor sencillo sobre contenteditable: el HTML se sanea en el servidor y de nuevo al mostrarse.
const props = defineProps<{ modelValue: string; label: string; placeholder?: string }>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
const area = ref<HTMLDivElement | null>(null)

type Accion = { command: string; value?: string; label: string; title: string; className?: string }
const acciones: Accion[] = [
  { command: 'formatBlock', value: 'h3', label: 'T', title: 'Título', className: 'tool-title' },
  { command: 'formatBlock', value: 'p', label: '¶', title: 'Párrafo' },
  { command: 'bold', label: 'B', title: 'Negrita (Ctrl+B)', className: 'tool-bold' },
  { command: 'italic', label: 'I', title: 'Cursiva (Ctrl+I)', className: 'tool-italic' },
  { command: 'underline', label: 'U', title: 'Subrayado (Ctrl+U)', className: 'tool-underline' },
  { command: 'strikeThrough', label: 'S', title: 'Tachado', className: 'tool-strike' },
  { command: 'insertUnorderedList', label: '•', title: 'Viñetas' },
  { command: 'insertOrderedList', label: '1.', title: 'Numeración' },
  { command: 'formatBlock', value: 'blockquote', label: '❝', title: 'Cita' },
  { command: 'removeFormat', label: '⌫', title: 'Quitar formato' }
]

function sync() {
  const html = area.value?.innerHTML || ''
  emit('update:modelValue', area.value?.textContent?.trim() ? html : '')
}

function apply(accion: Accion) {
  area.value?.focus()
  // execCommand está desaconsejado pero sigue disponible en los navegadores y evita una dependencia nueva.
  document.execCommand(accion.command, false, accion.value)
  sync()
}

function pastePlain(event: ClipboardEvent) {
  // Se pega texto plano para no arrastrar estilos externos; el formato se aplica con la barra.
  event.preventDefault()
  document.execCommand('insertText', false, event.clipboardData?.getData('text/plain') || '')
}

watch(() => props.modelValue, value => {
  if (area.value && value === '' && area.value.innerHTML !== '') area.value.innerHTML = ''
})
onMounted(() => { if (area.value) area.value.innerHTML = props.modelValue })
</script>

<template>
  <div class="rich-editor">
    <div class="rich-toolbar" role="toolbar" :aria-label="`Formato de ${label}`">
      <button
        v-for="accion in acciones" :key="accion.title" type="button" :class="accion.className"
        :title="accion.title" :aria-label="accion.title" @mousedown.prevent @click="apply(accion)"
      >{{ accion.label }}</button>
    </div>
    <div
      ref="area" class="rich-area" contenteditable="true" role="textbox" aria-multiline="true"
      :aria-label="label" :data-placeholder="placeholder || ''" @input="sync" @blur="sync" @paste="pastePlain"
    />
  </div>
</template>
