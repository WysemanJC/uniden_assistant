import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { readFileSync } from 'fs'
import { resolve } from 'path'

// Get backend URL from environment or use default
const backendUrl = process.env.BACKEND_URL || 'http://localhost:8001'

// Get FQDN from environment and build allowedHosts list
const fqdn = process.env.FQDN || 'localhost'
const allowedHosts = [fqdn, 'localhost', '127.0.0.1']

export default defineConfig({
  plugins: [
    vue(),
    // Custom plugin to serve markdown files from docs directory
    {
      name: 'serve-docs',
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          if (req.url.startsWith('/docs/')) {
            try {
              const docPath = resolve(__dirname, '..', req.url.slice(1))
              const content = readFileSync(docPath, 'utf-8')
              res.setHeader('Content-Type', 'text/markdown; charset=utf-8')
              res.end(content)
            } catch (err) {
              res.statusCode = 404
              res.end('Documentation not found')
            }
          } else {
            next()
          }
        })
      }
    }
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 9001,
    host: '0.0.0.0',
    allowedHosts: allowedHosts,
    proxy: {
      '/api': {
        target: backendUrl,
        changeOrigin: true
      }
    }
  }
})
