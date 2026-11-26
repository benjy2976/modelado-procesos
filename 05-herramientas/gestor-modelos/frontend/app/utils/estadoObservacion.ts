import type { components } from '~/types/api'

// Estado visible de una observación (rediseño 2026-11-26): traduce etapa, definición, aplicación y cierre a una
// sola clave con texto y color por significado. Los colores difieren también en luminosidad (daltonismo, impresión).
type Registro = components['schemas']['ObservacionVista']
type Trabajo = components['schemas']['TrabajoVista']
// Decisión en texto libre de una persona («Responder y decidir»): se envía como definición MANUAL al agente.
export type Definicion = { tipo: 'OPCION' | 'OPCIONES' | 'MANUAL' | 'VINCULADA'; opciones: string[]; texto: string; formato: 'html' | 'texto'; vinculada_a: string }

export type ClaveEstado =
  | 'por-decidir' | 'en-analisis' | 'en-aplicacion' | 'falta-evidencia'
  | 'resuelta-cambio' | 'resuelta-sin-cambio' | 'cerrada-sin-decision'

export type EstadoVisual = { clave: ClaveEstado; texto: string; color: string; fondo: string; barra: string }

const ESTILOS: Record<ClaveEstado, Omit<EstadoVisual, 'clave' | 'texto'>> = {
  'por-decidir': { color: '#9a4a00', fondo: '#fff1dc', barra: '#c2410c' },
  'en-analisis': { color: '#3b5b7a', fondo: '#eef3f7', barra: '#6b8aa6' },
  'en-aplicacion': { color: '#1d5aa6', fondo: '#eaf2fc', barra: '#1d5aa6' },
  'falta-evidencia': { color: '#6b3fa0', fondo: '#f1e9fb', barra: '#6b3fa0' },
  'resuelta-cambio': { color: '#1f6b3f', fondo: '#e8f5ec', barra: '#2e8b57' },
  'resuelta-sin-cambio': { color: '#3f6150', fondo: '#eef4f0', barra: '#7fa08c' },
  'cerrada-sin-decision': { color: '#a11d48', fondo: '#fde7ee', barra: '#be185d' }
}

export const ORDEN_ATENCION: ClaveEstado[] = [
  'cerrada-sin-decision', 'por-decidir', 'falta-evidencia', 'en-analisis', 'en-aplicacion', 'resuelta-cambio', 'resuelta-sin-cambio'
]

function efectosElegidos(item: Registro): Set<string> {
  const resolucion = item.resolucion
  const elegidas = new Set(resolucion?.definicion?.opciones || [])
  return new Set((resolucion?.propuesta?.opciones || []).filter(o => elegidas.has(o.id)).map(o => o.efecto))
}

export function estadoVisual(item: Registro, trabajos: Trabajo[] = []): EstadoVisual {
  const resolucion = item.resolucion
  const etapa = item.etapa || (item.estado === 'RESUELTA' ? 'RESUELTA' : 'REGISTRADA')
  const crear = (clave: ClaveEstado, texto: string): EstadoVisual => ({ clave, texto, ...ESTILOS[clave] })
  if (etapa === 'RESUELTA' || item.estado === 'RESUELTA') {
    const cierre = resolucion?.cierre
    if (cierre?.tipo === 'ACLARADA') return crear('resuelta-sin-cambio', 'Aclarada')
    if (cierre?.tipo === 'NO-PROCEDE') return crear('resuelta-sin-cambio', 'No procede')
    const aplicacion = resolucion?.aplicacion
    if (aplicacion?.resultado === 'ACLARADA') return crear('resuelta-sin-cambio', 'Aclarada')
    if (aplicacion?.resultado === 'NO-PROCEDE') return crear('resuelta-sin-cambio', 'No procede')
    if (aplicacion?.resultado === 'CAMBIO-MODELO') return crear('resuelta-cambio', 'Resuelta: cambió el diagrama')
    if (aplicacion?.resultado === 'CAMBIO-SUSTENTO') return crear('resuelta-cambio', 'Resuelta: cambió el sustento')
    if (aplicacion?.sesion) {
      return crear('resuelta-cambio', efectosElegidos(item).has('CAMBIO-MODELO') || !efectosElegidos(item).size
        ? 'Resuelta: cambió el diagrama' : 'Resuelta: cambió el sustento')
    }
    if (aplicacion || resolucion?.definicion) return crear('resuelta-sin-cambio', 'Resuelta sin cambios')
    return crear('cerrada-sin-decision', 'Cerrada sin decisión')
  }
  if (etapa === 'PENDIENTE-EVIDENCIA') return crear('falta-evidencia', 'Falta evidencia')
  if (etapa === 'DEFINIDA' || etapa === 'EN-CORRECCION') return crear('en-aplicacion', 'Decisión enviada al agente')
  if (resolucion?.decisiones_devueltas?.length && ['REGISTRADA', 'PROPUESTA'].includes(etapa)) return crear('por-decidir', 'Claudia pidió precisar')
  if (etapa === 'PROPUESTA') return crear('por-decidir', 'Por decidir')
  const analizando = trabajos.some(t => t.tipo === 'ANALISIS' && ['PENDIENTE', 'EN-CURSO'].includes(t.estado))
  return crear('en-analisis', analizando || etapa === 'EN-ANALISIS' ? 'En análisis' : 'Registrada')
}

function textoPlano(html: string): string {
  return html.replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim()
}

// Resumen de una línea para la lista: la etiqueta inicial («Duda.») y la pregunta si la hay, si no la primera frase.
export function resumenObservacion(item: Registro): { etiqueta: string; titulo: string } {
  const texto = item.texto || ''
  const etiqueta = /^\s*<p>\s*<strong>([^<]{2,40}?)\.?<\/strong>/i.exec(texto)?.[1]?.trim()
    || /^\s*\[([^\]]{2,40})\]/.exec(texto)?.[1]?.trim()
    || (item.tipo === 'COMENTARIO' ? 'Comentario' : 'Observación')
  const plano = textoPlano(texto).replace(/^\[[^\]]+\]\s*/, '').replace(new RegExp(`^${etiqueta.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\.?\\s*`), '')
  const pregunta = /Pregunta:\s*([^?]+\?)/.exec(plano)?.[1]
  const frase = pregunta || /^(.{20,170}?[.?])(\s|$)/.exec(plano)?.[1] || plano.slice(0, 160)
  return { etiqueta, titulo: frase.length > 170 ? `${frase.slice(0, 167)}…` : frase }
}

export type Paso = { nombre: string; detalle: string; estado: 'hecho' | 'actual' | 'futuro' }

const fecha = (valor?: string | null) => valor ? new Date(valor).toLocaleDateString('es-PE', { day: '2-digit', month: '2-digit' }) : ''

// Barra de etapas del detalle: quién hizo cada paso y a quién le toca el siguiente.
export function pasosObservacion(item: Registro, visual: EstadoVisual): Paso[] {
  const r = item.resolucion
  const cerrada = visual.clave === 'resuelta-cambio' || visual.clave === 'resuelta-sin-cambio'
  const sinCambio = Boolean(r?.cierre)
  const hecho = (nombre: string, detalle: string): Paso => ({ nombre, detalle, estado: 'hecho' })
  const pasos: Paso[] = [
    hecho('Registrada', `${item.autor} · ${fecha(item.fecha)}`),
    r?.analisis ? hecho('Analizada', `${r.analisis.autor} · ${fecha(r.analisis.fecha)}`) : { nombre: 'Analizar', detalle: 'Claudia', estado: 'futuro' },
    r?.propuesta ? hecho('Propuesta', `${r.propuesta.opciones.length} opciones`) : { nombre: 'Proponer', detalle: 'Claudia', estado: 'futuro' }
  ]
  if (sinCambio) {
    pasos.push(hecho('Decidida', `${r!.cierre!.autor} · ${fecha(r!.cierre!.fecha)}`))
    pasos.push(hecho('Sin cambio', 'No se toca el modelo'))
  } else {
    pasos.push(r?.definicion ? hecho('Decidida', `${r.definicion.autor} · ${fecha(r.definicion.fecha)}`) : { nombre: 'Decidir', detalle: 'Le toca al equipo', estado: 'futuro' })
    pasos.push(r?.aplicacion ? hecho('Aplicada', `${r.aplicacion.autor} · ${fecha(r.aplicacion.fecha)}`) : { nombre: 'Aplicar', detalle: 'Agente', estado: 'futuro' })
  }
  pasos.push(cerrada ? hecho('Resuelta', visual.texto) : { nombre: 'Resuelta', detalle: '—', estado: 'futuro' })
  const siguiente = pasos.find(p => p.estado === 'futuro')
  if (siguiente && visual.clave !== 'cerrada-sin-decision') siguiente.estado = 'actual'
  return pasos
}
