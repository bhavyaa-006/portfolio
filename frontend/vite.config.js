import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const devPort = Number(env.VITE_DEV_SERVER_PORT || 5173)
  const hmrHost = env.VITE_HMR_HOST || 'localhost'
  const hmrClientPort = Number(env.VITE_HMR_CLIENT_PORT || devPort)
  const apiProxyTarget = env.VITE_API_PROXY_TARGET || 'http://localhost:8000'

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
      hmr: {
        host: hmrHost,
        clientPort: hmrClientPort,
        protocol: env.VITE_HMR_PROTOCOL || 'ws',
      },
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
