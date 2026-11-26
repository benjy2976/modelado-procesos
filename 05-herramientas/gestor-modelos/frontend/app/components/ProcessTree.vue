<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { components } from '~/types/api'

type Nodo = components['schemas']['NodoArbol']

// counts: observaciones abiertas por código de proceso (contador del árbol).
const props = withDefaults(defineProps<{ node: Nodo; selected: string; depth?: number; counts?: Record<string, number> }>(), { depth: 0, counts: () => ({}) })
const emit = defineEmits<{ select: [codigo: string] }>()

function contains(node: Nodo, code: string): boolean {
  return node.codigo === code || node.hijos.some(child => contains(child, code))
}

const expanded = ref(props.depth === 0 || contains(props.node, props.selected))
watch(() => props.selected, code => {
  expanded.value = props.depth === 0 || contains(props.node, code)
})

function suma(node: Nodo): number {
  return node.hijos.reduce((total, child) => total + (props.counts[child.codigo] || 0) + suma(child), 0)
}
const propias = computed(() => props.counts[props.node.codigo] || 0)
// Plegado, el nodo también avisa de las abiertas de sus procesos interiores.
const interiores = computed(() => expanded.value ? 0 : suma(props.node))

function selectNode() {
  if (props.node.hijos.length) expanded.value = true
  emit('select', props.node.codigo)
}
</script>

<template>
  <div class="tree-branch">
    <div class="tree-row" :style="{ paddingLeft: `${6 + depth * 14}px` }">
      <button
        v-if="node.hijos.length"
        type="button"
        class="tree-expand"
        :aria-expanded="expanded"
        :aria-label="`${expanded ? 'Plegar' : 'Desplegar'} ${node.codigo} ${node.nombre}`"
        @click="expanded = !expanded"
      >{{ expanded ? '▾' : '▸' }}</button>
      <span v-else class="tree-expand-spacer" aria-hidden="true" />
      <button
        type="button"
        class="tree-node"
        :class="{ 'tree-node--active': selected === node.codigo }"
        :aria-current="selected === node.codigo ? 'page' : undefined"
        @click="selectNode"
      >
        <span class="tree-node__code">{{ node.codigo }}</span>
        <span class="tree-node__name">{{ node.nombre }}</span>
        <span v-if="propias" class="tab-badge tree-badge" :title="`${propias} observaciones abiertas`">{{ propias }}</span>
        <span v-else-if="interiores" class="tree-badge tree-badge--inner" :title="`${interiores} observaciones abiertas en procesos interiores`">{{ interiores }}</span>
      </button>
    </div>
    <div v-if="expanded" class="tree-children">
      <ProcessTree
        v-for="child in node.hijos"
        :key="child.codigo"
        :node="child"
        :selected="selected"
        :depth="depth + 1"
        :counts="counts"
        @select="emit('select', $event)"
      />
    </div>
  </div>
</template>
