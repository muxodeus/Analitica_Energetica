<template>
  <div class="layout">
    <!-- Se aplica la clase "collapsed" según el valor de isSidebarCollapsed -->
    <aside :class="{ sidebar: true, collapsed: isSidebarCollapsed }">
      <!-- Se pasa el estado y la función toggle al Sidebar -->
      <Sidebar :is-collapsed="isSidebarCollapsed" @toggleSidebar="toggleSidebar" />
    </aside>
    <main class="main-content">
      <router-view :key="$route.fullPath" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from './components/Sidebar.vue'

const isSidebarCollapsed = ref(false)

function toggleSidebar() {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* Ancho completo del sidebar cuando está expandido */
.sidebar {
  transition: width 0.3s;
  width: 280px;
  flex-shrink: 0;
  background: transparent; /* El fondo del Sidebar se establecerá dentro del componente Sidebar */
  box-shadow: none;
  z-index: 10;
}

/* Cuando se colapsa el sidebar, se reduce su ancho */
.sidebar.collapsed {
  width: 80px;
}

/* El área principal se ajusta automáticamente gracias a flex */
.main-content {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  background-color: #f7f9fc;
  transition: margin-left 0.3s;
}
</style>
