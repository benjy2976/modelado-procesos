// Misma paleta visual del visor HTML anterior (renderizar_bpmn.py: ESTILO).
// Solo colorea la copia en memoria que recibe bpmn-js; no cambia el BPMN maestro.
const palette: Record<string, readonly [string, string]> = {
  startEvent: ['#E6FF97', '#62A716'],
  endEvent: ['#EEAAAA', '#A23030'],
  intermediateCatchEvent: ['#FFFFE0', '#A6A600'],
  intermediateThrowEvent: ['#FFFFE0', '#A6A600'],
  boundaryEvent: ['#FFFFE0', '#A6A600'],
  task: ['#ECEFFF', '#03689A'],
  userTask: ['#ECEFFF', '#03689A'],
  manualTask: ['#ECEFFF', '#03689A'],
  serviceTask: ['#ECEFFF', '#03689A'],
  sendTask: ['#ECEFFF', '#03689A'],
  receiveTask: ['#ECEFFF', '#03689A'],
  scriptTask: ['#ECEFFF', '#03689A'],
  businessRuleTask: ['#ECEFFF', '#03689A'],
  callActivity: ['#ECEFFF', '#03689A'],
  subProcess: ['#ECEFFF', '#03689A'],
  exclusiveGateway: ['#FFFF99', '#A6A600'],
  parallelGateway: ['#FFFF99', '#A6A600'],
  inclusiveGateway: ['#FFFF99', '#A6A600'],
  eventBasedGateway: ['#FFFF99', '#A6A600'],
  complexGateway: ['#FFFF99', '#A6A600']
}

const diagramNamespace = 'http://www.omg.org/spec/BPMN/20100524/DI'
const colorNamespace = 'http://www.omg.org/spec/BPMN/non-normative/color/1.0'

export function colorizeBpmn(xml: string): string {
  const document = new DOMParser().parseFromString(xml, 'application/xml')
  if (document.querySelector('parsererror')) throw new Error('El BPMN no contiene XML válido.')

  const types = new Map(
    [...document.querySelectorAll('[id]')].map(element => [element.getAttribute('id'), element.localName])
  )
  for (const shape of document.getElementsByTagNameNS(diagramNamespace, 'BPMNShape')) {
    const style = palette[types.get(shape.getAttribute('bpmnElement')) || '']
    if (!style) continue
    shape.setAttributeNS(colorNamespace, 'color:background-color', style[0])
    shape.setAttributeNS(colorNamespace, 'color:border-color', style[1])
    let label = [...shape.children].find(element => element.namespaceURI === diagramNamespace && element.localName === 'BPMNLabel')
    if (!label) {
      label = document.createElementNS(diagramNamespace, 'bpmndi:BPMNLabel')
      shape.appendChild(label)
    }
    label.setAttributeNS(colorNamespace, 'color:color', '#000000')
  }
  return new XMLSerializer().serializeToString(document)
}

type BpmnDefinition = { $type: string }
type BpmnStartEvent = { $type: string; isInterrupting?: boolean; eventDefinitions?: BpmnDefinition[] }
type BpmnElement = {
  businessObject?: { $type: string; triggeredByEvent?: boolean; flowElements?: BpmnStartEvent[] }
  di?: { isExpanded?: boolean }
}
export type BpmnRegistry = {
  get: (id: string) => BpmnElement | undefined
  getGraphics: (element: BpmnElement) => Element | null
  filter: (predicate: (element: BpmnElement) => boolean) => BpmnElement[]
}

function svg(name: string, attributes: Record<string, string>): SVGElement {
  const element = document.createElementNS('http://www.w3.org/2000/svg', name)
  for (const [key, value] of Object.entries(attributes)) element.setAttribute(key, value)
  return element
}

function strokePath(path: string, color: string, width = '1.5'): SVGElement {
  return svg('path', { d: path, fill: 'none', stroke: color, 'stroke-width': width, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' })
}

// El visor anterior agrega el evento disparador en subprocesos de evento contraídos.
// bpmn-js no lo dibuja en la esquina superior izquierda; este marcador conserva esa lectura.
export function markEventSubprocesses(registry: BpmnRegistry): void {
  const subprocesses = registry.filter(element => {
    const object = element.businessObject
    return object?.$type === 'bpmn:SubProcess' && object.triggeredByEvent === true && element.di?.isExpanded === false
  })
  for (const subprocess of subprocesses) {
    const start = subprocess.businessObject?.flowElements?.find(element => element.$type === 'bpmn:StartEvent')
    const definition = start?.eventDefinitions?.[0]
    const visual = registry.getGraphics(subprocess)?.querySelector('.djs-visual')
    if (!start || !definition || !visual || visual.querySelector('[data-marker="event-subprocess-trigger"]')) continue

    const rectangle = visual.querySelector('rect')
    const color = rectangle?.style.stroke || rectangle?.getAttribute('stroke') || '#03689A'
    const fill = rectangle?.style.fill || rectangle?.getAttribute('fill') || '#FFFFFF'
    const group = svg('g', { transform: 'translate(8 8) scale(0.62)', 'data-marker': 'event-subprocess-trigger', 'pointer-events': 'none' })
    group.appendChild(svg('circle', {
      cx: '18', cy: '18', r: '16', fill, stroke: color, 'stroke-width': '2',
      'stroke-dasharray': start.isInterrupting === false ? '4 3' : 'none'
    }))

    if (definition.$type === 'bpmn:MessageEventDefinition') {
      group.appendChild(strokePath('M8.5 11.3 L8.5 23.9 L27.4 23.9 L27.4 11.3 Z M8.5 11.3 L18 16.7 L27.4 11.3', color))
    } else if (definition.$type === 'bpmn:TimerEventDefinition') {
      group.appendChild(svg('circle', { cx: '18', cy: '18', r: '10.5', fill: 'none', stroke: color, 'stroke-width': '1.7' }))
      group.appendChild(strokePath('M18 18 L20.25 10.5 M18 18 L23.25 19.5', color, '1.7'))
      for (let angle = 0; angle < 360; angle += 30) {
        group.appendChild(svg('path', {
          d: 'M18 25.5 L18 27.5', transform: `rotate(${angle} 18 18)`, fill: 'none',
          stroke: color, 'stroke-width': '1', 'stroke-linecap': 'round'
        }))
      }
    } else if (definition.$type === 'bpmn:ConditionalEventDefinition') {
      group.appendChild(strokePath(
        'M10.5 8.5 L25 8.5 L25 26.5 L10.5 26.5 Z ' +
        'M12.5 11.5 L23 11.5 M12.5 14.5 L23 14.5 M12.5 17.5 L23 17.5 ' +
        'M12.5 20.5 L23 20.5 M12.5 23.5 L23 23.5', color, '1.2'
      ))
    } else {
      continue
    }
    visual.appendChild(group)
  }
}
