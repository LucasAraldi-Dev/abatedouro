import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'node:path'

// Remover console/debugger no build de produção
export default defineConfig(({ mode }) => {
  const isProd = mode === 'production'
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    },
    // Esbuild só no build de produção para manter logs no dev
    esbuild: isProd ? { drop: ['console', 'debugger'] } : undefined
  }
})