<!-- App.vue -->
<template>
  <div class="layout">
    <aside class="sidebar">
      <Sidebar />
    </aside>
    <main class="main-content">
      <router-view :key="$route.fullPath" />
    </main>
  </div>
</template>



<script setup>
import Sidebar from './components/Sidebar.vue'
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 280px;
  flex-shrink: 0;
  background: #1e1e2f;
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.main-content {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  background-color: #f7f9fc;
}

</style>
