"""Revisa el dibujo (BPMN DI) de archivos BPMN 2.0 y reporta superposiciones (control D4).

Uso: python _revisar_trazado.py <archivo_o_carpeta> [...]
Controles:
- T1 flujos de secuencia o de mensaje que atraviesan un elemento que no es su origen ni su destino;
- T2 tramos de dos flujos distintos que corren superpuestos (se admiten los tramos comunes de flujos que comparten
  origen o destino: troncos de bifurcación y de unión);
- T3 flujos de mensaje que atraviesan un pool que no es su origen ni su destino;
- T4 etiquetas que se montan sobre elementos u otras etiquetas;
- T5 elementos que se superponen entre sí;
- T6 flujos que cruzan una etiqueta ajena.
Funciona con cualquier BPMN con diagrama, incluidos los exportados desde Bizagi. Requiere lxml.
"""
import glob
import os
import sys
from lxml import etree

sys.stdout.reconfigure(encoding='utf-8')
B = '{http://www.omg.org/spec/BPMN/20100524/MODEL}'
BDI = '{http://www.omg.org/spec/BPMN/20100524/DI}'
DC = '{http://www.omg.org/spec/DD/20100524/DC}'
DI = '{http://www.omg.org/spec/DD/20100524/DI}'
ln = lambda e: etree.QName(e).localname
CONTENEDORES = ('participant', 'lane')
MAX = 8


def caja(e):
    b = e.find(DC + 'Bounds')
    return tuple(float(b.get(k)) for k in ('x', 'y', 'width', 'height')) if b is not None else None


def cruza(p, q, c, m=2):
    x, y, w, h = c[0] + m, c[1] + m, c[2] - 2 * m, c[3] - 2 * m
    if w <= 0 or h <= 0:
        return False
    if abs(p[0] - q[0]) < 0.5:
        return x < p[0] < x + w and max(min(p[1], q[1]), y) < min(max(p[1], q[1]), y + h)
    if abs(p[1] - q[1]) < 0.5:
        return y < p[1] < y + h and max(min(p[0], q[0]), x) < min(max(p[0], q[0]), x + w)
    # tramo oblicuo: muestreo
    for k in range(1, 20):
        t = k / 20
        px, py = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        if x < px < x + w and y < py < y + h:
            return True
    return False


def inter(a, b):
    w = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
    h = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
    return w * h if w > 0 and h > 0 else 0


def revisar(ruta):
    raiz = etree.parse(ruta).getroot()
    el = {e.get('id'): e for e in raiz.iter() if isinstance(e.tag, str) and e.get('id')}
    nom = lambda i: ((el[i].get('name') or ln(el[i])) if i in el else i).replace('\n', ' ')[:45]
    dueno = {}  # nodo -> participant
    proc_part = {p.get('processRef'): p.get('id') for p in raiz.iter(B + 'participant')}
    for pr in raiz.iter(B + 'process'):
        for e in pr.iter():
            if isinstance(e.tag, str) and e.get('id'):
                dueno[e.get('id')] = proc_part.get(pr.get('id'))
    formas, etiquetas, pools = {}, [], {}
    for s in raiz.iter(BDI + 'BPMNShape'):
        i = s.get('bpmnElement')
        c = caja(s)
        if i not in el or c is None:
            continue
        t = ln(el[i])
        if t == 'participant':
            pools[i] = c
        elif t not in CONTENEDORES and t not in ('group', 'textAnnotation'):
            formas[i] = c
        lab = s.find(BDI + 'BPMNLabel')
        if lab is not None and caja(lab) and t not in ACT and t not in CONTENEDORES:
            etiquetas.append((i, caja(lab), nom(i)))
    aristas = []
    for e in raiz.iter(BDI + 'BPMNEdge'):
        i = e.get('bpmnElement')
        if i not in el:
            continue
        f = el[i]
        pts = [(float(w.get('x')), float(w.get('y'))) for w in e.findall(DI + 'waypoint')]
        s, t = f.get('sourceRef'), f.get('targetRef')
        if ln(f) in ('dataInputAssociation', 'dataOutputAssociation'):
            t = f.findtext(B + 'targetRef')
            s = f.findtext(B + 'sourceRef') or f.getparent().get('id')
            if t and t.endswith('_ph'):
                t = f.getparent().get('id')
        aristas.append(dict(id=i, tipo=ln(f), s=s, t=t, pts=pts, nombre=f.get('name') or ''))
        lab = e.find(BDI + 'BPMNLabel')
        if lab is not None and caja(lab) and f.get('name'):
            etiquetas.append((i, caja(lab), f.get('name')[:45]))
    h = {k: [] for k in ('T1', 'T2', 'T3', 'T4', 'T5', 'T6')}
    for a in aristas:
        if a['tipo'] not in ('sequenceFlow', 'messageFlow'):
            continue
        for p, q in zip(a['pts'], a['pts'][1:]):
            for i, c in formas.items():
                if i not in (a['s'], a['t']) and cruza(p, q, c, -3):
                    h['T1'].append(f'{a["tipo"]} "{nom(a["s"])}" -> "{nom(a["t"])}" atraviesa "{nom(i)}"')
            if a['tipo'] == 'messageFlow':
                propios = {a['s'], a['t'], dueno.get(a['s']), dueno.get(a['t'])}
                for i, c in pools.items():
                    if i not in propios and cruza(p, q, c, 0):
                        h['T3'].append(f'mensaje "{a["nombre"][:40]}" atraviesa el pool "{nom(i)}"')
    segs = [(a, p, q) for a in aristas if a['tipo'] in ('sequenceFlow', 'messageFlow')
            for p, q in zip(a['pts'], a['pts'][1:])]
    for x in range(len(segs)):
        a, p, q = segs[x]
        for y in range(x + 1, len(segs)):
            b, r, s = segs[y]
            if a is b or a['s'] == b['s'] or a['t'] == b['t']:
                continue
            if abs(p[0] - q[0]) < 0.5 and abs(r[0] - s[0]) < 0.5 and abs(p[0] - r[0]) < 2:
                lo = max(min(p[1], q[1]), min(r[1], s[1]))
                hi = min(max(p[1], q[1]), max(r[1], s[1]))
            elif abs(p[1] - q[1]) < 0.5 and abs(r[1] - s[1]) < 0.5 and abs(p[1] - r[1]) < 2:
                lo = max(min(p[0], q[0]), min(r[0], s[0]))
                hi = min(max(p[0], q[0]), max(r[0], s[0]))
            else:
                continue
            if hi - lo > 4:
                h['T2'].append(f'"{nom(a["s"])}" -> "{nom(a["t"])}" y "{nom(b["s"])}" -> "{nom(b["t"])}" '
                               f'comparten {hi - lo:.0f} px')
    for k, (i, c, txt) in enumerate(etiquetas):
        for j, fc in formas.items():
            if j != i and inter(c, fc) > 20:
                h['T4'].append(f'etiqueta "{txt}" sobre "{nom(j)}"')
        for i2, c2, t2 in etiquetas[k + 1:]:
            if inter(c, c2) > 20:
                h['T4'].append(f'etiqueta "{txt}" sobre la etiqueta "{t2}"')
    for a in aristas:
        if a['tipo'] not in ('sequenceFlow', 'messageFlow'):
            continue
        for i, c, txt in etiquetas:
            if i == a['id']:
                continue
            if any(cruza(p, q, c, 1) for p, q in zip(a['pts'], a['pts'][1:])):
                h['T6'].append(f'{a["tipo"]} "{nom(a["s"])}" -> "{nom(a["t"])}" cruza la etiqueta "{txt}"')
    ids = list(formas)
    for x in range(len(ids)):
        for y in range(x + 1, len(ids)):
            if inter(formas[ids[x]], formas[ids[y]]) > 4:
                h['T5'].append(f'"{nom(ids[x])}" y "{nom(ids[y])}" se superponen')
    return h


ACT = ('task', 'userTask', 'manualTask', 'serviceTask', 'sendTask', 'receiveTask', 'scriptTask',
       'businessRuleTask', 'callActivity', 'subProcess')
TITULOS = {'T1': 'flujos que atraviesan elementos', 'T2': 'flujos superpuestos',
           'T3': 'mensajes que atraviesan pools ajenos', 'T4': 'etiquetas montadas', 'T5': 'elementos superpuestos',
           'T6': 'flujos que cruzan etiquetas'}

if __name__ == '__main__':
    archivos = []
    for a in sys.argv[1:]:
        archivos += sorted(glob.glob(os.path.join(a, '*.bpmn'))) if os.path.isdir(a) else [a]
    for f in archivos:
        h = revisar(f)
        total = sum(len(v) for v in h.values())
        print(f'D4 trazado ({os.path.basename(f)}): ' + ('sin superposiciones' if not total else f'{total} hallazgo(s)'))
        for k, v in h.items():
            v = list(dict.fromkeys(v))
            if v:
                print(f'    {k} {TITULOS[k]}: {len(v)}')
                for x in v[:MAX]:
                    print('        ' + x)
                if len(v) > MAX:
                    print(f'        … y {len(v) - MAX} más')
