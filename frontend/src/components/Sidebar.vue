<!-- src/components/Sidebar.vue -->
<template>
  <!-- Se agrega una clase dinámica para ajustar el ancho según isCollapsed -->
  <div class="custom-sidebar" :class="{ collapsed: isCollapsed }">
    <div class="custom-sidebar-header">
      <!-- Se muestra el título completo o abreviado según el estado -->
      <h1 class="sidebar-title" v-show="!isCollapsed">ANALÍTICA ENERGÉTICA</h1>
      <h1 class="sidebar-title" v-show="isCollapsed">AE</h1>
    </div>
    <nav class="custom-sidebar-menu">
      <ul>
        <li v-for="(item, index) in menu" :key="index">
          <a :href="item.href ? item.href : '#'" class="menu-item">
            <i :class="item.icon"></i>
            <!-- Usamos v-show para que el texto se oculte en estado colapsado, pero siempre esté en el DOM -->
            <span class="menu-title" v-show="!isCollapsed">{{ item.title }}</span>
          </a>
          <!-- Submenú: se renderiza siempre, pero se oculta cuando isCollapsed es true -->
          <ul class="submenu" v-if="item.child" v-show="!isCollapsed">
            <li v-for="(child, cIndex) in item.child" :key="cIndex">
              <a :href="child.href" class="submenu-item">
                {{ child.title }}
              </a>
            </li>
          </ul>
        </li>
      </ul>
    </nav>
    <!-- Botón para colapsar/expandir en la parte inferior -->
    <div class="sidebar-footer">
      <button class="toggle-button" @click="$emit('toggleSidebar')">
        <i v-if="!isCollapsed" class="mdi mdi-chevron-left"></i>
        <i v-else class="mdi mdi-chevron-right"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  isCollapsed: {
    type: Boolean,
    default: false
  }
})
const emit = defineEmits(['toggleSidebar'])

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

<style scoped>
/* Contenedor del Sidebar con transición de ancho */
.custom-sidebar {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  font-family: Arial, sans-serif;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  width: 280px;
  transition: width 0.3s ease;
}

/* Cuando está colapsado, se reduce el ancho */
.custom-sidebar.collapsed {
  width: 80px;
}

/* Encabezado del Sidebar */
.custom-sidebar-header {
  padding: 20px 16px;
  border-bottom: 1px solid #e0e0e0;
  text-align: center;
  background-color: #f8f9fa;
}
.sidebar-title {
  font-size: 1.3rem;
  margin: 0;
  color: #333;
}

/* Menú Principal */
.custom-sidebar-menu {
  flex-grow: 1;
  padding: 0;
  margin: 0;
  overflow-y: auto;
}
.custom-sidebar-menu ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  text-decoration: none;
  color: #333;
  transition: background-color 0.2s ease;
}
.menu-item:hover {
  background-color: #f0f0f0;
}
.menu-item i {
  font-size: 28px;
  margin-right: 10px;
  color: #007bff;
}
.menu-title {
  font-size: 1rem;
  font-weight: 500;
}

/* Submenú */
.submenu {
  list-style: none;
  padding-left: 20px;
  margin: 5px 0;
}
.submenu-item {
  display: block;
  padding: 8px 16px;
  text-decoration: none;
  color: #666;
  font-size: 0.9rem;
  border-radius: 4px;
}
.submenu-item:hover {
  background-color: #f9f9f9;
}

/* Footer: botón de colapso */
.sidebar-footer {
  padding: 16px;
  text-align: center;
}
.toggle-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px; /* Botón más grande */
  height: 56px;
  border-radius: 50%;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
  font-size: 1.8rem;
  transition: background-color 0.3s ease, transform 0.3s ease;
}
.toggle-button:hover {
  background-color: #0056b3;
  transform: scale(1.1);
}
</style>
