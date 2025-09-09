<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

const handleLogout = () => {
  localStorage.removeItem('userToken');
  router.push('/login');
};
</script>

<template>
  <div>
    <h1>¡Bienvenido al Dashboard!</h1>
    <p>Has iniciado sesión correctamente.</p>
    <button @click="handleLogout">Cerrar Sesión</button>
  </div>
</template>

<style scoped>
div{padding:2rem;text-align:center}button{margin-top:1rem;padding:.5rem 1rem;cursor:pointer;background-color:#e74c3c;color:#fff;border:none;border-radius:4px}
</style>
