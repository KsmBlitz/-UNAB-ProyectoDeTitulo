<script setup lang="ts">
import UsersTable from '@/components/UsersTable.vue';

defineOptions({
  name: 'UserManagementView'
});
</script>

<template>
  <div class="view-container">
    <header class="view-header">
      <h1>Gestión de Usuarios</h1>
      <button class="add-user-btn">
        <i class="pi pi-plus"></i>
        <span>Crear Nuevo Usuario</span>
      </button>
    </header>
    <p>Desde aquí podrás administrar los usuarios del sistema.</p>
    <UsersTable />
  </div>
</template>

<style scoped>
.view-container {
  padding: 2rem;
}
.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.view-header h1 {
  margin: 0;
}
.add-user-btn {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.add-user-btn:hover {
  background-color: #218838;
}
</style>
