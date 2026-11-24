<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { navigateTo, useRoute } from '#imports'
import type { components } from '~/types/api'

type Nodo = components['schemas']['NodoArbol']
type Modelo = components['schemas']['ModeloVista']
type Fuente = components['schemas']['FuenteVista']
type DocumentoAbierto = { title: string; url: string; kind: 'markdown' | 'pdf' | 'text'; page?: number; fragment?: string; location?: string; rectangles?: number[][]; segments?: { pagina: number; rol: string; rectangulos?: number[][] }[]; anchorStatus?: string }

const tree = ref<Nodo | null>(null)
const activeCode = ref('Nivel 0')
const model = ref<Modelo | null>(null)
const selectedId = ref<string | null>(null)
const loading = ref(false)
const message = ref('')
const documentOpen = ref<DocumentoAbierto | null>(null)
const inspectorTab = ref<'detalle' | 'observaciones' | 'edicion'>('detalle')
const sidebarOpen = ref(true)
const route = useRoute()
const routeCode = computed(() => {
  const path = route.params.path
  if (!path || (Array.isArray(path) && path.length === 0)) return 'Nivel 0'
  return Array.isArray(path) && path.length === 2 && path[0] === 'procesos' ? path[1] : null
})
let loadVersion = 0

function findNode(root: Nodo | null, code: string): Nodo | null {
  if (!root) return null
  if (root.codigo === code) return root
  for (const child of root.hijos) {
    const found = findNode(child, code)
    if (found) return found
  }
  return null
}

function routeTo(root: Nodo | null, code: string): Nodo[] {
  if (!root) return []
  if (root.codigo === code) return [root]
  for (const child of root.hijos) {
    const path = routeTo(child, code)
    if (path.length) return [root, ...path]
  }
  return []
}

const activeNode = computed(() => findNode(tree.value, activeCode.value))
const breadcrumbs = computed(() => routeTo(tree.value, activeCode.value))
const selectedElement = computed(() => selectedId.value ? model.value?.elementos[selectedId.value] : undefined)
const selectedFlow = computed(() => selectedId.value ? model.value?.flujos[selectedId.value] : undefined)
const sources = computed(() => selectedElement.value ? model.value?.fuentes_visor[selectedElement.value.ref] || [] : [])
const elementNumbers = computed<Record<string, string>>(() => Object.fromEntries(
  Object.entries(model.value?.elementos || {})
    .filter(([, element]) => element.numero)
    .map(([id, element]) => [id, element.numero])
))
const childCode = computed(() => {
  const label = selectedElement.value?.nombre || ''
  const code = label.match(/^S\d+(?:\.\d+)+/)?.[0]
  return code && findNode(tree.value, code) ? code : null
})

async function displayProcess(code: string) {
  const node = findNode(tree.value, code)
  if (!node) return
  const version = ++loadVersion
  activeCode.value = code
  selectedId.value = null
  inspectorTab.value = 'detalle'
  documentOpen.value = null
  model.value = null
  message.value = ''
  loading.value = Boolean(node.bpmn)
  if (!node.bpmn) return
  try {
    const response = await fetch(`/api/procesos/${encodeURIComponent(code)}`)
    if (!response.ok) throw new Error(`El proceso ${code} aún no tiene ficha de revisión disponible.`)
    const nextModel = await response.json() as Modelo
    if (version === loadVersion) model.value = nextModel
  } catch (error) {
    if (version === loadVersion) message.value = error instanceof Error ? error.message : 'No se pudo abrir el proceso.'
  } finally {
    if (version === loadVersion) loading.value = false
  }
}

async function openProcess(code: string) {
  if (!findNode(tree.value, code)) return
  const target = code === 'Nivel 0' ? '/' : `/procesos/${encodeURIComponent(code)}`
  if (route.path === target) await displayProcess(code)
  else await navigateTo(target)
}

watch([tree, routeCode], ([root, code]) => {
  if (!root) return
  if (!code || !findNode(root, code)) {
    void navigateTo('/', { replace: true })
    return
  }
  void displayProcess(code)
}, { immediate: true })

function openProcessDocument(kind: 'tabla' | 'sustento') {
  if (!model.value) return
  documentOpen.value = {
    title: kind === 'tabla' ? 'Tabla del proceso' : 'Sustento del proceso',
    url: `/api/procesos/${encodeURIComponent(model.value.codigo)}/documentos/${kind}`,
    kind: 'markdown'
  }
}

function openSource(source: Fuente, index: number) {
  if (!model.value || !selectedElement.value) return
  const extension = source.ruta.toLowerCase()
  documentOpen.value = {
    title: source.titulo || 'Fuente registrada',
    url: `/api/procesos/${encodeURIComponent(model.value.codigo)}/fuentes/${encodeURIComponent(selectedElement.value.ref)}/${index}`,
    kind: extension.endsWith('.pdf') ? 'pdf' : extension.endsWith('.md') ? 'markdown' : 'text',
    page: source.pagina || 1,
    fragment: source.fragmento,
    location: source.ubicacion,
    rectangles: source.rectangulos,
    segments: source.tramos,
    anchorStatus: source.estado_ancla
  }
}

onMounted(async () => {
  try {
    const response = await fetch('/api/arbol')
    if (!response.ok) throw new Error('No se pudo cargar el árbol de procesos.')
    tree.value = await response.json() as Nodo
  } catch (error) {
    message.value = error instanceof Error ? error.message : 'No se pudo conectar con la API.'
  }
})
</script>

<template>
  <div class="workspace">
    <header class="topbar">
      <div class="brand-mark" aria-hidden="true">G</div>
      <div class="brand-copy">
        <span class="eyebrow">Gobierno Regional de Huánuco</span>
        <strong>Mesa de modelamiento</strong>
      </div>
      <button
        type="button"
        class="sidebar-toggle"
        aria-controls="process-sidebar"
        :aria-expanded="sidebarOpen"
        :aria-label="sidebarOpen ? 'Ocultar árbol de procesos' : 'Mostrar árbol de procesos'"
        @click="sidebarOpen = !sidebarOpen"
      >
        <span class="sidebar-toggle__icon" aria-hidden="true">☰</span>
        <span>{{ sidebarOpen ? 'Ocultar árbol' : 'Mostrar árbol' }}</span>
      </button>
      <span class="topbar-badge">Revisión de procesos</span>
    </header>

    <div class="workspace-body" :class="{ 'workspace-body--sidebar-hidden': !sidebarOpen }">
      <aside v-show="sidebarOpen" id="process-sidebar" class="sidebar" aria-label="Árbol de procesos">
        <div class="pane-heading">
          <span class="eyebrow">Explorar</span>
          <h2>Procesos</h2>
          <p>Desde el mapa institucional hasta cada proceso interior.</p>
        </div>
        <div class="tree-scroll">
          <ProcessTree v-if="tree" :node="tree" :selected="activeCode" @select="openProcess" />
          <p v-else class="muted">Cargando árbol…</p>
        </div>
      </aside>

      <main class="main-pane">
        <nav class="breadcrumbs" aria-label="Ruta del proceso">
          <template v-for="(part, index) in breadcrumbs" :key="part.codigo">
            <span v-if="index" class="breadcrumb-separator" aria-hidden="true">/</span>
            <span v-if="index === breadcrumbs.length - 1" class="breadcrumb-current" aria-current="page">
              {{ part.codigo }} <strong>{{ part.nombre }}</strong>
            </span>
            <button v-else type="button" @click="openProcess(part.codigo)">{{ part.codigo }}</button>
          </template>
          <span v-if="model" class="status-pill">BPMN disponible</span>
        </nav>

        <div v-if="message" class="notice" role="status">{{ message }}</div>
        <div v-if="loading" class="empty-state">Cargando el diagrama…</div>
        <BpmnCanvas
          v-else-if="model?.bpmn_url"
          :key="model.codigo"
          :xml-url="model.bpmn_url"
          :selected-id="selectedId"
          :numbers="elementNumbers"
          @select="selectedId = $event"
          @error="message = $event"
        />
        <div v-else class="level-landing">
          <div class="landing-intro">
            <span class="eyebrow">Mapa de navegación</span>
            <h2>{{ activeNode?.hijos.length ? 'Seleccione un proceso interior' : 'Sin diagrama publicado' }}</h2>
            <p v-if="activeNode?.hijos.length">Estos niveles se presentan como enlaces hasta que tengan un modelo BPMN propio.</p>
            <p v-else>Este proceso aún no tiene un diagrama disponible en la mesa de revisión.</p>
          </div>
          <div class="process-cards">
            <button
              v-for="child in activeNode?.hijos || []"
              :key="child.codigo"
              type="button"
              class="process-card"
              @click="openProcess(child.codigo)"
            >
              <span class="process-card__code">{{ child.codigo }}</span>
              <strong>{{ child.nombre }}</strong>
              <span class="process-card__footer">{{ child.bpmn ? 'Ver diagrama' : 'Explorar nivel' }} <span aria-hidden="true">→</span></span>
            </button>
          </div>
        </div>
      </main>

      <aside class="inspector" aria-label="Detalle y sustento">
        <div class="pane-heading inspector-heading">
          <span class="eyebrow">Inspector</span>
          <h2>{{ inspectorTab === 'observaciones' ? 'Observaciones' : inspectorTab === 'edicion' ? 'Edición en copia' : selectedElement ? selectedElement.nombre : selectedFlow ? 'Flujo seleccionado' : 'Detalle del proceso' }}</h2>
          <p>{{ inspectorTab === 'observaciones' ? 'Registre, responda y organice la revisión.' : inspectorTab === 'edicion' ? 'Copia recuperable, diff y validación.' : selectedElement ? `Caja ${selectedElement.numero || selectedElement.ref}` : 'Seleccione una caja o flujo para consultar su descripción.' }}</p>
        </div>
        <div v-if="model" class="inspector-tabs" role="tablist" aria-label="Panel de revisión">
          <button type="button" role="tab" :aria-selected="inspectorTab === 'detalle'" :class="{ active: inspectorTab === 'detalle' }" @click="inspectorTab = 'detalle'">Detalle y sustento</button>
          <button type="button" role="tab" :aria-selected="inspectorTab === 'observaciones'" :class="{ active: inspectorTab === 'observaciones' }" @click="inspectorTab = 'observaciones'">Observaciones</button>
          <button type="button" role="tab" :aria-selected="inspectorTab === 'edicion'" :class="{ active: inspectorTab === 'edicion' }" @click="inspectorTab = 'edicion'">Editar copia</button>
        </div>
        <div class="inspector-scroll">
          <ObservationsPanel v-if="model && inspectorTab === 'observaciones'" :code="model.codigo" :element-id="selectedId" :reference="selectedElement?.ref || ''" />
          <ModelEditPanel v-else-if="model && inspectorTab === 'edicion'" :code="model.codigo" @integrated="openProcess(model.codigo)" />
          <template v-else-if="selectedElement">
            <dl class="detail-list">
              <div><dt>ID de tabla</dt><dd>{{ selectedElement.ref }}</dd></div>
              <div><dt>Tipo</dt><dd>{{ selectedElement.tipo }}</dd></div>
              <div v-if="selectedElement.carril"><dt>Responsable / carril</dt><dd>{{ selectedElement.carril }}</dd></div>
              <div v-if="selectedElement.plazo"><dt>Plazo</dt><dd>{{ selectedElement.plazo }}</dd></div>
              <div v-if="selectedElement.documentos"><dt>Documentos</dt><dd>{{ selectedElement.documentos }}</dd></div>
              <div v-if="selectedElement.anotacion"><dt>Descripción</dt><dd>{{ selectedElement.anotacion }}</dd></div>
              <div v-if="selectedElement.fuente"><dt>Fuente registrada</dt><dd>{{ selectedElement.fuente }}</dd></div>
            </dl>
            <button v-if="childCode" class="primary-link" type="button" @click="openProcess(childCode)">
              Abrir proceso interior {{ childCode }} <span aria-hidden="true">→</span>
            </button>
            <div v-if="sources.length" class="source-group">
              <h3>Documentos de sustento</h3>
              <button v-for="(source, index) in sources" :key="`${source.ruta}-${index}`" type="button" class="source-button" @click="openSource(source, index)">
                <strong>{{ source.titulo || 'Fuente registrada' }}</strong>
                <span>{{ source.pagina ? `Página ${source.pagina}` : 'Documento' }}{{ source.ubicacion ? ` · ${source.ubicacion}` : '' }}</span>
              </button>
            </div>
          </template>
          <template v-else-if="selectedFlow">
            <dl class="detail-list">
              <div v-for="(value, key) in selectedFlow" :key="key"><dt>{{ key }}</dt><dd>{{ value }}</dd></div>
            </dl>
          </template>
          <div v-else class="inspector-empty">
            <span class="inspector-empty__icon" aria-hidden="true">◇</span>
            <strong>El sustento empieza en cada elemento.</strong>
            <p>Haga clic en una caja del diagrama. La selección mostrará su responsable, plazo, documentos y fuente registrada.</p>
          </div>
          <div v-if="model" class="process-documents">
            <h3>Documentación del proceso</h3>
            <button type="button" @click="openProcessDocument('tabla')">Ver tabla estructurada</button>
            <button type="button" @click="openProcessDocument('sustento')">Ver sustento</button>
          </div>
        </div>
      </aside>
    </div>
    <DocumentModal v-if="documentOpen" v-bind="documentOpen" @close="documentOpen = null" />
  </div>
</template>
