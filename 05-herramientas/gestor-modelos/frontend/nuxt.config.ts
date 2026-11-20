export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  ssr: false,
  css: ['~/assets/main.css'],
  runtimeConfig: {
    apiTarget: 'http://127.0.0.1:8766'
  },
  app: {
    head: {
      htmlAttrs: { lang: 'es' },
      title: 'Mesa de modelamiento | Gobierno Regional de Huánuco',
      meta: [{ name: 'description', content: 'Revisión de procesos y evidencia del Gobierno Regional de Huánuco' }]
    }
  }
})
