// frontend/server.js
const express = require('express')
const path = require('path')

const app = express()

// Servir archivos estáticos desde dist/
app.use(express.static(path.join(__dirname, 'dist')))

// Fallback manual para Vue Router en modo history
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'))
})

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
  console.log(`Servidor en línea: http://localhost:${PORT}`)
})
