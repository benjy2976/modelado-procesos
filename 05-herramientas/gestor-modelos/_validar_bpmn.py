"""Valida archivos BPMN 2.0 del proyecto (guía 07_, Parte D, controles D1 a D3).

Uso: python _validar_bpmn.py <archivo_o_carpeta> [...] [--pm4py]
- D1 Estructura: esquema XSD oficial de la OMG (xsd_bpmn20/BPMN20.xsd, idéntico a https://www.omg.org/spec/BPMN/20100501/).
Origen: proyecto de la directiva SGE (guía 07_); incorporado al gestor de modelos por DEC-025.
- D2 Referencias: referencias rotas, flujos de mensaje dentro de un mismo proceso, secuencias que cruzan procesos,
  nodos fuera de carril.
- D3 Bloqueos y terminación (juego de tokens con la semántica BPMN del libro, guía 07_ B1 a B9), sobre toda la
  colaboración: los flujos de mensaje entre nodos se recorren como flujos; un mensaje hacia un pool cerrado se consume;
  cada evento de inicio y cada mensaje que llega desde un pool cerrado abre un escenario, y en cada escenario se
  recorren todos los estados alcanzables. Informa bloqueos (tokens detenidos, p. ej., una compuerta paralela
  que espera una entrada que no llega), estados desde los que ya no se puede terminar, acumulación de tokens y
  elementos que nunca se ejecutan. Admite terminación implícita (cada token se consume en su evento de fin).
  Antes se resuelven los pares de enlaces y las actividades de llamada pasan a tareas. Informa además los pools sin
  evento de inicio y los elementos sin llegada (p. ej., un enlace sin pareja).
- D3b (opcional, --pm4py): contraste con pm4py (red de Petri, soundness de workflow net). pm4py exige un único token
  final, por lo que marca como error las ramas paralelas que terminan en eventos de fin distintos, aunque en BPMN
  sea válido.
Requiere lxml; pm4py solo para --pm4py (pip install --user pm4py).
"""
import copy
import glob
import io
import os
import sys
import warnings
from lxml import etree

sys.stdout.reconfigure(encoding='utf-8')
warnings.filterwarnings('ignore')
B = '{http://www.omg.org/spec/BPMN/20100524/MODEL}'
XSD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xsd_bpmn20', 'BPMN20.xsd')
schema = etree.XMLSchema(etree.parse(XSD))
NODOS = ('task', 'callActivity', 'subProcess', 'startEvent', 'endEvent', 'intermediateCatchEvent',
         'intermediateThrowEvent', 'boundaryEvent', 'exclusiveGateway', 'parallelGateway', 'inclusiveGateway',
         'eventBasedGateway', 'complexGateway', 'userTask', 'manualTask', 'serviceTask', 'sendTask', 'receiveTask',
         'scriptTask', 'businessRuleTask')
DECISION = ('exclusiveGateway', 'eventBasedGateway', 'inclusiveGateway', 'complexGateway')
ln = lambda e: etree.QName(e).localname


def nombre(e):
    return (e.get('name') or ln(e)).replace('\n', ' ')


def d2(root):
    ids = {e.get('id'): e for e in root.iter() if isinstance(e.tag, str) and e.get('id')}
    probs = []
    for e in root.iter():
        if not isinstance(e.tag, str):
            continue
        for a in ('sourceRef', 'targetRef', 'attachedToRef', 'processRef', 'bpmnElement', 'dataObjectRef',
                  'dataStoreRef', 'categoryValueRef'):
            if e.get(a) and e.get(a) not in ids:
                probs.append(f'referencia rota {a}={e.get(a)}')
    for t in ('sourceRef', 'targetRef', 'flowNodeRef'):
        for e in root.iter(B + t):
            if e.text not in ids:
                probs.append(f'referencia rota {t}={e.text}')
    owner = {}
    for p in root.iter(B + 'process'):
        for e in p.iter():
            if isinstance(e.tag, str) and e.get('id'):
                owner[e.get('id')] = p.get('id')
    part = {pp.get('id'): pp.get('processRef') for pp in root.iter(B + 'participant')}
    proc = lambda i: part[i] if i in part else owner.get(i)
    for m in root.iter(B + 'messageFlow'):
        if proc(m.get('sourceRef')) is not None and proc(m.get('sourceRef')) == proc(m.get('targetRef')):
            probs.append(f'flujo de mensaje dentro del mismo proceso: {m.get("name")}')
    for s in root.iter(B + 'sequenceFlow'):
        if owner.get(s.get('sourceRef')) != owner.get(s.get('targetRef')):
            probs.append(f'flujo de secuencia que cruza procesos: {s.get("id")}')
    for p in root.iter(B + 'process'):
        if p.find(B + 'laneSet') is None:
            continue
        en_carril = {x.text for x in p.iter(B + 'flowNodeRef')}
        for e in p:
            if ln(e) in NODOS and e.get('id') not in en_carril:
                probs.append(f'nodo sin carril: {nombre(e)}')
    return probs


def proceso_simple(p):
    """Copia del proceso como definición independiente, sin carriles ni datos, con enlaces resueltos."""
    q = copy.deepcopy(p)
    for e in list(q):
        if ln(e) in ('laneSet', 'dataObject', 'dataObjectReference', 'dataStoreReference', 'textAnnotation',
                     'association', 'group'):
            q.remove(e)
        elif ln(e) == 'subProcess' and e.get('triggeredByEvent') == 'true':
            # un subproceso de evento se activa por su disparador mientras el proceso está activo: no forma parte
            # del recorrido del flujo principal
            q.remove(e)
    for e in q.iter():
        if isinstance(e.tag, str):
            for ch in list(e):
                if ln(ch) in ('dataInputAssociation', 'dataOutputAssociation', 'property',
                              'standardLoopCharacteristics'):
                    e.remove(ch)
            if ln(e) == 'callActivity':
                e.tag = B + 'task'
                e.attrib.pop('calledElement', None)
    flows = list(q.iter(B + 'sequenceFlow'))
    captura = {}
    for e in q.iter(B + 'intermediateCatchEvent'):
        if e.find(B + 'linkEventDefinition') is not None:
            captura.setdefault((e.get('name') or '').strip(), []).append(e)
    for th in list(q.iter(B + 'intermediateThrowEvent')):
        if th.find(B + 'linkEventDefinition') is None:
            continue
        destinos = captura.get((th.get('name') or '').strip(), [])
        if len(destinos) != 1:
            continue
        for f in flows:
            if f.get('targetRef') == th.get('id'):
                f.set('targetRef', destinos[0].get('id'))
        q.remove(th)
    for e in q.iter():
        if isinstance(e.tag, str):
            for ch in list(e):
                if ln(ch) in ('incoming', 'outgoing'):
                    e.remove(ch)
    defs = etree.Element(B + 'definitions', nsmap={'bpmn': B[1:-1]})
    defs.set('targetNamespace', 'http://validacion')
    defs.append(q)
    return defs, q


def grafo(root):
    """Grafo de toda la colaboración: flujos de secuencia y flujos de mensaje entre nodos (con semántica de unión
    exclusiva). Un mensaje hacia un pool cerrado se consume ahí; un mensaje desde un pool cerrado abre un escenario."""
    nodos, fl, borde = {}, {}, {}
    defs_proc = []
    for p in root.iter(B + 'process'):
        if not any(ln(e) in NODOS for e in p):
            continue
        defs, q = proceso_simple(p)
        defs_proc.append((p.get('name') or p.get('id'), defs, q))
        for e in q:
            if ln(e) in NODOS:
                nodos[e.get('id')] = e
                if ln(e) == 'boundaryEvent':
                    borde.setdefault(e.get('attachedToRef'), []).append(e.get('id'))
        for f in q.iter(B + 'sequenceFlow'):
            fl[f.get('id')] = (f.get('sourceRef'), f.get('targetRef'))
    pools = {pp.get('id'): pp.get('name') for pp in root.iter(B + 'participant')}
    con_secuencia = {b for (_, b) in fl.values()}
    entradas_externas = {}
    for m in root.iter(B + 'messageFlow'):
        s, t = m.get('sourceRef'), m.get('targetRef')
        if s in nodos and t in nodos:
            fl[m.get('id')] = (s, t)
        elif s in nodos:
            fl[m.get('id')] = (s, '_externo:' + pools.get(t, t))
        elif t in nodos and (ln(nodos[t]) == 'startEvent' or t not in con_secuencia):
            # un mensaje desde un pool cerrado abre un escenario solo si llega a un inicio o a un elemento sin
            # flujo de entrada; si llega a una actividad o evento intermedio ya alcanzable, se recibe en el recorrido
            entradas_externas[t] = pools.get(s, s)
    inc, out = {}, {}
    for i, (a, b) in fl.items():
        out.setdefault(a, []).append(i)
        inc.setdefault(b, []).append(i)
    return dict(nodos=nodos, fl=fl, inc=inc, out=out, borde=borde, externas=entradas_externas), defs_proc


def juego_tokens(g, inicio, max_estados=200000, tope=3):
    """Recorre los estados alcanzables desde un nodo de inicio (con un token que entra a él)."""
    nodos, fl, borde = g['nodos'], dict(g['fl']), g['borde']
    inc = {k: list(v) for k, v in g['inc'].items()}
    out = g['out']
    fl['_inicio'] = (None, inicio)
    inc.setdefault(inicio, []).append('_inicio')
    nom = lambda i: nombre(nodos[i]) if i in nodos else i.replace('_externo:', 'pool ')

    def sucesores(est):
        tok = dict(est)
        res = []
        for n, e in nodos.items():
            t = ln(e)
            llegan = [f for f in inc.get(n, []) if tok.get(f)]
            if t == 'parallelGateway':
                if not inc.get(n) or len(llegan) < len(inc[n]):
                    continue
                consumos = [inc[n]]
            else:
                if not llegan:
                    continue
                consumos = [[f] for f in llegan]
            for c in consumos:
                base = dict(tok)
                for f in c:
                    base[f] -= 1
                if t in DECISION:
                    salidas = [[f] for f in out.get(n, []) if not fl[f][1].startswith('_externo')] or [[]]
                    salidas = [s + [f for f in out.get(n, []) if fl[f][1].startswith('_externo')] for s in salidas]
                elif t == 'endEvent':
                    salidas = [[f for f in out.get(n, [])]]
                    if e.find(B + 'terminateEventDefinition') is not None:
                        base = {}
                else:
                    salidas = [out.get(n, [])]
                    salidas += [out.get(b, []) for b in borde.get(n, [])]
                det = len(salidas) == 1
                for sal in salidas:
                    nuevo = dict(base)
                    for f in sal:
                        if not fl[f][1].startswith('_externo'):
                            nuevo[f] = nuevo.get(f, 0) + 1
                    res.append((n, tuple(sorted((k, v) for k, v in nuevo.items() if v))))
                if det:
                    # reducción de orden parcial: un paso sin elección no inhabilita a otros (modelo sin compuertas
                    # basadas en eventos), así que basta con dispararlo primero; las elecciones se exploran todas
                    return res[-1:]
        return res

    ini = (('_inicio', 1),)
    vistos, pila, aristas, disparados = {ini}, [ini], {}, set()
    bloqueos, acumulacion = [], set()
    while pila and len(vistos) < max_estados:
        est = pila.pop()
        suc = sucesores(est)
        aristas[est] = [s2 for _, s2 in suc]
        if est and not suc:
            bloqueos.append(est)
        for n, s2 in suc:
            disparados.add(n)
            if any(v > tope for _, v in s2):
                acumulacion.add(n)
                continue
            if s2 not in vistos:
                vistos.add(s2)
                pila.append(s2)
    hallazgos = []
    if len(vistos) >= max_estados:
        hallazgos.append(f'exploración cortada en {max_estados} estados')
    pueden = {()} if () in vistos else set()
    cambio = True
    while cambio:
        cambio = False
        for est, sig in aristas.items():
            if est not in pueden and any(x in pueden for x in sig):
                pueden.add(est)
                cambio = True

    def donde(est):
        partes = []
        for f, v in est:
            dest = fl[f][1]
            e = nodos.get(dest)
            extra = ''
            if e is not None and ln(e) == 'parallelGateway':
                llegan = sum(1 for h in inc[dest] if dict(est).get(h))
                extra = f' (compuerta paralela: llegan {llegan} de {len(inc[dest])} entradas)'
            partes.append(f'antes de "{nom(dest)}"{extra}')
        return '; '.join(partes)

    for b in sorted({donde(x) for x in bloqueos})[:6]:
        hallazgos.append('BLOQUEO: token detenido ' + b)
    sin_salida = [x for x in vistos if x not in pueden and x not in bloqueos]
    if sin_salida and not bloqueos and len(vistos) < max_estados:
        hallazgos.append(f'{len(sin_salida)} estado(s) desde los que ya no se puede terminar (ciclo sin salida)')
    for n in sorted(acumulacion)[:3]:
        hallazgos.append(f'ACUMULACIÓN: los tokens se multiplican al pasar por "{nom(n)}" (rama paralela sin unión '
                         f'dentro de un ciclo; guía 07_, B8)')
    return hallazgos, disparados


def d3_pm4py(defs, q):
    try:
        stdout, sys.stdout = sys.stdout, io.StringIO()
        try:
            import pm4py
        finally:
            sys.stdout = stdout
    except ImportError:
        return 'pm4py no instalado'
    con_entrada = {f.get('targetRef') for f in q.iter(B + 'sequenceFlow')}
    entradas = [e for e in q if ln(e) in NODOS and ln(e) not in ('startEvent', 'boundaryEvent')
                and e.get('id') not in con_entrada]
    if entradas or sum(1 for e in q if ln(e) == 'startEvent') != 1:
        return 'no evaluable (más de un punto de entrada)'
    ruta = os.path.join(os.environ.get('TEMP', '.'), '_validar_bpmn_tmp.bpmn')
    open(ruta, 'wb').write(etree.tostring(defs, xml_declaration=True, encoding='UTF-8'))
    try:
        stdout, sys.stdout = sys.stdout, io.StringIO()
        try:
            b = pm4py.read_bpmn(ruta)
            net, im, fm = pm4py.convert_to_petri_net(b)
            ok = pm4py.check_soundness(net, im, fm)[0]
        finally:
            sys.stdout = stdout
        return 'sound' if ok else 'unsound'
    except Exception as ex:
        return f'error ({type(ex).__name__})'


def d3(root, usar_pm4py=False):
    g, defs_proc = grafo(root)
    nodos = g['nodos']
    res = []
    inicios = [i for i, e in nodos.items() if ln(e) == 'startEvent']
    escenarios = [(i, f'inicio "{nombre(nodos[i])}"') for i in inicios]
    escenarios += [(i, f'mensaje desde el pool "{p}" a "{nombre(nodos[i])}"') for i, p in g['externas'].items()]
    huerfanos = [i for i, e in nodos.items() if ln(e) not in ('startEvent', 'boundaryEvent')
                 and not g['inc'].get(i) and i not in g['externas']]
    alcanzados = set()
    for i, desc in escenarios:
        hall, disp = juego_tokens(g, i)
        alcanzados |= disp | {i}
        res.append(f'escenario {desc}: ' + ('sin bloqueos' if not hall else 'CON HALLAZGOS'))
        res += ['    ' + h for h in hall]
    if not inicios:
        res.append('SIN EVENTO DE INICIO en la colaboración (guía 07_, B15)')
    for p, defs, q in defs_proc:
        if not any(ln(e) == 'startEvent' for e in q) and any(ln(e) in NODOS for e in q):
            res.append(f'pool "{p}" sin evento de inicio (guía 07_, B15)')
    if huerfanos:
        res.append('ELEMENTOS SIN LLEGADA (ningún flujo ni mensaje los activa; p. ej., enlace sin pareja): '
                   + ', '.join(f'"{nombre(nodos[i])}"' for i in huerfanos))
    nunca = [i for i in nodos if i not in alcanzados and i not in huerfanos and ln(nodos[i]) != 'boundaryEvent']
    if nunca:
        res.append(f'{len(nunca)} elemento(s) que ningún escenario alcanza: '
                   + ', '.join(f'"{nombre(nodos[i])}"' for i in nunca[:8]) + ('…' if len(nunca) > 8 else ''))
    if usar_pm4py:
        for p, defs, q in defs_proc:
            res.append(f'contraste pm4py, proceso "{p}": ' + d3_pm4py(defs, q))
    return res


archivos = []
for a in [x for x in sys.argv[1:] if not x.startswith('--')]:
    archivos += sorted(glob.glob(os.path.join(a, '*.bpmn'))) if os.path.isdir(a) else [a]
for f in archivos:
    doc = etree.parse(f)
    ok = schema.validate(doc)
    print(f'## {os.path.basename(f)}')
    print(f'D1 esquema OMG: {"válido" if ok else "INVÁLIDO"}')
    for e in list(schema.error_log)[:10]:
        print(f'    línea {e.line}: {e.message[:200]}')
    probs = d2(doc.getroot())
    print(f'D2 referencias: {"sin problemas" if not probs else str(len(probs)) + " problema(s)"}')
    for x in probs[:20]:
        print('    ' + x)
    print('D3 bloqueos y terminación (juego de tokens):')
    for x in d3(doc.getroot(), '--pm4py' in sys.argv):
        print('    ' + x)
