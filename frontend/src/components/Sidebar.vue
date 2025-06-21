<!-- src/components/Sidebar.vue -->
<template>
  <SidebarMenu :menu="menu" />
</template>

<script setup>
import { SidebarMenu } from 'vue-sidebar-menu'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'

const menu = [
  { href: '/', title: 'Tiempo Real', icon: 'mdi mdi-clock-outline' },
  {
    title: 'Históricos',
    icon: 'mdi mdi-history',
    child: [
      { href: '/historicos/tendencias', title: 'Tendencias' },
      { href: '/historicos/estadisticas', title: 'Estadísticas' },
      { href: '/historicos/factor-carga', title: 'Factor de Carga' },
      { href: '/historicos/anomalias', title: 'Anomalías' },
      { href: '/historicos/patrones', title: 'Patrones' }
    ]
  },
  { href: '/reportes', title: 'Reportes', icon: 'mdi mdi-file-chart' },
  { href: '/consumo', title: 'Análisis de Consumo', icon: 'mdi mdi-flash-auto' },
  { href: '/configuracion', title: 'Configuración', icon: 'mdi mdi-cog-outline' }
]
</script>

<style>
/* Estas reglas se aplicarán globalmente (sin scope) para asegurar la sobreescritura */
.vue-sidebar-menu .vue-sidebar-menu-active a,
.vue-sidebar-menu li.active a {
  background-color: transparent !important; /* Se elimina el fondo azul */
  border-left: 4px solid #007bff !important;   /* Se agrega un borde izquierdo azul */
  color: #007bff !important;                     /* Se cambia el color del texto a azul */
}

.vue-sidebar-menu a:hover {
  background-color: rgba(0, 123, 255, 0.1) !important;
}
</style>
