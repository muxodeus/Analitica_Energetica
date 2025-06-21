// frontend/server.js
const express = require('express')
const path = require('path')
const app = express()
const history = require('connect-history-api-fallback')

// Soporte para Vue Router en modo history
app.use(history())

// Servir archivos estáticos desde dist/
app.use(express.static(path.join(__dirname, 'dist')))

// Enviar index.html para cualquier ruta no encontrada (SPA fallback)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'))
})

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
  console.log(`Servidor en línea: http://localhost:${PORT}`)
})
