import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

function parsePositiveInt(value) {
  if (value === undefined || value === null) {
    return undefined
  }

  const normalized = String(value).trim()
  if (!normalized || normalized.toLowerCase() === 'undefined' || normalized.toLowerCase() === 'null') {
    return undefined
  }

  const parsed = Number(normalized)
  if (!Number.isFinite(parsed) || parsed <= 0) {
    return undefined
  }

  return parsed
}

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const devPort = parsePositiveInt(env.VITE_DEV_SERVER_PORT) || 5173
  const hmrHost = env.VITE_HMR_HOST?.trim()
  const hmrClientPort = parsePositiveInt(env.VITE_HMR_CLIENT_PORT) || parsePositiveInt(env.VITE_HMR_PORT)
  const apiProxyTarget = env.VITE_API_PROXY_TARGET || 'http://localhost:8000'
  const usePolling = ['1', 'true', 'yes'].includes(String(env.CHOKIDAR_USEPOLLING || '').toLowerCase())
  const hmrProtocol = env.VITE_HMR_PROTOCOL === 'wss' ? 'wss' : 'ws'

  const hmrConfig = hmrHost || hmrClientPort
    ? {
        protocol: hmrProtocol,
        host: hmrHost || 'localhost',
        clientPort: hmrClientPort,
        port: hmrClientPort,
      }
    : true

  return {
    plugins: [react()],
    resolve: {
      dedupe: ['react', 'react-dom'],
    },
    server: {
      host: '0.0.0.0',
      port: devPort,
      strictPort: true,
      cors: true,
      watch: usePolling ? { usePolling: true, interval: 100 } : undefined,
      hmr: hmrConfig,
      proxy: {
        '/api': {
          target: apiProxyTarget,
          changeOrigin: true,
          secure: false,
        },
        '/uploads': {
          target: apiProxyTarget,
          changeOrigin: true,
          secure: false,
        },
      },
    },
  }
})
