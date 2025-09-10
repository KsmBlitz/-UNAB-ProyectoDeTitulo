<script setup lang="ts">
import { ref } from 'vue';
import UsersTable from '@/components/UsersTable.vue';
import CreateUserModal from '@/components/CreateUserModal.vue'; // <-- Importar el modal

defineOptions({
  name: 'UserManagementView'
});

const isModalOpen = ref(false);
const usersTableKey = ref(0); // Clave para forzar la recarga de la tabla

function handleUserCreated() {
  isModalOpen.value = false; // Cierra el modal
  usersTableKey.value++; // Cambia la clave para que el componente UsersTable se recargue
}
</script>

<template>
  <div class="view-container">
    <header class="view-header">
      <h1>Gestión de Usuarios</h1>
      <button @click="isModalOpen = true" class="add-user-btn">
        <i class="pi pi-plus"></i>
        <span>Crear Nuevo Usuario</span>
      </button>
    </header>
    <p>Desde aquí podrás administrar los usuarios del sistema.</p>

    <UsersTable :key="usersTableKey" />

    <CreateUserModal
      v-if="isModalOpen"
      @close="isModalOpen = false"
      @user-created="handleUserCreated"
    />
  </div>
</template>

<style scoped>
/* Estilos sin cambios */
.view-container{padding:2rem}.view-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem}.view-header h1{margin:0}.add-user-btn{background-color:#28a745;color:#fff;border:none;border-radius:6px;padding:.75rem 1rem;font-size:1rem;font-weight:500;cursor:pointer;display:flex;align-items:center;gap:.5rem}.add-user-btn:hover{background-color:#218838}
</style>
