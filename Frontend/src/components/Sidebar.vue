<script setup lang="ts">
import { inject } from 'vue'
import type { Ref } from 'vue'
import { RouterLink } from 'vue-router' // <-- Importante

defineOptions({
  name: 'AppSidebar'
})

const isSidebarExpanded = inject<Ref<boolean>>('isSidebarExpanded');
const toggleSidebar = inject<() => void>('toggleSidebar');
</script>

<template>
  <aside class="sidebar" :class="{ collapsed: !isSidebarExpanded }">
    <header class="sidebar-header">
      <i class="pi pi-bars menu-toggle" @click="toggleSidebar"></i>
      <span class="logo-text">Embalses IoT</span>
    </header>
    <nav class="navigation">
      <ul>
        <RouterLink to="/" custom v-slot="{ navigate, isActive }">
          <li class="nav-item" :class="{ active: isActive }" @click="navigate">
            <i class="pi pi-home"></i>
            <span class="nav-text">Resumen</span>
          </li>
        </RouterLink>
        <li class="nav-item">
          <i class="pi pi-chart-bar"></i>
          <span class="nav-text">Reportes</span>
        </li>
        <li class="nav-item">
          <i class="pi pi-cog"></i>
          <span class="nav-text">Configuración</span>
        </li>
        <RouterLink to="/users" custom v-slot="{ navigate, isActive }">
          <li class="nav-item" :class="{ active: isActive }" @click="navigate">
            <i class="pi pi-users"></i>
            <span class="nav-text">Gestión de Usuarios</span>
          </li>
        </RouterLink>
      </ul>
    </nav>
  </aside>
</template>

<style scoped>
/* El estilo se mantiene igual que antes */
.sidebar{position:fixed;top:0;left:0;height:100vh;background-color:#2c3e50;color:#ecf0f1;display:flex;flex-direction:column;width:250px;transition:width .3s ease-in-out;overflow-x:hidden;z-index:999}.sidebar.collapsed{width:80px}.sidebar-header{display:flex;align-items:center;gap:1rem;font-size:1.5rem;font-weight:700;padding:0 25px;height:70px;flex-shrink:0}.menu-toggle{font-size:1.5rem;cursor:pointer}.navigation{padding:0 15px}.navigation ul{list-style:none;padding:0;margin:0}.nav-item{display:flex;align-items:center;padding:15px;margin-bottom:5px;border-radius:8px;cursor:pointer;transition:background-color .2s;height:56px}.sidebar.collapsed .nav-item{justify-content:center;padding:15px 0}.nav-item i{font-size:1.5rem;min-width:50px;text-align:center;transition:min-width .3s ease-in-out}.sidebar.collapsed .nav-item i{min-width:auto}.nav-item:hover{background-color:#34495e}.nav-item.active{background-color:#3498db;font-weight:700}.logo-text,.nav-text{opacity:1;transition:opacity .2s ease-in-out;white-space:nowrap}.sidebar.collapsed .logo-text,.sidebar.collapsed .nav-text{opacity:0;width:0}
</style>
