<script setup lang="ts">
import { ref, provide } from 'vue';
import Sidebar from '@/components/Sidebar.vue';

defineOptions({
  name: 'DashboardLayout'
});

// El estado sobre si el sidebar está expandido vive aquí
const isSidebarExpanded = ref(false);

function toggleSidebar() {
  isSidebarExpanded.value = !isSidebarExpanded.value;
}

// Proveemos el estado y la función a los componentes hijos (Sidebar)
provide('isSidebarExpanded', isSidebarExpanded);
provide('toggleSidebar', toggleSidebar);
</script>

<template>
  <div class="layout-wrapper">
    <Sidebar />
    <main class="main-content" :class="{ 'sidebar-expanded': isSidebarExpanded }">
      <h1>Contenido Principal</h1>
      <p>El sidebar ya está funcionando.</p>
    </main>
  </div>
</template>

<style scoped>
.layout-wrapper {
  display: flex;
}

.main-content {
  flex-grow: 1;
  height: 100vh;
  overflow-y: auto;
  margin-left: 80px; /* Ancho del sidebar colapsado */
  transition: margin-left 0.3s ease-in-out;
  padding: 2rem;
  box-sizing: border-box; /* Asegura que el padding no afecte el cálculo del ancho */
}

.main-content.sidebar-expanded {
  margin-left: 250px; /* Ancho del sidebar expandido */
}
</style>
