import js from '@eslint/js'
import vue from 'eslint-plugin-vue'
import ts from 'typescript-eslint'

export default ts.config(
  { ignores: ['.nuxt/**', '.output/**', 'node_modules/**', 'app/types/api.d.ts'] },
  js.configs.recommended,
  ...ts.configs.recommended,
  ...vue.configs['flat/essential'],
  {
    files: ['**/*.vue'],
    languageOptions: { parserOptions: { parser: ts.parser } },
    rules: { 'vue/multi-word-component-names': 'off' }
  },
  {
    languageOptions: {
      globals: {
        defineNuxtConfig: 'readonly',
        defineEventHandler: 'readonly',
        createError: 'readonly',
        useRuntimeConfig: 'readonly',
        fetch: 'readonly',
        URL: 'readonly',
        Error: 'readonly',
        HTMLElement: 'readonly',
        Element: 'readonly',
        document: 'readonly',
        DOMParser: 'readonly',
        XMLSerializer: 'readonly',
        WheelEvent: 'readonly',
        HTMLCanvasElement: 'readonly',
        KeyboardEvent: 'readonly',
        PointerEvent: 'readonly',
        ClipboardEvent: 'readonly',
        HTMLDivElement: 'readonly',
        localStorage: 'readonly',
        sessionStorage: 'readonly',
        TextDecoder: 'readonly',
        window: 'readonly',
        Blob: 'readonly',
        Image: 'readonly',
        setTimeout: 'readonly',
        setInterval: 'readonly',
        clearInterval: 'readonly'
      }
    }
  }
)
