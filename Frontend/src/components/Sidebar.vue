<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { authStore } from '@/auth/store';

defineOptions({
  name: 'AppSidebar'
});

defineProps<{
  isCollapsed: boolean
}>();
const emit = defineEmits(['toggle-sidebar']);
</script>

<template>
  <aside class="sidebar" :class="{ collapsed: isCollapsed }">
    <div class="sidebar-content">
      <div class="sidebar-header">
        <i class="pi pi-shield logo-icon"></i>
        <h2 v-if="!isCollapsed" class="app-title">Embalse IoT</h2>
      </div>
      <nav class="navigation">
        <RouterLink to="/" class="nav-item">
          <i class="pi pi-th-large"></i>
          <span v-if="!isCollapsed">Dashboard</span>
        </RouterLink>
        <RouterLink to="/users" class="nav-item" v-if="authStore.user?.role === 'admin'">
          <i class="pi pi-users"></i>
          <span v-if="!isCollapsed">Usuarios</span>
        </RouterLink>
      </nav>
    </div>

    <div class="sidebar-footer">
      <button class="toggle-btn" @click="emit('toggle-sidebar')" title="Colapsar/Expandir Menú">
        <i class="pi" :class="isCollapsed ? 'pi-align-right' : 'pi-align-left'"></i>
      </button>
    </div>
  </aside>
</template>

<style scoped>
:root {
  --sidebar-width: 260px;
  --sidebar-collapsed-width: 88px;
}

.sidebar {
  width: var(--sidebar-width);
  background-color: #2c3e50;
  color: #ecf0f1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  transition: width 0.3s ease-in-out;
  flex-shrink: 0;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

.sidebar-content {
  /* Contenedor para el header y la navegación */
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0 1.75rem;
  height: var(--header-height, 80px);
  flex-shrink: 0;
  overflow: hidden;
  border-bottom: 1px solid #4a5568;
}

.sidebar.collapsed .sidebar-header {
  justify-content: center;
  padding: 0;
}

.logo-icon {
  font-size: 1.8rem;
  flex-shrink: 0;
}

.app-title {
  font-size: 1.2rem;
  font-weight: 600;
  white-space: nowrap;
}

.navigation {
  padding: 1rem;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.9rem 1rem;
  color: #a0aec0;
  text-decoration: none;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.nav-item i {
  font-size: 1.5rem;
  margin-right: 1.5rem;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}

.sidebar.collapsed .nav-item {
  justify-content: center;
}

.sidebar.collapsed .nav-item i {
  margin-right: 0;
}

.sidebar.collapsed .nav-item span {
  display: none;
}

.nav-item:hover {
  background-color: #34495e;
  color: #fff;
}

/* --- CORRECCIÓN PARA EL ENLACE ACTIVO --- */
/* Vue Router añade esta clase automáticamente al enlace EXACTO */
.nav-item.router-link-exact-active {
  background-color: #3498db;
  color: #fff;
  font-weight: 500;
}

/* --- NUEVOS ESTILOS PARA EL BOTÓN EN EL FOOTER --- */
.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid #4a5568;
}

.toggle-btn {
  width: 100%;
  background-color: #34495e;
  border: none;
  color: #a0aec0;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;
}

.toggle-btn:hover {
  background-color: #4a5568;
  color: #fff;
}
</style>
