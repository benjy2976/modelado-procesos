"""Genera un BPMN 2.0 con diagrama a partir de una descripción de procesos en Markdown, lo valida y produce la
copia que importa Bizagi Modeler. Herramienta genérica: no depende de este proyecto.

Uso: python tabla_a_bpmn.py <entrada.md> [carpeta_salida] [--sin-bizagi] [--sin-visor]
Sin carpeta de salida, se usa salida/<nombre de la entrada>/ dentro de la carpeta de esta herramienta.

Entrada: un .md en uno de dos formatos, que se detecta solo:
- tabla: título "# ...", tabla "## Elementos" obligatoria; "## Mensajes" y "## Pools" opcionales. Plantilla del
  proyecto: 00-gobernanza/plantillas/modelamiento/diagrama-proceso-tabla.md;
- lista: "## Pool: X", "### Carril", "- ID (tipo) Nombre → siguientes" y subviñetas.
Salida, en la carpeta indicada:
- <nombre>.bpmn: BPMN 2.0 estándar con pools, carriles, nodos, flujos, mensajes, datos y coordenadas calculadas.
- validacion.txt: informe de `_validar_bpmn.py` (D1-D3: esquema OMG, referencias, bloqueos), `_revisar_trazado.py`
  (D4: superposiciones del dibujo) y `_revisar_notacion.py` (D5: paleta del proyecto y buenas practicas del manual).
- bizagi/<nombre>_bizagi.bpmn: copia en el dialecto de Bizagi (`_bpmn_a_bizagi.py`), para importar en Bizagi Modeler.
- <nombre>_visor.html: vista rápida en el navegador, con bpmn-js local fijado (`renderizar_bpmn.py`) y colores de
  estilo Bizagi; sin la copia local, usa bpmn-js desde internet.
Las imágenes SVG y PNG se generan aparte con `renderizar_bpmn.py`.
Trazado (versión 2.0): columnas por orden del flujo; una fila por rama de cada compuerta dentro del carril; flujos
ortogonales que esquivan las cajas; puertos de mensaje repartidos; pools externos cerrados en bandas, los que envían
arriba y los que reciben abajo, junto al elemento con el que se comunican; etiquetas dimensionadas según su texto.
Requiere lxml. Usa _validar_bpmn.py, _revisar_trazado.py y _bpmn_a_bizagi.py (con la carpeta xsd_bpmn20/), que busca
en esta carpeta o en la superior. En el proyecto: 05-herramientas/gestor-modelos/ (DEC-025).
"""
import os
import re
import subprocess
import sys
import uuid
from xml.sax.saxutils import escape, quoteattr

sys.stdout.reconfigure(encoding='utf-8')
AQUI = os.path.dirname(os.path.abspath(__file__))


def auxiliar(nombre):
    """Ubica los auxiliares en esta carpeta o en la superior (8. Scripts del proyecto)."""
    for d in (AQUI, os.path.dirname(AQUI)):
        if os.path.exists(os.path.join(d, nombre)):
            return os.path.join(d, nombre)
    sys.exit(f'No se encontró {nombre} ni en {AQUI} ni en la carpeta superior.')


NS_UUID = uuid.UUID('6f1c2a7e-3b0d-4c8e-9a51-2d7f4e8b9c10')

TIPOS = {  # tipo en la tabla -> (etiqueta BPMN, definición de evento, ancho, alto)
    'inicio': ('startEvent', None, 36, 36),
    'inicio-mensaje': ('startEvent', 'message', 36, 36),
    'inicio-temporizador': ('startEvent', 'timer', 36, 36),
    'inicio-condicional': ('startEvent', 'conditional', 36, 36),
    'inicio-senal': ('startEvent', 'signal', 36, 36),
    'tarea': ('task', None, 100, 80),
    'tarea-usuario': ('userTask', None, 100, 80),
    'tarea-manual': ('manualTask', None, 100, 80),
    'tarea-servicio': ('serviceTask', None, 100, 80),
    'subproceso': ('callActivity', None, 100, 80),
    'compuerta': ('exclusiveGateway', None, 50, 50),
    'compuerta-paralela': ('parallelGateway', None, 50, 50),
    'compuerta-inclusiva': ('inclusiveGateway', None, 50, 50),
    'compuerta-eventos': ('eventBasedGateway', None, 50, 50),
    'temporizador': ('intermediateCatchEvent', 'timer', 36, 36),
    'mensaje-recepcion': ('intermediateCatchEvent', 'message', 36, 36),
    'mensaje-envio': ('intermediateThrowEvent', 'message', 36, 36),
    'condicional': ('intermediateCatchEvent', 'conditional', 36, 36),
    'senal-recepcion': ('intermediateCatchEvent', 'signal', 36, 36),
    'senal-envio': ('intermediateThrowEvent', 'signal', 36, 36),
    'escalacion-envio': ('intermediateThrowEvent', 'escalation', 36, 36),
    'hito': ('intermediateThrowEvent', None, 36, 36),
    'fin': ('endEvent', None, 36, 36),
    'fin-mensaje': ('endEvent', 'message', 36, 36),
    'fin-terminal': ('endEvent', 'terminate', 36, 36),
    'fin-senal': ('endEvent', 'signal', 36, 36),
    'fin-escalacion': ('endEvent', 'escalation', 36, 36),
    'fin-error': ('endEvent', 'error', 36, 36),
    # eventos de borde: columna Adjunto (actividad) e Interrumpe (Sí por defecto)
    'borde-temporizador': ('boundaryEvent', 'timer', 36, 36),
    'borde-mensaje': ('boundaryEvent', 'message', 36, 36),
    'borde-condicional': ('boundaryEvent', 'conditional', 36, 36),
    'borde-senal': ('boundaryEvent', 'signal', 36, 36),
    'borde-escalacion': ('boundaryEvent', 'escalation', 36, 36),
    'borde-error': ('boundaryEvent', 'error', 36, 36),
    # subprocesos de evento sin interrupción, contraídos, fuera del flujo principal (DEC-024)
    'subproceso-evento-mensaje': ('subProcess', 'message', 120, 90),
    'subproceso-evento-temporizador': ('subProcess', 'timer', 120, 90),
    'subproceso-evento-condicional': ('subProcess', 'conditional', 120, 90),
}
ACTIVIDAD = ('task', 'userTask', 'manualTask', 'serviceTask', 'callActivity', 'subProcess')
MARCADORES = {  # columna Marcador de las actividades (manual BPMN, sec. 2.7.2, p. 79-81)
    'multiple-paralelo': '<bpmn:multiInstanceLoopCharacteristics isSequential="false" />',
    'multiple-secuencial': '<bpmn:multiInstanceLoopCharacteristics isSequential="true" />',
    'bucle': '<bpmn:standardLoopCharacteristics />',
}

# Geometría (px). FILA: alto de cada fila de un carril; NODO_Y: centro del nodo dentro de la fila.
POOL_X, CAB, COL, FILA, NODO_Y, GAP_POOL = 20, 50, 170, 230, 80, 40
SLOT, NIVEL, MARGEN_FAN, SEP_POOL = 150, 12, 16, 30
CELDA, FILA_SEV = 420, 200  # zona de subprocesos de evento: marco expandido, anotación y pasillo de 20 px
AVISOS_TRAZADO = []  # avisos que detecta el trazado (por ejemplo, un elemento ajeno dentro de un grupo)
FILA_BAJA = 160  # fila sin objetos de datos; las filas con documentos usan FILA
LARGO_BIZAGI = {'evento': 40, 'compuerta': 40, 'mensaje': 50}  # Bizagi recorta etiquetas más largas


def gid(*partes):
    return '_' + str(uuid.uuid5(NS_UUID, '|'.join(partes)))


def tabla(md, titulo):
    """Filas (dict por encabezado) de la primera tabla bajo '## <titulo>'."""
    m = re.search(r'^##\s+' + re.escape(titulo) + r'\s*$', md, re.MULTILINE | re.IGNORECASE)
    if not m:
        return []
    lineas = md[m.end():].split('\n')
    filas, cab = [], None
    for ln in lineas:
        s = ln.strip()
        if s.startswith('## '):
            break
        if not s.startswith('|'):
            if cab is not None and filas:
                break
            continue
        celdas = [c.strip() for c in s.strip('|').split('|')]
        if cab is None:
            cab = [c.lower() for c in celdas]
        elif not set(s.replace('|', '').strip()) <= set('-: '):
            filas.append(dict(zip(cab, celdas + [''] * (len(cab) - len(celdas)))))
    return filas


def lista(md):
    """Formato de lista: '## Pool: X' o '## Pool externo: X', '### Carril', '- ID (tipo) Nombre → siguientes' y
    subviñetas 'entra:', 'sale:', 'almacén:', 'plazo:', 'nota:' y 'mensaje: Destino [Nombre]'.
    Devuelve las mismas filas que el formato de tabla."""
    elems, pools, msgs = [], [], []
    pool = carril = None
    actual = None
    for ln in md.splitlines():
        s = ln.rstrip()
        m = re.match(r'^##\s+Pool(\s+externo)?\s*:\s*(.+)$', s, re.IGNORECASE)
        if m:
            pool, carril, actual = m.group(2).strip(), None, None
            pools.append({'pool': pool, 'carriles': '', 'externo': bool(m.group(1))})
            continue
        m = re.match(r'^###\s+(.+)$', s)
        if m and pool:
            carril = m.group(1).strip()
            pools[-1]['carriles'] += ('; ' if pools[-1]['carriles'] else '') + carril
            continue
        m = re.match(r'^[-*]\s+(\S+)\s+\(([^)]+)\)\s*(.*)$', s)
        if m and pool:
            resto = m.group(3)
            partes = re.split(r'\s*(?:→|->)\s*', resto, maxsplit=1)
            nom, sig = (partes + [''])[:2]
            actual = {'id': m.group(1), 'tipo': m.group(2).strip(), 'pool': pool, 'carril': carril or pool,
                      'nombre': nom.strip(), 'siguiente': sig.strip(), 'documentos': '', 'plazo': ''}
            elems.append(actual)
            continue
        m = re.match(r'^\s+[-*]\s+([^:]+):\s*(.+)$', s)
        if m and actual is not None:
            clave, valor = m.group(1).strip().lower(), m.group(2).strip()
            if clave in ('entra', 'sale', 'almacén', 'almacen'):
                actual['documentos'] += ('; ' if actual['documentos'] else '') + f'{clave}: {valor}'
            elif clave in ('plazo', 'nota'):
                actual['plazo'] += ('; ' if actual['plazo'] else '') + valor
            elif clave == 'mensaje':
                mm = re.match(r'^(.+?)\s*(?:\[(.*)\])?$', valor)
                msgs.append({'desde': actual['id'], 'hacia': mm.group(1).strip(), 'nombre': (mm.group(2) or '').strip()})
    return elems, pools, msgs


def leer(ruta):
    with open(ruta, encoding='utf-8') as f:
        md = f.read()
    m = re.search(r'^#\s+(.+)$', md, re.MULTILINE)
    nombre = m.group(1).strip() if m else os.path.splitext(os.path.basename(ruta))[0]
    elems = tabla(md, 'Elementos')
    if elems:
        formato, pools_filas, msg_filas = 'tabla', tabla(md, 'Pools'), tabla(md, 'Mensajes')
    else:
        formato = 'lista'
        elems, pools_filas, msg_filas = lista(md)
    if not elems:
        sys.exit('No se encontró ni la tabla "## Elementos" ni elementos en formato de lista ("- ID (tipo) Nombre → ...").')
    print(f'Formato de entrada: {formato}')
    errores, avisos = [], []
    nodos, orden_pools, carriles = {}, [], {}
    for f in elems:
        i = f.get('id', '')
        tipo = f.get('tipo', '').lower()
        pool = f.get('pool', '') or nombre
        carril = f.get('carril', '') or pool
        if not i:
            errores.append(f'fila sin ID: {f}')
            continue
        if i in nodos:
            errores.append(f'ID repetido: {i}')
        if tipo not in TIPOS:
            errores.append(f'{i}: tipo "{tipo}" no reconocido (válidos: {", ".join(TIPOS)})')
            continue
        sig, defecto = [], ''
        for parte in [p.strip() for p in f.get('siguiente', '').split(';') if p.strip()]:
            mm = re.match(r'^(\S+)\s*(?:\[(.*?)\])?\s*(\(por defecto\))?$', parte, re.IGNORECASE)
            sig.append((mm.group(1), (mm.group(2) or '').strip()) if mm else (parte, ''))
            if mm and mm.group(3):
                defecto = mm.group(1)
        docs = []
        for parte in [p.strip() for p in f.get('documentos', '').split(';') if p.strip()]:
            mm = re.match(r'^(entra|sale|almac[eé]n)\s*:\s*(.+)$', parte, re.IGNORECASE)
            clase = (mm.group(1).lower().replace('é', 'e') if mm else 'sale')
            docs.append((clase, (mm.group(2) if mm else parte).strip()))
        sev = TIPOS[tipo][0] == 'subProcess'
        borde = TIPOS[tipo][0] == 'boundaryEvent'
        adjunto = f.get('adjunto', '').strip()
        interrumpe = (f.get('interrumpe', '') or 'Sí').strip().lower() not in ('no', 'false')
        marcador = f.get('marcador', '').strip().lower()
        if borde and not adjunto:
            errores.append(f'{i}: un evento de borde necesita la columna Adjunto con el ID de su actividad')
        if tipo == 'borde-error' and not interrumpe:
            errores.append(f'{i}: un evento de error en el borde siempre interrumpe la actividad')
        if marcador and marcador not in MARCADORES:
            errores.append(f'{i}: marcador "{marcador}" no reconocido (válidos: {", ".join(MARCADORES)})')
        elif marcador and TIPOS[tipo][0] not in ACTIVIDAD:
            errores.append(f'{i}: solo las actividades llevan marcador')
        if defecto and TIPOS[tipo][0] not in ('exclusiveGateway', 'inclusiveGateway', *ACTIVIDAD):
            errores.append(f'{i}: solo una compuerta exclusiva o inclusiva, o una actividad, tiene flujo por defecto')
        if sev and sig:
            errores.append(f'{i}: un subproceso de evento no lleva "Siguiente"; se activa por su disparador')
        if sev and docs:
            avisos.append(f'{i}: los documentos de un subproceso de evento no se dibujan')
            docs = []
        doc = f.get('plazo', '') or f.get('nota', '')
        disparador = f.get('disparador', '').strip()
        if disparador and not sev:
            avisos.append(f'{i}: Disparador solo se dibuja en subprocesos de evento; se guarda como documentación')
            doc = '; '.join(x for x in [doc, disparador] if x)
        nodos[i] = dict(id=i, tipo=tipo, pool=pool, carril=carril, nombre=f.get('nombre', ''), sig=sig, docs=docs,
                        doc=doc, disparador=disparador if sev else '', anotacion=f.get('anotacion', '').strip(),
                        grupo=f.get('grupo', '').strip(), adjunto=adjunto, interrumpe=interrumpe,
                        marcador=marcador, defecto=defecto)
        if pool not in orden_pools:
            orden_pools.append(pool)
        carriles.setdefault(pool, [])
        if carril not in carriles[pool]:
            carriles[pool].append(carril)
    for n in nodos.values():
        if n['adjunto']:
            h = nodos.get(n['adjunto'])
            if h is None or TIPOS[h['tipo']][0] not in ACTIVIDAD or TIPOS[h['tipo']][0] == 'subProcess':
                errores.append(f'{n["id"]}: Adjunto debe ser el ID de una tarea o subproceso del flujo')
            else:
                n['pool'], n['carril'] = h['pool'], h['carril']  # el evento de borde va en el carril de su actividad
        for d, _ in n['sig']:
            if d not in nodos:
                errores.append(f'{n["id"]}: "Siguiente" apunta a {d}, que no existe')
            elif nodos[d]['pool'] != n['pool']:
                errores.append(f'{n["id"]} -> {d}: un flujo de secuencia no cruza pools; use un mensaje')
            elif TIPOS[nodos[d]['tipo']][0] == 'subProcess':
                errores.append(f'{n["id"]} -> {d}: un subproceso de evento no recibe flujos de secuencia')
    pools_tabla = {f.get('pool', ''): f for f in pools_filas}
    for p, f in pools_tabla.items():
        if p and p not in orden_pools:
            orden_pools.append(p)
        if p in carriles and f.get('carriles'):
            orden = [c.strip() for c in f['carriles'].split(';') if c.strip()]
            usados = set(carriles[p])
            for c in orden:
                if c not in usados:
                    avisos.append(f'pool "{p}": el carril declarado "{c}" no tiene elementos y se omite '
                                  f'(un nombre de carril no puede contener ";")')
            for c in carriles[p]:
                if c not in orden:
                    avisos.append(f'pool "{p}": el carril "{c}" de los elementos no figura en "## Pools"')
            carriles[p] = [c for c in orden if c in usados] + [c for c in carriles[p] if c not in orden]
    mensajes = []
    for f in msg_filas:
        a, b = f.get('desde', ''), f.get('hacia', '')
        for x in (a, b):
            if x not in nodos and x not in orden_pools:
                orden_pools.append(x)  # pool externo (cerrado) nombrado solo en los mensajes
        mensajes.append((a, b, f.get('nombre', '')))
    for p in orden_pools:
        carriles.setdefault(p, [])
    for n in nodos.values():
        et = TIPOS[n['tipo']][0]
        clase = 'compuerta' if 'Gateway' in et else ('evento' if 'Event' in et else None)
        if clase and len(n['nombre']) > LARGO_BIZAGI[clase]:
            avisos.append(f'{n["id"]}: nombre de {len(n["nombre"])} caracteres; Bizagi lo recorta sobre '
                          f'{LARGO_BIZAGI[clase]}')
    for a, b, nom in mensajes:
        if len(nom) > LARGO_BIZAGI['mensaje']:
            avisos.append(f'mensaje "{nom[:40]}…": {len(nom)} caracteres; Bizagi lo recorta sobre '
                          f'{LARGO_BIZAGI["mensaje"]}')
    if errores:
        sys.exit('Errores en la tabla:\n- ' + '\n- '.join(errores))
    return nombre, nodos, orden_pools, carriles, mensajes, avisos


def rangos(nodos, mensajes):
    """Columna de cada nodo: camino más largo desde los inicios, sin los flujos de retorno (ciclos)."""
    ady = {i: [d for d, _ in n['sig']] for i, n in nodos.items()}
    for a, b, _ in mensajes:
        if a in nodos and b in nodos:
            ady[a].append(b)
    retorno, estado = set(), {}

    def dfs(u):
        estado[u] = 1
        for v in ady[u]:
            if estado.get(v) == 1:
                retorno.add((u, v))
            elif v not in estado:
                dfs(v)
        estado[u] = 2

    entradas = {v for vs in ady.values() for v in vs}
    for i in [i for i in nodos if i not in entradas] + list(nodos):
        if i not in estado:
            dfs(i)
    rango = {i: 0 for i in nodos}
    for _ in range(len(nodos)):
        cambio = False
        for u, vs in ady.items():
            for v in vs:
                if (u, v) not in retorno and rango[v] < rango[u] + 1:
                    rango[v] = rango[u] + 1
                    cambio = True
        if not cambio:
            break
    return rango, retorno


def filas(nodos, rango, retorno, bordes=None):
    """Fila de cada nodo dentro de su carril: la primera salida de un nodo conserva su fila y cada salida adicional
    (rama de una compuerta) toma la fila siguiente; en una unión se toma la menor; si la celda está ocupada, se baja."""
    bordes = bordes or {}
    idx = {i: k for k, i in enumerate(nodos)}
    adelante = lambda i, d: (i, d) not in retorno and rango[d] > rango[i]
    mismo = lambda i, d: (nodos[i]['pool'], nodos[i]['carril']) == (nodos[d]['pool'], nodos[d]['carril'])
    fila, ocupado, salida, ramas = {}, set(), {}, {}
    tras_borde = {d for b in bordes for d, _ in nodos[b]['sig'] if rango.get(d) == rango[b]}
    for i in sorted(nodos, key=lambda i: (rango[i], 2 if i in tras_borde else int(i in bordes), idx[i])):
        n = nodos[i]
        clave = (n['pool'], n['carril'])
        if i in bordes:
            # un evento de borde va sobre su actividad; cada rama de excepcion toma una fila propia por debajo y se
            # reserva el pasillo vertical en la columna de la actividad
            fila[i] = fila[bordes[i]]
            col = (*clave, rango[i])
            for d, _ in n['sig']:
                if mismo(i, d) and (i, d) not in retorno:
                    r = max(fila[i] + 1, ramas.get(col, 0))
                    while (*clave, r, rango[i]) in ocupado:
                        r += 1
                    salida[(i, d)] = r
                    ramas[col] = r + 1
                    for rr in range(fila[i] + 1, r):
                        ocupado.add((*clave, rr, rango[i]))
            continue
        deseadas = [f for (p, d), f in salida.items() if d == i]
        f = min(deseadas) if deseadas else 0
        while (n['pool'], n['carril'], f, rango[i]) in ocupado:
            f += 1
        fila[i] = f
        ocupado.add((n['pool'], n['carril'], f, rango[i]))
        extra = 0
        for d, _ in n['sig']:
            if adelante(i, d) and mismo(i, d):
                salida[(i, d)] = f + extra
                extra += 1
        for rr in range(f + 1, f + extra):  # pasillo vertical bajo una compuerta que bifurca
            ocupado.add((*clave, rr, rango[i]))
    return fila


def caja_texto(texto, px=6.2, ancho_max=130, ancho_min=50, alto_linea=14):
    """Ancho y alto estimados de una etiqueta (Arial/Segoe UI de 11-12 px), con corte por palabras."""
    w = max(ancho_min, min(ancho_max, len(texto) * px + 8))
    lineas, actual = 1, 0.0
    for palabra in texto.split():
        largo = len(palabra) * px
        if actual and actual + px + largo > w - 6:
            lineas, actual = lineas + 1, largo
        else:
            actual += (px if actual else 0) + largo
    return w, alto_linea * lineas + 4


def cruza(p, q, caja, m=2):
    """¿El segmento ortogonal p-q pasa por el interior de la caja (x, y, w, h)?"""
    x, y, w, h = caja[0] + m, caja[1] + m, caja[2] - 2 * m, caja[3] - 2 * m
    if abs(p[0] - q[0]) < 0.5:
        return x < p[0] < x + w and max(min(p[1], q[1]), y) < min(max(p[1], q[1]), y + h)
    if abs(p[1] - q[1]) < 0.5:
        return y < p[1] < y + h and max(min(p[0], q[0]), x) < min(max(p[0], q[0]), x + w)
    return True


def trazar(nodos, orden_pools, carriles, mensajes):
    """Calcula toda la geometría. Devuelve formas, etiquetas, aristas y datos de carriles y pools."""
    sev = [i for i, n in nodos.items() if TIPOS[n['tipo']][0] == 'subProcess']
    principal = {i: n for i, n in nodos.items() if i not in sev}
    bordes = {i: n['adjunto'] for i, n in principal.items() if TIPOS[n['tipo']][0] == 'boundaryEvent'}
    para_rango = {i: dict(n, sig=[*n['sig'], *[(b, '') for b, h in bordes.items() if h == i]])
                  for i, n in principal.items()}
    rango, retorno = rangos(para_rango, mensajes)
    predecesores = {}
    for i, n in principal.items():
        for d, _ in n['sig']:
            predecesores.setdefault(d, []).append(i)
    alineado = {}  # destino de una rama de excepcion -> evento de borde sobre el que se alinea
    for b, h in bordes.items():
        rango[b] = rango[h]
        for d, _ in principal[b]['sig']:
            if predecesores.get(d) == [b]:
                rango[d] = rango[h]
                alineado[d] = b
    fila = filas(principal, rango, retorno, bordes) if principal else {}
    abiertos = [p for p in orden_pools if carriles[p]]
    cerrados = [p for p in orden_pools if not carriles[p]]
    ncol = max(rango.values()) + 1 if rango else 1
    x0 = POOL_X + CAB + 40
    cx = {i: x0 + rango[i] * COL + 50 for i in principal}

    # --- zona de subprocesos de evento: grilla bajo el flujo principal de cada carril; cada grupo ocupa celdas
    # contiguas de una misma fila si cabe
    ncel = max(3, int(ncol * COL // CELDA))
    celda, filas_sev = {}, {}
    por_carril = {}
    for i in sev:
        por_carril.setdefault((nodos[i]['pool'], nodos[i]['carril']), []).append(i)
    for k, ids in por_carril.items():
        bloques = {}
        for i in ids:
            bloques.setdefault(nodos[i]['grupo'] or f'_{i}', []).append(i)
        r = c = 0
        for miembros in bloques.values():
            if c and c + min(len(miembros), ncel) > ncel:
                r, c = r + 1, 0
            for i in miembros:
                if c >= ncel:
                    r, c = r + 1, 0
                celda[i] = (r, c)
                c += 1
            if len(miembros) > ncel:
                r, c = r + 1, 0
        filas_sev[k] = r + 1 if c else r
    for i, (r, c) in celda.items():
        cx[i] = x0 + c * CELDA + 110

    # --- mensajes con pools cerrados: lado de cada pool (los que envían, arriba; los que reciben, abajo)
    envia, recibe = {p: 0 for p in cerrados}, {p: 0 for p in cerrados}
    mcp = []  # mensajes nodo <-> pool cerrado
    for k, (a, b, nom) in enumerate(mensajes):
        if a in cerrados and b in nodos:
            envia[a] += 1
            mcp.append(dict(k=k, a=a, b=b, nom=nom, nodo=b, pool=a))
        elif b in cerrados and a in nodos:
            recibe[b] += 1
            mcp.append(dict(k=k, a=a, b=b, nom=nom, nodo=a, pool=b))
    lado = {p: ('arriba' if envia[p] >= recibe[p] and envia[p] else 'abajo') for p in cerrados}
    # un pool que recibe va arriba si su linea bajaria a traves de la zona de subprocesos de evento de su carril
    # desde un nodo intermedio del flujo; los eventos de fin conservan el lado inferior, porque las ramas de
    # excepcion alineadas bajo su actividad ocupan el camino hacia arriba y el trazado rodea la zona por el margen
    fin_sev = {}
    for i, (r, c) in celda.items():
        k = (nodos[i]['pool'], nodos[i]['carril'])
        fin_sev[k] = max(fin_sev.get(k, 0), x0 + (c + 1) * CELDA + 20)
    for m in mcp:
        n = nodos[m['nodo']]
        if lado[m['pool']] == 'abajo' and m['nodo'] in principal and TIPOS[n['tipo']][0] != 'endEvent' \
                and cx[m['nodo']] < fin_sev.get(
                (n['pool'], n['carril']), 0):
            lado[m['pool']] = 'arriba'
    for m in mcp:
        m['lado'] = lado[m['pool']]

    # --- bandas de pools cerrados: rango horizontal según los nodos con los que se comunican
    info = {}
    for p in cerrados:
        ms = sorted([m for m in mcp if m['pool'] == p], key=lambda m: cx[m['nodo']])
        slots = []
        for m in ms:
            slots.append(max(cx[m['nodo']], slots[-1] + SLOT) if slots else cx[m['nodo']])
        for m, s in zip(ms, slots):
            m['slot'] = s
        if not slots:
            slots = [x0 + 100]
        w_nom = len(p) * 7 + 60
        ini, fin = slots[0] - SLOT / 2, slots[-1] + SLOT / 2
        if fin - ini < w_nom:
            c = (ini + fin) / 2
            ini, fin = c - w_nom / 2, c + w_nom / 2
        if ini < POOL_X:
            ini, fin = POOL_X, fin + POOL_X - ini
        info[p] = dict(ini=ini, fin=fin, slots=slots, ms=ms, h=60, lado=lado[p])  # banda delgada (manual, p. 106-107)

    def bandas(ld):
        """Ubica los pools de un lado en filas de banda. Un pool puede correrse hacia un costado (con sus puntos de
        llegada) antes de pasar a una fila más alejada. Ninguna línea puede cruzar un pool de una fila más cercana."""
        ps = sorted([p for p in cerrados if lado[p] == ld], key=lambda p: info[p]['fin'] - info[p]['ini'])
        filas_b = []

        def admite(I, off, r):
            ini, fin, slots = I['ini'] + off, I['fin'] + off, [s + off for s in I['slots']]
            if ini < POOL_X:
                return False
            fila_r = filas_b[r] if r < len(filas_b) else []
            if any(not (fin + SEP_POOL <= info[q]['ini'] or info[q]['fin'] + SEP_POOL <= ini) for q in fila_r):
                return False
            if any(info[q]['ini'] - 5 <= s <= info[q]['fin'] + 135
                   for rr in range(min(r, len(filas_b))) for q in filas_b[rr] for s in slots):
                return False
            return not any(ini - 5 <= s <= fin + 135
                           for rr in range(r + 1, len(filas_b)) for q in filas_b[rr] for s in info[q]['slots'])

        for p in ps:
            I = info[p]
            puesto = False
            for r in range(len(filas_b) + 1):
                fila_r = filas_b[r] if r < len(filas_b) else []
                desplazamientos = [0]
                for q in fila_r:
                    desplazamientos += [info[q]['fin'] + SEP_POOL - I['ini'], info[q]['ini'] - SEP_POOL - I['fin']]
                for off in sorted(set(desplazamientos), key=abs):
                    if abs(off) <= 4 * SLOT and admite(I, off, r):
                        I['ini'] += off
                        I['fin'] += off
                        I['slots'] = [s + off for s in I['slots']]
                        for m in I['ms']:
                            m['slot'] += off
                        if r == len(filas_b):
                            filas_b.append([])
                        filas_b[r].append(p)
                        I['banda'] = r
                        puesto = True
                        break
                if puesto:
                    break
            if not puesto:
                filas_b.append([p])
                I['banda'] = len(filas_b) - 1
        return filas_b

    filas_banda = {ld: bandas(ld) for ld in ('arriba', 'abajo')}
    etq_msg = {m['k']: caja_texto(m['nom'], ancho_max=SLOT - 15, alto_linea=13) for m in mcp if m['nom']}
    n_lado = {ld: sum(1 for m in mcp if m['lado'] == ld) for ld in ('arriba', 'abajo')}

    def alto_lado(ld):
        if not filas_banda[ld]:
            return 0, [], []
        total = MARGEN_FAN + NIVEL * n_lado[ld]
        zonas, altos = [], []
        for r, fr in enumerate(filas_banda[ld]):
            z = 10 + max([etq_msg[m['k']][1] for p in fr for m in info[p]['ms'] if m['k'] in etq_msg] + [14])
            zonas.append(z)
            altos.append(max(info[p]['h'] for p in fr))
            total += z + altos[-1] + (SEP_POOL if r else 0)
        return total + 20, zonas, altos

    alto_arriba, zonas_arriba, altos_arriba = alto_lado('arriba')
    alto_abajo, zonas_abajo, altos_abajo = alto_lado('abajo')

    # --- pools abiertos, carriles y nodos
    y_abierto = 20 + alto_arriba
    filas_carril = {}
    for i, n in principal.items():
        k = (n['pool'], n['carril'])
        filas_carril[k] = max(filas_carril.get(k, 1), fila[i] + 1)
    alto_sev = {k: FILA_SEV * v + 20 for k, v in filas_sev.items()}
    def alto_texto(texto, ancho):
        return sum(caja_texto(x, ancho_max=ancho, ancho_min=ancho)[1] for x in texto.split('\n'))

    def bajo_nodo(i):
        """Alto ocupado bajo el centro del nodo por su etiqueta o sus documentos."""
        n = principal[i]
        et, _, _, h = TIPOS[n['tipo']]
        if n['docs']:
            return h / 2 + 16 + 38 + 34
        if et in ACTIVIDAD or et.endswith('Gateway') or not n['nombre']:
            return h / 2
        return h / 2 + 3 + caja_texto(n['nombre'], ancho_max=120)[1]

    alto_fila = {}
    for i, n in principal.items():
        k = (n['pool'], n['carril'], fila[i])
        req = FILA if n['docs'] else FILA_BAJA
        if i in bordes:
            req = max(req, NODO_Y + 40 + 22 + caja_texto(n['nombre'], ancho_max=80)[1] + 16)
        elif n['anotacion']:
            req = max(req, NODO_Y + bajo_nodo(i) + 12 + alto_texto(n['anotacion'], 140) + 20)
        alto_fila[k] = max(alto_fila.get(k, FILA_BAJA), req)

    def y_fila(p, c, r):
        """Desplazamiento vertical de la fila r dentro del carril: suma de los altos de las filas anteriores."""
        return sum(alto_fila.get((p, c, rr), FILA_BAJA) for rr in range(r))
    ancho = max([CAB + 40 + ncol * COL + 40, CAB + 40 + ncel * CELDA + 20 if sev else 0]
                + [info[p]['fin'] + 20 - POOL_X for p in cerrados])
    geo_pool, geo_carril, y = {}, {}, y_abierto
    for p in abiertos:
        y_ini = y
        for c in carriles[p]:
            alto = y_fila(p, c, filas_carril.get((p, c), 0 if (p, c) in alto_sev else 1)) + alto_sev.get((p, c), 0)
            geo_carril[(p, c)] = (POOL_X + CAB, y, ancho - CAB, alto)
            y += alto
        geo_pool[p] = (POOL_X, y_ini, ancho, y - y_ini)
        y += GAP_POOL
    y_fin_abierto = y - GAP_POOL

    caja = {}
    for i, n in principal.items():
        _, _, w, h = TIPOS[n['tipo']]
        cy = geo_carril[(n['pool'], n['carril'])][1] + y_fila(n['pool'], n['carril'], fila[i]) + NODO_Y
        caja[i] = (cx[i] - w / 2, cy - h / 2, w, h)
    centro = lambda i: (caja[i][0] + caja[i][2] / 2, caja[i][1] + caja[i][3] / 2)
    por_actividad, lado_borde = {}, {}
    for b, h in bordes.items():
        k = por_actividad.get(h, 0)
        por_actividad[h] = k + 1
        if k == 2:
            AVISOS_TRAZADO.append(f'{h}: mas de dos eventos de borde en una actividad; pueden superponerse')
        hx, hy, hw, hh = caja[h]
        lado_borde[b] = 'izquierda' if k % 2 else 'derecha'
        bcx = hx + hw / 2 + (1 if k % 2 == 0 else -1) * (36 + 34 * (k // 2))
        caja[b] = (bcx - 18, hy + hh - 18, 36, 36)
    for d, b in alineado.items():
        dx, dy, dw, dh = caja[d]
        caja[d] = (caja[b][0] + 18 - dw / 2, dy, dw, dh)

    def zona_top(i):
        k = (nodos[i]['pool'], nodos[i]['carril'])
        return geo_carril[k][1] + y_fila(*k, filas_carril.get(k, 0)) + 10 + celda[i][0] * FILA_SEV

    anotaciones, grupos, inicio_sev = {}, {}, {}
    for i in sev:
        # subproceso de evento expandido: marco punteado con su nombre y, dentro, el evento de inicio con el ícono del
        # disparador (manual BPMN, sec. 2.8.6, fig. 2.90, p. 97); su detalle se modela en su propio diagrama
        n = nodos[i]
        top = zona_top(i)
        left = cx[i] - 110
        caja[i] = (left + 10, top + 30, 200, 130)
        w_e, h_e = caja_texto(n['disparador'], ancho_max=130) if n['disparador'] else (0, 0)
        inicio_sev[i] = dict(caja=(left + 60, top + 66, 36, 36),
                             etq=(left + 78 - w_e / 2, top + 105, w_e, h_e) if n['disparador'] else None)
        if n['anotacion']:
            ancho_a = CELDA - 240
            anotaciones[i] = dict(texto=n['anotacion'], asoc=[(left + 210, top + 50), (left + 220, top + 50)],
                                  caja=(left + 220, top + 30, ancho_a,
                                        max(40, min(alto_texto(n['anotacion'], ancho_a), FILA_SEV - 44))))
        if n['grupo']:
            grupos.setdefault((n['pool'], n['carril'], n['grupo']), []).append(i)
    geo_grupo = {}
    for (p, c, g), ids in grupos.items():
        x1 = min(caja[i][0] for i in ids) - 8
        x2 = max(caja[i][0] for i in ids) + CELDA - 32
        y1 = min(zona_top(i) for i in ids) + 2
        y2 = max(zona_top(i) for i in ids) + FILA_SEV - 12
        geo_grupo[(p, c, g)] = dict(caja=(x1, y1, x2 - x1, y2 - y1), nombre=g, pool=p,
                                    etq=(x1 + 8, y1 + 5, min(x2 - x1 - 16, 320), 18))

    # --- objetos de datos y almacenes: centrados bajo la actividad
    datos = []
    for i, n in nodos.items():
        if TIPOS[n['tipo']][0] not in ACTIVIDAD or not n['docs']:
            continue
        bx, by, bw, bh = caja[i]
        nd = len(n['docs'])
        for k, (clase, dnom) in enumerate(n['docs']):
            dw, dh = (36, 36) if clase == 'almacen' else (30, 38)
            dxc = bx + bw / 2 + (k - (nd - 1) / 2) * 64
            d = dict(nodo=i, k=k, clase=clase, nombre=dnom, caja=(dxc - dw / 2, by + bh + 16, dw, dh))
            lw, lh = caja_texto(dnom, ancho_max=62, ancho_min=40)
            d['etq'] = (dxc - lw / 2, by + bh + 16 + dh + 2, lw, lh)
            if clase == 'entra':
                d['pts'] = [(dxc, by + bh + 16), (dxc, by + bh)]
            else:
                d['pts'] = [(dxc, by + bh), (dxc, by + bh + 16)]
            datos.append(d)
    for i, n in principal.items():
        if not n['anotacion']:
            continue
        if i in bordes:
            AVISOS_TRAZADO.append(f'{i}: la anotación de un evento de borde no se dibuja; se guarda como documentación')
            n['doc'] = '; '.join(x for x in [n['doc'], n['anotacion']] if x)
            continue
        bx, by, bw, bh = caja[i]
        cxn = bx + bw / 2
        ay = caja[i][1] + caja[i][3] / 2 + bajo_nodo(i) + 12
        asoc = ([(cxn - 45, by + bh), (cxn - 45, ay)] if TIPOS[n['tipo']][0] in ACTIVIDAD
                else [(bx + 8, by + bh - 6), (cxn - 50, ay)])
        anotaciones[i] = dict(texto=n['anotacion'], asoc=asoc,
                              caja=(cxn - 70, ay, 140, max(30, alto_texto(n['anotacion'], 140))))
    obstaculos = dict(caja)
    for d in datos:
        obstaculos[('dato', d['nodo'], d['k'])] = d['caja']
    for i, a in anotaciones.items():
        obstaculos[('ann', i)] = a['caja']
    for i, n in nodos.items():  # zona prevista de la etiqueta de eventos (abajo) y compuertas (arriba)
        et = TIPOS[n['tipo']][0]
        if et not in ACTIVIDAD and n['nombre']:
            bx, by, bw, bh = caja[i]
            w, h = caja_texto(n['nombre'], ancho_max=120)
            if et == 'boundaryEvent':
                w, h = caja_texto(n['nombre'], ancho_max=80)
                xe = bx + bw / 2 + 6 if lado_borde[i] == 'derecha' else bx + bw / 2 - 6 - w
                obstaculos[('etq', i)] = (xe, by + bh + 2, w, h)
                continue
            yb = by - h - 3 if et.endswith('Gateway') else by + bh + 3
            obstaculos[('etq', i)] = (bx + bw / 2 - w / 2, yb, w, h)
    # grupos de elementos del flujo principal: marco que envuelve a sus miembros con sus etiquetas y anotaciones
    generales = {}
    for i, n in principal.items():
        if n['grupo']:
            generales.setdefault((n['pool'], n['carril'], n['grupo']), []).append(i)
    for k, ids in generales.items():
        if k in geo_grupo:
            AVISOS_TRAZADO.append(f'grupo "{k[2]}": no puede reunir subprocesos de evento y elementos del flujo')
            continue
        cajas = [caja[i] for i in ids] + [obstaculos[('etq', i)] for i in ids if ('etq', i) in obstaculos]
        cajas += [anotaciones[i]['caja'] for i in ids if i in anotaciones]
        cajas += [d['caja'] for d in datos if d['nodo'] in ids] + [d['etq'] for d in datos if d['nodo'] in ids]
        x1 = min(c[0] for c in cajas) - 14
        y1 = min(c[1] for c in cajas) - 26
        x2 = max(c[0] + c[2] for c in cajas) + 14
        y2 = max(c[1] + c[3] for c in cajas) + 12
        geo_grupo[k] = dict(caja=(x1, y1, x2 - x1, y2 - y1), nombre=k[2], pool=k[0],
                            etq=(x1 + 8, y1 + 4, min(x2 - x1 - 16, 320), 18))
        grupos[k] = ids
        for j in principal:
            if j not in ids and j not in bordes:
                jx, jy, jw, jh = caja[j]
                if x1 < jx + jw / 2 < x2 and y1 < jy + jh / 2 < y2:
                    AVISOS_TRAZADO.append(f'grupo "{k[2]}": el elemento {j} queda dentro del marco sin ser miembro')
    # los marcos de grupo tampoco se atraviesan, salvo por los flujos de sus propios miembros
    marcos = [(G['caja'], set(grupos[k])) for k, G in geo_grupo.items()]

    def libre(pts, excluir=()):
        for p, q in zip(pts, pts[1:]):
            for k, b in obstaculos.items():
                if k in excluir or (isinstance(k, tuple) and k[1] in excluir):
                    continue
                if cruza(p, q, b, -8 if k in caja else -3):
                    return False
            for b, miembros in marcos:
                if not miembros & set(excluir) and cruza(p, q, b, -3):
                    return False
        return True

    def costo(pts, excluir=()):
        c = 0
        for p, q in zip(pts, pts[1:]):
            for k, b in obstaculos.items():
                if k in excluir or (isinstance(k, tuple) and k[1] in excluir):
                    continue
                if cruza(p, q, b, -8 if k in caja else -3):
                    c += 10 if k in caja else 1
            for b, miembros in marcos:
                if not miembros & set(excluir) and cruza(p, q, b, -3):
                    c += 1
        return c

    def fila_top(i):
        return geo_carril[(nodos[i]['pool'], nodos[i]['carril'])][1] + y_fila(nodos[i]['pool'], nodos[i]['carril'],
                                                                                    fila[i])

    canales = {}  # uso de canales verticales y horizontales, para separar líneas paralelas

    def canal(clave, base, paso=6):
        k = canales.get(clave, 0)
        canales[clave] = k + 1
        return base + paso * ((k + 1) // 2) * (1 if k % 2 else -1) if k else base

    # --- flujos de secuencia
    flujos, rutas = [], {}
    for i, n in nodos.items():
        for d, cond in n['sig']:
            flujos.append((gid('flujo', i, d), i, d, cond))
    es_comp = lambda i: TIPOS[nodos[i]['tipo']][0].endswith('Gateway')
    sale_vertical = lambda i: es_comp(i) or i in bordes
    for fid, a, b, cond in flujos:
        ax, ay, aw, ah = caja[a]
        bx, by, bw, bh = caja[b]
        (acx, acy), (bcx, bcy) = centro(a), centro(b)
        exc = (a, b)
        cand = []
        if ((a, b) in retorno or rango[b] <= rango[a]) and alineado.get(b) != a:
            yc = canal(('retorno', min(fila_top(a), fila_top(b))), min(ay, by) - 16)
            if es_comp(a):
                cand.append([(acx, ay), (acx, yc), (bcx, yc), (bcx, by)])
            else:
                xs = canal(('v', round(ax + aw + 16)), ax + aw + 16)
                cand.append([(ax + aw, acy), (xs, acy), (xs, yc), (bcx, yc), (bcx, by)])
        elif abs(acy - bcy) < 0.5:
            cand.append([(ax + aw, acy), (bx, bcy)])
            yc = canal(('h', round(fila_top(a))), fila_top(a) + 10)
            cand.append([(ax + aw, acy), (ax + aw + 14, acy), (ax + aw + 14, yc), (bx - 14, yc), (bx - 14, bcy),
                         (bx, bcy)])
        else:
            abajo = bcy > acy
            if abs(acx - bcx) < 1 and abajo:
                cand.append([(acx, ay + ah), (bcx, by)])
            if sale_vertical(a):
                ya = ay + ah if abajo else ay
                cand.append([(acx, ya), (acx, bcy), (bx, bcy)])
            if es_comp(b):
                yb = by if abajo else by + bh
                cand.append([(ax + aw, acy), (bcx, acy), (bcx, yb)])
            xm = canal(('v', round(bx - 18)), bx - 18)
            cand.append([(ax + aw, acy), (xm, acy), (xm, bcy), (bx, bcy)])
            xm = canal(('v', round(ax + aw + 18)), ax + aw + 18)
            cand.append([(ax + aw, acy), (xm, acy), (xm, bcy), (bx, bcy)])
        libres = [c for c in cand if libre(c, exc)]
        rutas[fid] = libres[0] if libres else min(cand, key=lambda c: costo(c, exc))

    # --- mensajes nodo <-> pool cerrado
    lado_y = {'arriba': y_abierto, 'abajo': y_fin_abierto}
    puertos = {}
    for m in mcp:
        puertos.setdefault((m['nodo'], m['lado']), []).append(m)
    for (i, ld), ms in puertos.items():
        ms.sort(key=lambda m: m['slot'])
        bx, by, bw, bh = caja[i]
        es_act = TIPOS[nodos[i]['tipo']][0] in ACTIVIDAD
        for k, m in enumerate(ms):
            m['px'] = bx + bw * (k + 1) / (len(ms) + 1) if es_act else bx + bw / 2 + (k - (len(ms) - 1) / 2) * 12
            m['py'] = by if ld == 'arriba' else by + bh
    huecos = [x0 + c * COL + 135 for c in range(-1, ncol)] + [x0 + c * CELDA + CELDA - 11 for c in range(-1, ncel)]
    niveles = {'arriba': 0, 'abajo': 0}
    rutas_msg, etq_m = {}, {}
    for m in sorted(mcp, key=lambda m: (m['lado'], m['slot'])):
        ld, i = m['lado'], m['nodo']
        signo = -1 if ld == 'arriba' else 1
        borde = lado_y[ld]
        px, py = m['px'], m['py']
        pts = [(px, py)]
        if not libre([(px, py), (px, borde)], (i,)):
            yj = py + signo * 9
            for gx0 in sorted(huecos, key=lambda g: abs(g - px)):
                gx = canal(('v', round(gx0)), gx0)
                if libre([(px, yj), (gx, yj)], (i,)) and libre([(gx, yj), (gx, borde)], (i,)):
                    pts += [(px, yj), (gx, yj)]
                    break
        I = info[m['pool']]
        nivel = niveles[ld]
        niveles[ld] += 1
        yf = borde + signo * (MARGEN_FAN + NIVEL * nivel)
        xl = pts[-1][0]
        if abs(xl - m['slot']) > 0.5:
            pts += [(xl, yf), (m['slot'], yf)]
        m['pts_nodo'] = pts
        rutas_msg[m['k']] = m

    # posición vertical de las bandas (ya conocido el alto de cada zona)
    geo_cerrado = {}
    for ld, zonas, altos in (('arriba', zonas_arriba, altos_arriba), ('abajo', zonas_abajo, altos_abajo)):
        signo = -1 if ld == 'arriba' else 1
        cursor = lado_y[ld] + signo * (MARGEN_FAN + NIVEL * n_lado[ld])
        for r, fr in enumerate(filas_banda[ld]):
            if r:
                cursor += signo * SEP_POOL
            zona_ini = cursor
            cursor += signo * zonas[r]
            for p in fr:
                I = info[p]
                if ld == 'abajo':
                    geo_cerrado[p] = (I['ini'], cursor, I['fin'] - I['ini'], I['h'])
                else:
                    geo_cerrado[p] = (I['ini'], cursor - I['h'], I['fin'] - I['ini'], I['h'])
                I['zona'] = (min(zona_ini, cursor), abs(cursor - zona_ini))
            cursor += signo * altos[r]
    for k, m in rutas_msg.items():
        g = geo_cerrado[m['pool']]
        ld = m['lado']
        y_pool = g[1] + g[3] if ld == 'arriba' else g[1]
        pts = m['pts_nodo'] + [(m['slot'], y_pool)]
        if m['a'] == m['pool']:
            pts = pts[::-1]
        m['pts'] = [p for j, p in enumerate(pts) if j == 0 or p != pts[j - 1]]
        if k in etq_msg:
            w, h = etq_msg[k]
            zy, zh = info[m['pool']]['zona']
            etq_m[k] = (m['slot'] + 5, zy + (zh - h) / 2, w, h)

    # --- mensajes nodo <-> nodo (entre pools abiertos) y pool <-> pool
    for k, (a, b, nom) in enumerate(mensajes):
        if k in rutas_msg:
            continue
        if a in nodos and b in nodos:
            (sxc, syc), (txc, tyc) = centro(a), centro(b)
            abajo = tyc > syc
            ys = caja[a][1] + caja[a][3] if abajo else caja[a][1]
            yt = caja[b][1] if abajo else caja[b][1] + caja[b][3]
            ym = (ys + yt) / 2
            pts = [(sxc, ys), (sxc, ym), (txc, ym), (txc, yt)] if abs(sxc - txc) > 0.5 else [(sxc, ys), (txc, yt)]
        else:
            ga = caja.get(a) or geo_pool.get(a) or geo_cerrado.get(a)
            gb = caja.get(b) or geo_pool.get(b) or geo_cerrado.get(b)
            xa = ga[0] + ga[2] / 2
            pts = [(xa, ga[1] + ga[3]), (xa, gb[1])] if gb[1] > ga[1] else [(xa, ga[1]), (xa, gb[1] + gb[3])]
        rutas_msg[k] = dict(k=k, a=a, b=b, nom=nom, pts=pts)
        if nom:
            w, h = caja_texto(nom, ancho_max=SLOT - 15, alto_linea=13)
            etq_m[k] = (pts[1][0] + 5, (pts[1][1] + pts[-2][1]) / 2 - h / 2, w, h)

    # --- etiquetas de nodos: del lado libre de conexiones
    lados_usados = {i: set() for i in nodos}

    def marcar(i, p):
        bx, by, bw, bh = caja[i]
        if abs(p[1] - by) < 1:
            lados_usados[i].add('arriba')
        elif abs(p[1] - (by + bh)) < 1:
            lados_usados[i].add('abajo')
    for fid, a, b, _ in flujos:
        marcar(a, rutas[fid][0])
        marcar(b, rutas[fid][-1])
    for m in rutas_msg.values():
        if m['a'] in nodos:
            marcar(m['a'], m['pts'][0])
        if m['b'] in nodos:
            marcar(m['b'], m['pts'][-1])
    etq_n = {}
    for i, n in nodos.items():
        bx, by, bw, bh = caja[i]
        et = TIPOS[n['tipo']][0]
        if et in ACTIVIDAD:
            etq_n[i] = caja[i]
            continue
        if not n['nombre']:
            continue
        w, h = caja_texto(n['nombre'], ancho_max=120)
        if i in bordes:
            w, h = caja_texto(n['nombre'], ancho_max=80)
            etq_n[i] = (bx + bw / 2 + 6 if lado_borde[i] == 'derecha' else bx + bw / 2 - 6 - w, by + bh + 2, w, h)
            continue
        preferido = ['arriba', 'abajo'] if et.endswith('Gateway') else ['abajo', 'arriba']
        libres = [s for s in preferido if s not in lados_usados[i]]
        lado_e = libres[0] if libres else 'derecha'
        if lado_e == 'arriba':
            etq_n[i] = (bx + bw / 2 - w / 2, by - h - 3, w, h)
        elif lado_e == 'abajo':
            etq_n[i] = (bx + bw / 2 - w / 2, by + bh + 3, w, h)
        else:
            etq_n[i] = (bx + bw + 4, by - h, w, h)

    # --- etiquetas de condiciones en flujos
    etq_f = {}
    for fid, a, b, cond in flujos:
        if not cond:
            continue
        p, q = rutas[fid][0], rutas[fid][1]
        w, h = caja_texto(cond, px=6, ancho_max=90, ancho_min=18)
        if abs(p[0] - q[0]) < 0.5:
            # salida vertical de compuerta: la etiqueta va junto al tramo horizontal de su rama
            etq_f[fid] = (q[0] + 6, q[1] - h - 2, w, h) if len(rutas[fid]) > 2 else (
                p[0] + 5, p[1] + (4 if q[1] > p[1] else -h - 4), w, h)
        else:
            etq_f[fid] = (p[0] + 5, p[1] - h - 2, w, h)

    return dict(anotaciones=anotaciones, geo_grupo=geo_grupo, sev=sev, bordes=bordes, inicio_sev=inicio_sev,
                rango=rango, retorno=retorno, caja=caja, datos=datos, flujos=flujos, rutas=rutas,
                rutas_msg=rutas_msg, etq_n=etq_n, etq_f=etq_f, etq_m=etq_m, geo_pool=geo_pool,
                geo_carril=geo_carril, geo_cerrado=geo_cerrado, abiertos=abiertos, cerrados=cerrados)


def definicion(defn, base, condicion=''):
    """Definición de evento BPMN; la condicional exige una expresión, que aquí es el texto de la condición."""
    if defn == 'conditional':
        return (f'<bpmn:conditionalEventDefinition id="{base}_def"><bpmn:condition xsi:type="bpmn:tFormalExpression">'
                f'{condicion}</bpmn:condition></bpmn:conditionalEventDefinition>')
    return f'<bpmn:{defn}EventDefinition id="{base}_def" />'


def generar(nombre, nodos, orden_pools, carriles, mensajes, origen=''):
    T = trazar(nodos, orden_pools, carriles, mensajes)
    # los identificadores se derivan del nombre del archivo (contiene el código del proceso) y del ID de cada
    # elemento, no del título: cambiar el título no cambia los identificadores (estándar de artefactos, regla 7.4)
    semilla = os.path.splitext(origen)[0] if origen else nombre
    caja, rutas = T['caja'], T['rutas']

    def bounds(x, yy, w, h):
        return f'<dc:Bounds x="{x:.0f}" y="{yy:.0f}" width="{w:.0f}" height="{h:.0f}" />'

    def wp(puntos):
        return ''.join(f'<di:waypoint x="{a:.0f}" y="{b:.0f}" />' for a, b in puntos)

    def etiqueta(b):
        return f'<bpmndi:BPMNLabel>{bounds(*b)}</bpmndi:BPMNLabel>' if b else ''

    pid = {p: gid(semilla, 'pool', p) for p in orden_pools}
    prc = {p: gid(semilla, 'proc', p) for p in orden_pools}
    nid = {i: gid(semilla, 'nodo', i) for i in nodos}
    raiz, coll, procs, formas, aristas = [], [], {p: [] for p in orden_pools}, [], []
    entradas = {i: [] for i in nodos}
    salidas = {i: [] for i in nodos}
    fids = {}
    for fid0, a, b, cond in T['flujos']:
        fid = gid(semilla, 'flujo', a, b)
        fids[fid0] = fid
        salidas[a].append(fid)
        entradas[b].append(fid)
    for p in orden_pools:
        # los pools cerrados no llevan proceso en el BPMN estándar; la copia para Bizagi se lo agrega
        ref = f' processRef="{prc[p]}"' if carriles[p] else ''
        coll.append(f'<bpmn:participant id="{pid[p]}" name={quoteattr(p)}{ref} />')
        g = T['geo_pool'].get(p) or T['geo_cerrado'].get(p)
        formas.append(f'<bpmndi:BPMNShape id="{pid[p]}_di" bpmnElement="{pid[p]}" isHorizontal="true">'
                      f'{bounds(*g)}</bpmndi:BPMNShape>')
    for k, m in sorted(T['rutas_msg'].items()):
        a, b, nom = m['a'], m['b'], m['nom']
        mid = gid(semilla, 'msj', a, b, str(k))
        src = nid.get(a, pid.get(a))
        tgt = nid.get(b, pid.get(b))
        coll.append(f'<bpmn:messageFlow id="{mid}" name={quoteattr(nom)} sourceRef="{src}" targetRef="{tgt}" />')
        aristas.append(f'<bpmndi:BPMNEdge id="{mid}_di" bpmnElement="{mid}">{wp(m["pts"])}'
                       f'{etiqueta(T["etq_m"].get(k))}</bpmndi:BPMNEdge>')
    almacenes = {}
    categorias = []
    datos_por_nodo = {}
    for d in T['datos']:
        datos_por_nodo.setdefault(d['nodo'], []).append(d)
    for p in T['abiertos']:
        cuerpo = procs[p]
        lanes = []
        for c in carriles[p]:
            refs = ''.join(f'<bpmn:flowNodeRef>{nid[i]}</bpmn:flowNodeRef>' for i, n in nodos.items()
                           if n['pool'] == p and n['carril'] == c)
            lid = gid(semilla, 'carril', p, c)
            lanes.append(f'<bpmn:lane id="{lid}" name={quoteattr(c)}>{refs}</bpmn:lane>')
            formas.append(f'<bpmndi:BPMNShape id="{lid}_di" bpmnElement="{lid}" isHorizontal="true">'
                          f'{bounds(*T["geo_carril"][(p, c)])}</bpmndi:BPMNShape>')
        cuerpo.append(f'<bpmn:laneSet id="{prc[p]}_ls">{"".join(lanes)}</bpmn:laneSet>')
        artefactos = []
        for i, n in [(i, n) for i, n in nodos.items() if n['pool'] == p]:
            et, defn, w, h = TIPOS[n['tipo']]
            hijos = f'<bpmn:documentation>{escape(n["doc"])}</bpmn:documentation>' if n['doc'] else ''
            hijos += ''.join(f'<bpmn:incoming>{f}</bpmn:incoming>' for f in entradas[i])
            hijos += ''.join(f'<bpmn:outgoing>{f}</bpmn:outgoing>' for f in salidas[i])
            asoc = ''
            ds = datos_por_nodo.get(i, [])
            if any(d['clase'] == 'entra' for d in ds):
                hijos += f'<bpmn:property id="{nid[i]}_ph" name="__targetRef_placeholder" />'
            for d in ds:
                k, clase, dnom = d['k'], d['clase'], d['nombre']
                did = gid(semilla, 'dato', i, str(k))
                aid = gid(semilla, 'asoc', i, str(k))
                if clase == 'almacen':
                    if dnom not in almacenes:
                        almacenes[dnom] = gid(semilla, 'almacen', dnom)
                        raiz.append(f'<bpmn:dataStore id="{almacenes[dnom]}" name={quoteattr(dnom)} />')
                    artefactos.append(f'<bpmn:dataStoreReference id="{did}" name={quoteattr(dnom)} '
                                      f'dataStoreRef="{almacenes[dnom]}" />')
                else:
                    artefactos.append(f'<bpmn:dataObject id="{did}_do" />')
                    artefactos.append(f'<bpmn:dataObjectReference id="{did}" name={quoteattr(dnom)} '
                                      f'dataObjectRef="{did}_do" />')
                formas.append(f'<bpmndi:BPMNShape id="{did}_di" bpmnElement="{did}">{bounds(*d["caja"])}'
                              f'{etiqueta(d["etq"])}</bpmndi:BPMNShape>')
                if clase == 'entra':
                    asoc += (f'<bpmn:dataInputAssociation id="{aid}"><bpmn:sourceRef>{did}</bpmn:sourceRef>'
                             f'<bpmn:targetRef>{nid[i]}_ph</bpmn:targetRef></bpmn:dataInputAssociation>')
                else:
                    asoc += (f'<bpmn:dataOutputAssociation id="{aid}"><bpmn:targetRef>{did}</bpmn:targetRef>'
                             f'</bpmn:dataOutputAssociation>')
                aristas.append(f'<bpmndi:BPMNEdge id="{aid}_di" bpmnElement="{aid}">{wp(d["pts"])}</bpmndi:BPMNEdge>')
            hijos += asoc
            if n['marcador']:
                hijos += MARCADORES[n['marcador']]
            atributos = ''
            if n['defecto']:
                atributos += f' default="{fids[gid("flujo", i, n["defecto"])]}"'
            if et == 'boundaryEvent':
                atributos += (f' attachedToRef="{nid[n["adjunto"]]}" '
                              f'cancelActivity="{"true" if n["interrumpe"] else "false"}"')
            if et == 'subProcess':
                # subproceso de evento expandido: su evento de inicio sin interrupción lleva el disparador
                cond = escape(n['disparador'] or n['nombre'])
                hijos += (f'<bpmn:startEvent id="{nid[i]}_ini" name={quoteattr(n["disparador"])} '
                          f'isInterrupting="false">{definicion(defn, nid[i] + "_ini", cond)}</bpmn:startEvent>')
                cuerpo.append(f'<bpmn:subProcess id="{nid[i]}" name={quoteattr(n["nombre"])} triggeredByEvent="true">'
                              f'{hijos}</bpmn:subProcess>')
                ini = T['inicio_sev'][i]
                formas.append(f'<bpmndi:BPMNShape id="{nid[i]}_ini_di" bpmnElement="{nid[i]}_ini">'
                              f'{bounds(*ini["caja"])}{etiqueta(ini["etq"])}</bpmndi:BPMNShape>')
            else:
                if defn:
                    hijos += definicion(defn, nid[i], escape(n['nombre']))
                cuerpo.append(f'<bpmn:{et} id="{nid[i]}" name={quoteattr(n["nombre"])}{atributos}>{hijos}</bpmn:{et}>')
            extra = ' isMarkerVisible="true"' if et == 'exclusiveGateway' else (
                ' isExpanded="false"' if et == 'callActivity' else (' isExpanded="true"' if et == 'subProcess' else ''))
            formas.append(f'<bpmndi:BPMNShape id="{nid[i]}_di" bpmnElement="{nid[i]}"{extra}>{bounds(*caja[i])}'
                          f'{etiqueta(T["etq_n"].get(i))}</bpmndi:BPMNShape>')
        for fid0, a, b, cond in T['flujos']:
            if nodos[a]['pool'] != p:
                continue
            fid = fids[fid0]
            cuerpo.append(f'<bpmn:sequenceFlow id="{fid}" name={quoteattr(cond)} sourceRef="{nid[a]}" '
                          f'targetRef="{nid[b]}" />')
            aristas.append(f'<bpmndi:BPMNEdge id="{fid}_di" bpmnElement="{fid}">{wp(rutas[fid0])}'
                           f'{etiqueta(T["etq_f"].get(fid0))}</bpmndi:BPMNEdge>')
        for i, a in T['anotaciones'].items():
            if nodos[i]['pool'] != p:
                continue
            aid, sid = gid(semilla, 'anotacion', i), gid(semilla, 'asocnota', i)
            artefactos.append(f'<bpmn:textAnnotation id="{aid}"><bpmn:text>{escape(a["texto"])}</bpmn:text>'
                              f'</bpmn:textAnnotation>')
            artefactos.append(f'<bpmn:association id="{sid}" sourceRef="{nid[i]}" targetRef="{aid}" '
                              'associationDirection="None" />')
            formas.append(f'<bpmndi:BPMNShape id="{aid}_di" bpmnElement="{aid}">{bounds(*a["caja"])}</bpmndi:BPMNShape>')
            aristas.append(f'<bpmndi:BPMNEdge id="{sid}_di" bpmnElement="{sid}">{wp(a["asoc"])}</bpmndi:BPMNEdge>')
        for (pg, _, g), G in T['geo_grupo'].items():
            if pg != p:
                continue
            gid_g, cv = gid(semilla, 'grupo', pg, g), gid(semilla, 'categoria', pg, g)
            categorias.append(f'<bpmn:categoryValue id="{cv}" value={quoteattr(g)} />')
            artefactos.append(f'<bpmn:group id="{gid_g}" categoryValueRef="{cv}" />')
            formas.append(f'<bpmndi:BPMNShape id="{gid_g}_di" bpmnElement="{gid_g}">{bounds(*G["caja"])}'
                          f'{etiqueta(G["etq"])}</bpmndi:BPMNShape>')
        cuerpo.extend(artefactos)
    did = gid(semilla, 'defs')[1:9]
    if categorias:
        raiz.append(f'<bpmn:category id="Cat_{did}">{"".join(categorias)}</bpmn:category>')
    procesos = ''.join(f'<bpmn:process id="{prc[p]}" name={quoteattr(p)} isExecutable="false">{"".join(procs[p])}'
                       f'</bpmn:process>' for p in T['abiertos'])
    aviso = (f'<!-- GENERADO con tabla_a_bpmn.py desde {escape(origen).replace('--', '-')}. En la etapa formal este BPMN pasa a ser la '
             'fuente maestra y se edita directamente. -->\n') if origen else ''
    return ('<?xml version="1.0" encoding="UTF-8"?>\n' + aviso +
            '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
            'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" '
            'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            f'id="Defs_{did}" targetNamespace="http://bpmn.tabla/{did}" exporter="_tabla_a_bpmn.py" '
            'exporterVersion="3.0">'
            + ''.join(raiz)
            + f'<bpmn:collaboration id="Collab_{did}">{"".join(coll)}</bpmn:collaboration>'
            + procesos
            + f'<bpmndi:BPMNDiagram id="Diag_{did}" name={quoteattr(nombre)}>'
            f'<bpmndi:BPMNPlane id="Plane_{did}" bpmnElement="Collab_{did}">{"".join(formas)}{"".join(aristas)}'
            '</bpmndi:BPMNPlane></bpmndi:BPMNDiagram></bpmn:definitions>\n')


VISOR = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__T__</title>
<link rel="stylesheet" href="https://unpkg.com/bpmn-js@17.11.1/dist/assets/diagram-js.css">
<link rel="stylesheet" href="https://unpkg.com/bpmn-js@17.11.1/dist/assets/bpmn-js.css">
<link rel="stylesheet" href="https://unpkg.com/bpmn-js@17.11.1/dist/assets/bpmn-font/css/bpmn.css">
<style>html,body{margin:0;height:100%;font:14px Arial,sans-serif;background:#fff}#c{height:calc(100% - 34px)}
header{padding:8px 12px;border-bottom:1px solid #ddd}.bjs-drilldown{display:none}</style></head>
<body><header>__T__ · vista generada por _tabla_a_bpmn.py (rueda: zoom; arrastrar: mover)</header><div id="c"></div>
<script src="https://unpkg.com/bpmn-js@17.11.1/dist/bpmn-navigated-viewer.production.min.js"></script>
<script>const xml = __X__; const v = new BpmnJS({container: '#c'});
v.importXML(xml).then(r => { window.listo = true; window.avisos = r.warnings.length; v.get('canvas').zoom('fit-viewport'); })
 .catch(e => { document.body.insertAdjacentHTML('beforeend', '<pre>' + e + '</pre>'); window.listo = true; });</script>
</body></html>
"""


def visor_html(nombre, xml):
    """Vista rápida: bpmn-js local fijado y colores de estilo Bizagi; si no hay copia local, bpmn-js desde internet."""
    try:
        sys.path.insert(0, AQUI)
        import renderizar_bpmn
        return renderizar_bpmn.pagina_visor(nombre, xml)
    except Exception as error:
        print(f'Vista rápida en línea (sin bpmn-js local: {error})')
        return VISOR.replace('__T__', escape(nombre)).replace('__X__', __import__('json').dumps(xml))


def ejecutar(script, *args):
    r = subprocess.run([sys.executable, auxiliar(script), *args], capture_output=True, text=True, encoding='utf-8',
                       check=False)
    return ((r.stdout or '') + (r.stderr or '')).strip()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) not in (1, 2):
        sys.exit(__doc__)
    ruta = args[0]
    if not os.path.exists(ruta) and os.path.exists(os.path.join(AQUI, ruta)):
        ruta = os.path.join(AQUI, ruta)  # permite correr las plantillas desde cualquier carpeta
    if not os.path.exists(ruta):
        sys.exit(f'No existe el archivo de entrada: {ruta}')
    base = re.sub(r'[^\w\-]+', '_', os.path.splitext(os.path.basename(ruta))[0]).strip('_')
    salida = args[1] if len(args) == 2 else os.path.join(AQUI, 'salida', base)
    os.makedirs(salida, exist_ok=True)
    nombre, nodos, orden_pools, carriles, mensajes, avisos = leer(ruta)
    for a in avisos:
        print('AVISO: ' + a)
    destino = os.path.join(salida, base + '.bpmn')
    with open(destino, 'w', encoding='utf-8', newline='\n') as f:
        f.write(generar(nombre, nodos, orden_pools, carriles, mensajes, os.path.basename(ruta)))
    for a in AVISOS_TRAZADO:
        print('AVISO: ' + a)
    avisos += AVISOS_TRAZADO
    print(f'BPMN: {destino} ({len(nodos)} elementos, {len(orden_pools)} pools, {len(mensajes)} mensajes)')
    informe = '\n'.join(ejecutar(s, destino) for s in ('_validar_bpmn.py', '_revisar_trazado.py', '_revisar_notacion.py'))
    if avisos:
        informe += '\nAvisos de la entrada:\n' + '\n'.join('    ' + a for a in avisos)
    with open(os.path.join(salida, 'validacion.txt'), 'w', encoding='utf-8') as f:
        f.write(informe + '\n')
    print('Validación:\n' + informe.strip())
    if '--sin-bizagi' not in sys.argv:
        print('Copia para Bizagi: ' + ejecutar('_bpmn_a_bizagi.py', destino, os.path.join(salida, 'bizagi')))
    if '--sin-visor' not in sys.argv:
        with open(destino, encoding='utf-8') as f:
            xml = f.read()
        html = visor_html(nombre, xml)
        with open(os.path.join(salida, base + '_visor.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print('Vista rápida: ' + os.path.join(salida, base + '_visor.html'))


if __name__ == '__main__':
    main()
