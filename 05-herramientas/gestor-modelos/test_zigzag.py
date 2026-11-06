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

    def test_seis_subprocesos_conservan_semantica_y_no_aumentan_d4(self):
        limites = {1: 0, 2: 0, 3: 18, 4: 1, 5: 0, 6: 6}
        tablas = sorted(AREA.glob('*/*-diagrama-proceso-tabla.md'))
        self.assertEqual(len(tablas), 6)
        for tabla in tablas:
            numero = int(tabla.name.split('-')[3])
            with self.subTest(proceso=numero):
                nombre, nodos, pools, carriles, mensajes, _, perfil = modelo.leer(str(tabla))
                def generar(p):
                    return modelo.generar(nombre, copy.deepcopy(nodos), pools, carriles, mensajes, tabla.name, p)
                xml = generar(perfil)
                self.assertEqual(xml, generar(perfil))
                self.assertEqual(semantica(xml), semantica(generar('normal')))
                with tempfile.TemporaryDirectory() as carpeta:
                    destino = Path(carpeta) / 'modelo.bpmn'
                    destino.write_text(xml, encoding='utf-8')
                    hallazgos = revisar(str(destino))
                    self.assertLessEqual(sum(map(len, hallazgos.values())), limites[numero], hallazgos)

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
