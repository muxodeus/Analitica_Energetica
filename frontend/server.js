// frontend/server.js
const express = require('express')
const path = require('path')
const history = require('connect-history-api-fallback')

const app = express()

// Soporte para Vue Router en modo history (una sola vez)
app.use(history({
  disableDotRule: true,
  verbose: true
}))

// Servir archivos estáticos desde dist/
app.use(express.static(path.join(__dirname, 'dist')))

// Fallback para rutas no encontradas (innecesario si usamos history middleware)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'))
})

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
  console.log(`Servidor en línea: http://localhost:${PORT}`)
})
