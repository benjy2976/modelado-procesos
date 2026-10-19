"""Convierte un BPMN 2.0 estandar (salida de tabla_a_bpmn.py) al dialecto que importa Bizagi Modeler.

Reconstruido a partir de la copia de referencia de la herramienta original (plantilla_tabla_bizagi.bpmn):
1. Identificadores con prefijo "Id_" y cuerpo GUID. Se conservan los GUID existentes; los demas se derivan
   de forma determinista (uuid5), de modo que la salida es reproducible.
2. dataObjectReference + dataObject vacio -> un solo dataObject con nombre (toma el id de la referencia).
3. Cada actividad con documentos declara ioSpecification (dataInput/dataOutput, inputSet y outputSet) y sus
   asociaciones de datos apuntan a esas entradas y salidas; se elimina el marcador __targetRef_placeholder.
4. Por cada asociacion de datos se agrega una bpmn:association visual que conserva el id original, porque las
   aristas del diagrama apuntan a ella.
5. Toda etiqueta del diagrama usa un BPMNLabelStyle (Segoe UI 8).

Uso: python _bpmn_a_bizagi.py <entrada.bpmn> <salida.bpmn | carpeta>
Con una carpeta, escribe <carpeta>/<nombre>_bizagi.bpmn (forma en que lo invoca tabla_a_bpmn.py).
"""
import os
import re
import sys
import uuid

from lxml import etree

B = "http://www.omg.org/spec/BPMN/20100524/MODEL"
DI = "http://www.omg.org/spec/BPMN/20100524/DI"
DC = "http://www.omg.org/spec/DD/20100524/DC"
NS = uuid.UUID("0b9d1f3e-5a2c-4e7b-8c6d-1f2e3a4b5c6d")
GUID = re.compile(r"^_?([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$")
ACTIVIDADES = {"task", "userTask", "manualTask", "serviceTask", "callActivity", "subProcess", "sendTask",
               "receiveTask", "scriptTask", "businessRuleTask"}
REF_ATTR = ("sourceRef", "targetRef", "processRef", "bpmnElement", "dataStoreRef", "dataObjectRef",
            "labelStyle", "attachedToRef", "calledElement", "messageRef", "default", "categoryValueRef")
REF_TEXT = ("flowNodeRef", "incoming", "outgoing", "sourceRef", "targetRef", "dataInputRefs", "dataOutputRefs")


def q(ns, tag):
    return f"{{{ns}}}{tag}"


def nuevo(*partes):
    return "_" + str(uuid.uuid5(NS, "|".join(partes)))


def convertir(raiz):
    # 0. Bizagi descarta un pool sin proceso (prueba del 2026-10-16): se agrega un proceso vacío a cada pool cerrado
    procesos = raiz.findall(q(B, "process"))
    for part in raiz.iter(q(B, "participant")):
        if not part.get("processRef"):
            pid = nuevo(part.get("id"), "proceso")
            proc = etree.Element(q(B, "process"), id=pid, name=part.get("name", ""), isExecutable="false")
            ancla = procesos[-1] if procesos else raiz.find(q(B, "collaboration"))
            ancla.addnext(proc)
            procesos.append(proc)
            part.set("processRef", pid)

    # 2. objetos de datos: la referencia pasa a ser el dataObject con nombre
    for proc in raiz.iter(q(B, "process")):
        vacios = {d.get("id"): d for d in proc.findall(q(B, "dataObject"))}
        for ref in proc.findall(q(B, "dataObjectReference")):
            obj = etree.Element(q(B, "dataObject"), id=ref.get("id"), name=ref.get("name", ""))
            proc.replace(ref, obj)
            vacio = vacios.pop(ref.get("dataObjectRef"), None)
            if vacio is not None:
                proc.remove(vacio)

    # 3 y 4. ioSpecification y asociaciones visuales
    for proc in raiz.iter(q(B, "process")):
        visuales = []
        for act in [e for e in proc if etree.QName(e).localname in ACTIVIDADES]:
            entradas = act.findall(q(B, "dataInputAssociation"))
            salidas = act.findall(q(B, "dataOutputAssociation"))
            for p in act.findall(q(B, "property")):
                if p.get("name") == "__targetRef_placeholder":
                    act.remove(p)
            if not entradas and not salidas:
                continue
            aid = act.get("id")
            io = etree.Element(q(B, "ioSpecification"), id=nuevo(aid, "io"))
            din, dout = [], []
            for a in entradas:
                i = nuevo(a.get("id"), "dataInput")
                etree.SubElement(io, q(B, "dataInput"), id=i)
                din.append(i)
            for a in salidas:
                o = nuevo(a.get("id"), "dataOutput")
                etree.SubElement(io, q(B, "dataOutput"), id=o)
                dout.append(o)
            iset = etree.SubElement(io, q(B, "inputSet"), id=nuevo(aid, "inputSet"))
            for i in din:
                etree.SubElement(iset, q(B, "dataInputRefs")).text = i
            oset = etree.SubElement(io, q(B, "outputSet"), id=nuevo(aid, "outputSet"))
            for o in dout:
                etree.SubElement(oset, q(B, "dataOutputRefs")).text = o
            # ioSpecification va despues de documentation, incoming y outgoing
            pos = max([list(act).index(e) for e in act
                       if etree.QName(e).localname in ("documentation", "incoming", "outgoing")] + [-1])
            act.insert(pos + 1, io)
            for a, i in zip(entradas, din):
                fuente = a.find(q(B, "sourceRef")).text
                a.find(q(B, "targetRef")).text = i
                visuales.append((a.get("id"), fuente, aid))
                a.set("id", nuevo(a.get("id"), "dataInputAssociation"))
            for a, o in zip(salidas, dout):
                destino = a.find(q(B, "targetRef")).text
                src = etree.Element(q(B, "sourceRef"))
                src.text = o
                a.insert(0, src)
                visuales.append((a.get("id"), aid, destino))
                a.set("id", nuevo(a.get("id"), "dataOutputAssociation"))
        for vid, s, t in visuales:
            etree.SubElement(proc, q(B, "association"), id=vid, sourceRef=s, targetRef=t)

    # 5. estilo de etiquetas
    for diag in raiz.iter(q(DI, "BPMNDiagram")):
        sid = nuevo(diag.get("id"), "labelStyle")
        estilo = etree.SubElement(diag, q(DI, "BPMNLabelStyle"), id=sid)
        etree.SubElement(estilo, q(DC, "Font"), name="Segoe UI", size="8", isBold="false", isItalic="false",
                         isUnderline="false", isStrikeThrough="false")
        for lab in diag.iter(q(DI, "BPMNLabel")):
            lab.set("labelStyle", sid)

    # 1. identificadores Id_<GUID>
    mapa = {}
    for e in raiz.iter():
        i = e.get("id") if isinstance(e.tag, str) else None
        if i:
            m = GUID.match(i)
            mapa[i] = "Id_" + (m.group(1) if m else str(uuid.uuid5(NS, i)))
    for e in raiz.iter():
        if not isinstance(e.tag, str):
            continue
        if e.get("id"):
            e.set("id", mapa[e.get("id")])
        for at in REF_ATTR:
            if e.get(at) in mapa:
                e.set(at, mapa[e.get(at)])
        if etree.QName(e).localname in REF_TEXT and e.text and e.text.strip() in mapa:
            e.text = mapa[e.text.strip()]
    return raiz


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    arbol = etree.parse(sys.argv[1], etree.XMLParser(remove_blank_text=True))
    convertir(arbol.getroot())
    destino = sys.argv[2]
    if not destino.lower().endswith(".bpmn"):
        os.makedirs(destino, exist_ok=True)
        base = os.path.splitext(os.path.basename(sys.argv[1]))[0]
        destino = os.path.join(destino, base + "_bizagi.bpmn")
    arbol.write(destino, xml_declaration=True, encoding="UTF-8")
    print(destino)


if __name__ == "__main__":
    main()
