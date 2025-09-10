<script setup lang="ts">
import { ref, provide } from 'vue';
import { RouterView } from 'vue-router'; // <-- Importamos RouterView
import Sidebar from '@/components/Sidebar.vue';
import TheHeader from '@/components/TheHeader.vue';

defineOptions({
  name: 'DashboardLayout'
});

const isSidebarExpanded = ref(false);
function toggleSidebar() {
  isSidebarExpanded.value = !isSidebarExpanded.value;
}
provide('isSidebarExpanded', isSidebarExpanded);
provide('toggleSidebar', toggleSidebar);
</script>

<template>
  <div class="layout-wrapper">
    <Sidebar />
    <main class="main-content" :class="{ 'sidebar-expanded': isSidebarExpanded }">
      <TheHeader />
      <div class="content-wrapper">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<style scoped>
.layout-wrapper{display:flex;background-color:#f4f6f9}.main-content{flex-grow:1;display:flex;flex-direction:column;height:100vh;overflow:hidden;margin-left:80px;transition:margin-left .3s ease-in-out}.main-content.sidebar-expanded{margin-left:250px}.content-wrapper{flex-grow:1;overflow-y:auto;padding:2rem}
</style>
