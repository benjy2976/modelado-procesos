"""Regresiones del trazado compacto: ejecutar con python -m unittest discover -s 05-herramientas/gestor-modelos -p test_zigzag.py."""
import copy
import tempfile
import unittest
from pathlib import Path

from lxml import etree
import tabla_a_bpmn as modelo
from _revisar_trazado import revisar


RAIZ = Path(__file__).resolve().parents[2]
AREA = RAIZ / '02-procesos/S4-gestion-de-las-inversiones/S4-3-ejecucion-inversion/S4-3-2-ejecucion'


def semantica(xml):
    raiz = etree.fromstring(xml.encode('utf-8'))
    for diagrama in raiz.findall('{http://www.omg.org/spec/BPMN/20100524/DI}BPMNDiagram'):
        raiz.remove(diagrama)
    return etree.tostring(raiz, method='c14n')


class ZigzagTests(unittest.TestCase):
    def test_simplificacion_conserva_extremos_y_ortogonalidad(self):
        ruta = [(0, 0), (0, 5), (0, 3), (0, 3), (8, 3), (8, 10)]
        self.assertEqual(modelo.simplificar_ruta(ruta), [(0, 0), (0, 3), (8, 3), (8, 10)])

    def test_conflictos_distingue_cruce_solape_y_contacto(self):
        self.assertEqual(modelo.conflictos_rutas([(0, 5), (10, 5)], [[(5, 0), (5, 10)]]), (0, 1))
        self.assertEqual(modelo.conflictos_rutas([(0, 5), (10, 5)], [[(5, 5), (15, 5)]]), (5, 0))
        self.assertEqual(modelo.conflictos_rutas([(0, 5), (10, 5)], [[(10, 5), (10, 10)]]), (0, 0))

    def test_ocho_subprocesos_conservan_semantica_y_no_aumentan_d4(self):
        tablas = sorted(AREA.glob('*/*-diagrama-proceso-tabla.md'))
        self.assertEqual(len(tablas), 8)
        for tabla in tablas:
            numero = int(tabla.name.split('-')[3])
            with self.subTest(proceso=numero):
                nombre, nodos, pools, carriles, mensajes, _, perfil = modelo.leer(str(tabla))
                def generar(p):
                    return modelo.generar(nombre, copy.deepcopy(nodos), pools, carriles, mensajes, tabla.name, p)
                xml = generar(perfil)
                self.assertEqual(xml, generar(perfil))
                self.assertEqual(semantica(xml), semantica(generar('normal')))
                configuracion = modelo.PERFILES_TRAZADO[perfil]
                anterior = configuracion.copy()
                try:
                    configuracion['compactar_filas_carril'] = False
                    configuracion['recolocar_terminales'] = False
                    configuracion['rutas_seguras'] = False
                    xml_anterior = generar(perfil)
                finally:
                    configuracion.clear()
                    configuracion.update(anterior)
                self.assertEqual(semantica(xml), semantica(xml_anterior))
                with tempfile.TemporaryDirectory() as carpeta:
                    destino = Path(carpeta) / 'modelo.bpmn'
                    destino.write_text(xml, encoding='utf-8')
                    hallazgos = revisar(str(destino))
                    destino.write_text(xml_anterior, encoding='utf-8')
                    previos = revisar(str(destino))
                    for tipo in set(hallazgos) | set(previos):
                        self.assertLessEqual(len(hallazgos.get(tipo, [])), len(previos.get(tipo, [])), hallazgos)

    def test_corredor_rodea_barrera_y_no_atraviesa_extremos(self):
        barreras = [(0,0,40,40),(180,0,40,40),(80,-30,40,100)]
        ruta = modelo.ruta_ortogonal_libre((40,20),(180,20),barreras)
        self.assertIsNotNone(ruta)
        self.assertEqual(ruta[0],(40,20))
        self.assertEqual(ruta[-1],(180,20))
        self.assertFalse(any(modelo.cruza(a,b,r,0) for a,b in zip(ruta,ruta[1:]) for r in barreras))
        self.assertIsNone(modelo.ruta_ortogonal_libre((20,20),(180,20),barreras))

    def test_terminales_suben_juntas_y_conexiones_no_atraviesan_cajas(self):
        tabla = next(AREA.glob('*/S4-3-2-3-diagrama-proceso-tabla.md'))
        _, nodos, pools, carriles, mensajes, _, perfil = modelo.leer(str(tabla))
        actual = modelo.trazar(copy.deepcopy(nodos), pools, carriles, mensajes, perfil)
        config = modelo.PERFILES_TRAZADO[perfil]
        try:
            config['recolocar_terminales'] = False
            anterior = modelo.trazar(copy.deepcopy(nodos), pools, carriles, mensajes, perfil)
        finally:
            config['recolocar_terminales'] = True
        for i in ('E-T11','E-F1'):
            self.assertLess(actual['caja'][i][1],anterior['caja'][i][1])
        a,b = (actual['caja'][i] for i in ('E-T11','E-F1'))
        self.assertEqual(a[1]+a[3]/2,b[1]+b[3]/2)
        rutas = list(actual['rutas'].values())+[m['pts'] for m in actual['rutas_msg'].values()]
        self.assertFalse(any(modelo.cruza(u,v,rect,0) for ruta in rutas
                             for u,v in zip(ruta,ruta[1:]) for rect in actual['caja'].values()))

    def test_adicionales_compacta_carriles_sin_cambiar_ancho_ni_cajas(self):
        tabla = next(AREA.glob('*/S4-3-2-3-diagrama-proceso-tabla.md'))
        _, nodos, pools, carriles, mensajes, _, perfil = modelo.leer(str(tabla))
        configuracion = modelo.PERFILES_TRAZADO[perfil]
        actual = modelo.trazar(copy.deepcopy(nodos), pools, carriles, mensajes, perfil)
        try:
            configuracion['compactar_filas_carril'] = False
            anterior = modelo.trazar(copy.deepcopy(nodos), pools, carriles, mensajes, perfil)
        finally:
            configuracion['compactar_filas_carril'] = True
        self.assertEqual(configuracion['columnas_tramo'], 16)
        self.assertLess(sum(v[3] for v in actual['geo_pool'].values()),
                        0.7 * sum(v[3] for v in anterior['geo_pool'].values()))
        for clave, caja in actual['caja'].items():
            self.assertEqual(caja[2:], anterior['caja'][clave][2:])
        for clave, caja in actual['geo_carril'].items():
            self.assertEqual(caja[2], anterior['geo_carril'][clave][2])
            self.assertLessEqual(caja[3], anterior['geo_carril'][clave][3])

    def test_suspension_compacta_sin_crecer_en_altura(self):
        tabla = next(AREA.glob('*/S4-3-2-5-diagrama-proceso-tabla.md'))
        _, nodos, pools, carriles, mensajes, _, perfil = modelo.leer(str(tabla))
        trazado = modelo.trazar(nodos, pools, carriles, mensajes, perfil)
        self.assertLess(trazado['caja']['E-E1'][0], 500)  # antes: 922
        self.assertLess(max(r[2] for r in trazado['geo_pool'].values()), 2200)  # antes: 2620
        self.assertEqual(trazado['geo_pool']['Gobierno Regional Huanuco'][3], 965)
        rutas = [m['pts'] for m in trazado['rutas_msg'].values()]
        for i, ruta in enumerate(rutas):
            self.assertEqual(modelo.conflictos_rutas(ruta, rutas[:i])[0], 0)
            self.assertTrue(all(u[0] == v[0] or u[1] == v[1] for u, v in zip(ruta, ruta[1:])))


if __name__ == '__main__':
    unittest.main()
