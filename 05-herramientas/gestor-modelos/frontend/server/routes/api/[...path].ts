import { getRequestURL, proxyRequest } from 'h3'

export default defineEventHandler((event) => {
  const incoming = getRequestURL(event)
  const upstream = useRuntimeConfig(event).apiTarget
  if (!incoming.pathname.startsWith('/api/') || !/^https?:\/\/[^/]+$/.test(upstream)) {
    throw createError({ statusCode: 400, statusMessage: 'Ruta de API inválida' })
  }
  const destination = `${upstream}${incoming.pathname}${incoming.search}`
  return proxyRequest(event, destination, { headers: { origin: new URL(upstream).origin } })
})
