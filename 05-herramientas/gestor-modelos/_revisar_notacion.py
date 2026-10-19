"""Revisa la notacion de archivos BPMN 2.0 contra la paleta del proyecto y las buenas practicas del manual (control D5).

Uso: python _revisar_notacion.py <archivo_o_carpeta> [...]
Paleta: estandar de artefactos de modelamiento, seccion 7.3 (DEC-027); manual BPMN 2.0 (LOC-004).
Controles:
- N1 elemento o tipo de evento fuera de la paleta (por ejemplo, compuerta compleja, tareas de envio o recepcion,
  eventos de conexion, compensacion, cancelacion o multiples);
- N2 compuerta exclusiva o inclusiva que bifurca sin pregunta o con salidas sin rotulo (p. 36);
- N3 compuerta paralela que bifurca con salidas rotuladas: las ramas paralelas no llevan condicion (p. 38);
- N4 compuerta basada en eventos con menos de dos salidas o con destinos que no son eventos intermedios de captura
  (p. 74);
- N5 proceso sin evento de inicio o sin evento de fin (p. 35);
- N6 evento de borde que no esta sobre una actividad, o de error que no interrumpe (p. 90);
- N7 subproceso de evento sin un unico evento de inicio con disparador (p. 96-98);
- N8 flujo condicional que sale de una actividad, en lugar de una compuerta (fig. 3.8, p. 149);
- N9 tarea o subproceso sin nombre.
Funciona con cualquier BPMN, incluidos los exportados desde Bizagi. Requiere lxml.
"""
import glob
import os
import sys

from lxml import etree

sys.stdout.reconfigure(encoding='utf-8')
B = '{http://www.omg.org/spec/BPMN/20100524/MODEL}'
ln = lambda e: etree.QName(e).localname
MAX = 8

# Paleta vigente (seccion 7.3 del estandar). Elementos semanticos permitidos, ademas de la estructura tecnica.
PALETA = {
    'startEvent', 'endEvent', 'intermediateCatchEvent', 'intermediateThrowEvent', 'boundaryEvent',
    'task', 'userTask', 'manualTask', 'serviceTask', 'callActivity', 'subProcess',
    'exclusiveGateway', 'parallelGateway', 'inclusiveGateway', 'eventBasedGateway',
    'sequenceFlow', 'messageFlow', 'association', 'dataInputAssociation', 'dataOutputAssociation',
    'dataObject', 'dataObjectReference', 'dataStore', 'dataStoreReference', 'textAnnotation', 'group',
    'category', 'categoryValue', 'multiInstanceLoopCharacteristics', 'standardLoopCharacteristics',
    'messageEventDefinition', 'timerEventDefinition', 'conditionalEventDefinition', 'signalEventDefinition',
    'escalationEventDefinition', 'errorEventDefinition', 'terminateEventDefinition',
    'message', 'signal', 'escalation', 'error',
}
TECNICOS = {
    'definitions', 'collaboration', 'participant', 'process', 'laneSet', 'lane', 'flowNodeRef', 'documentation',
    'incoming', 'outgoing', 'property', 'sourceRef', 'targetRef', 'text', 'condition', 'conditionExpression',
    'timeDuration', 'timeDate', 'timeCycle', 'ioSpecification', 'dataInput', 'dataOutput', 'inputSet', 'outputSet',
    'dataInputRefs', 'dataOutputRefs', 'extensionElements',
}
ACTIVIDADES = {'task', 'userTask', 'manualTask', 'serviceTask', 'callActivity', 'subProcess'}
CAPTURA = {'message', 'timer', 'conditional', 'signal'}


def definiciones(e):
    return [ln(d).replace('EventDefinition', '') for d in e if isinstance(d.tag, str) and ln(d).endswith('EventDefinition')]


def revisar(ruta):
    raiz = etree.parse(ruta).getroot()
    el = {e.get('id'): e for e in raiz.iter() if isinstance(e.tag, str) and e.get('id')}
    nom = lambda e: (e.get('name') or ln(e)).replace('\n', ' ')[:50]
    h = {k: [] for k in ('N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9')}
    for e in raiz.iter():
        if not isinstance(e.tag, str) or not e.tag.startswith(B):
            continue
        t = ln(e)
        if t not in PALETA and t not in TECNICOS:
            h['N1'].append(f'{t} "{nom(e)}" no esta en la paleta')
        if t.endswith('Event'):
            defs = definiciones(e)
            if len(defs) > 1:
                h['N1'].append(f'evento multiple "{nom(e)}" ({", ".join(defs)}) no esta en la paleta')
            if e.get('parallelMultiple') == 'true':
                h['N1'].append(f'evento multiple paralelo "{nom(e)}" no esta en la paleta')
            if 'terminate' in defs and t != 'endEvent':
                h['N1'].append(f'"{nom(e)}": el evento terminal solo puede ser de fin')
        if t == 'eventBasedGateway' and e.get('eventGatewayType') == 'Parallel':
            h['N1'].append(f'compuerta basada en eventos paralela "{nom(e)}" no esta en la paleta')
        if t == 'subProcess' and e.get('triggeredByEvent') != 'true':
            h['N1'].append(f'subproceso embebido "{nom(e)}" no esta en la paleta vigente; use un subproceso de llamada')
    flujos = list(raiz.iter(B + 'sequenceFlow'))
    salidas, entradas = {}, {}
    for f in flujos:
        salidas.setdefault(f.get('sourceRef'), []).append(f)
        entradas.setdefault(f.get('targetRef'), []).append(f)
    for e in raiz.iter():
        if not isinstance(e.tag, str):
            continue
        t, i = ln(e), e.get('id')
        sal = salidas.get(i, [])
        if t in ('exclusiveGateway', 'inclusiveGateway') and len(sal) > 1:
            if not (e.get('name') or '').strip():
                h['N2'].append(f'compuerta {t} {i} bifurca sin pregunta')
            for f in sal:
                if not (f.get('name') or '').strip() and f.get('id') != e.get('default'):
                    destino = el.get(f.get('targetRef'))
                    h['N2'].append(f'salida de "{nom(e)}" hacia "{nom(destino) if destino is not None else "?"}" '
                                   'sin rotulo')
        if t == 'parallelGateway' and len(sal) > 1:
            for f in sal:
                if (f.get('name') or '').strip():
                    h['N3'].append(f'salida "{f.get("name")}" de una compuerta paralela: las ramas paralelas no '
                                   'llevan condicion')
        if t == 'eventBasedGateway':
            if len(sal) < 2:
                h['N4'].append(f'compuerta basada en eventos "{nom(e)}" con menos de dos salidas')
            for f in sal:
                d = el.get(f.get('targetRef'))
                ok = d is not None and (ln(d) == 'receiveTask' or (ln(d) == 'intermediateCatchEvent'
                                                                   and set(definiciones(d)) <= CAPTURA))
                if not ok:
                    h['N4'].append(f'"{nom(e)}": el destino "{nom(d) if d is not None else "?"}" no es un evento '
                                   'intermedio de captura')
        if t == 'boundaryEvent':
            host = el.get(e.get('attachedToRef'))
            if host is None or ln(host) not in ACTIVIDADES:
                h['N6'].append(f'evento de borde "{nom(e)}" no esta sobre una actividad')
            if 'error' in definiciones(e) and e.get('cancelActivity') == 'false':
                h['N6'].append(f'evento de error en el borde "{nom(e)}" debe interrumpir')
        if t == 'subProcess' and e.get('triggeredByEvent') == 'true':
            inicios = [s for s in e if isinstance(s.tag, str) and ln(s) == 'startEvent']
            if len(inicios) != 1 or not definiciones(inicios[0]):
                h['N7'].append(f'subproceso de evento "{nom(e)}" sin un unico evento de inicio con disparador')
        if t in ACTIVIDADES and not (e.get('name') or '').strip():
            h['N9'].append(f'{t} {i} sin nombre')
    for f in flujos:
        origen = el.get(f.get('sourceRef'))
        if f.find(B + 'conditionExpression') is not None and origen is not None and not ln(origen).endswith('Gateway'):
            h['N8'].append(f'flujo condicional desde "{nom(origen)}": use una compuerta')
    for p in raiz.iter(B + 'process'):
        nodos = [e for e in p if isinstance(e.tag, str)]
        if not any(ln(e) not in ('laneSet', 'documentation') for e in nodos):
            continue  # proceso vacio de un pool cerrado (copia para Bizagi)
        if not any(ln(e) == 'startEvent' for e in nodos):
            h['N5'].append(f'proceso "{nom(p)}" sin evento de inicio')
        if not any(ln(e) == 'endEvent' for e in nodos):
            h['N5'].append(f'proceso "{nom(p)}" sin evento de fin')
    return h


TITULOS = {'N1': 'fuera de la paleta', 'N2': 'compuertas exclusivas o inclusivas', 'N3': 'compuertas paralelas',
           'N4': 'compuertas basadas en eventos', 'N5': 'inicio y fin', 'N6': 'eventos de borde',
           'N7': 'subprocesos de evento', 'N8': 'flujos condicionales', 'N9': 'nombres'}

if __name__ == '__main__':
    archivos = []
    for a in sys.argv[1:]:
        archivos += sorted(glob.glob(os.path.join(a, '*.bpmn'))) if os.path.isdir(a) else [a]
    for f in archivos:
        h = revisar(f)
        total = sum(len(v) for v in h.values())
        print(f'D5 notacion ({os.path.basename(f)}): ' + ('sin hallazgos' if not total else f'{total} hallazgo(s)'))
        for k, v in h.items():
            v = list(dict.fromkeys(v))
            if v:
                print(f'    {k} {TITULOS[k]}: {len(v)}')
                for x in v[:MAX]:
                    print('        ' + x)
                if len(v) > MAX:
                    print(f'        … y {len(v) - MAX} mas')
