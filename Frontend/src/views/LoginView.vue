<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const router = useRouter();

const handleLogin = () => {
  // Lógica de autenticación simulada
  if (email.value === 'admin@embalses.cl' && password.value === 'password') {
    localStorage.setItem('userToken', 'fake-jwt-token-12345');
    router.push('/'); // Redirige al dashboard al iniciar sesión
  } else {
    alert('Correo o contraseña incorrectos.');
    password.value = '';
  }
};
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <div class="logo">
        <i class="pi pi-shield" style="font-size: 3rem; color: #3498db;"></i>
        <h2>Embalses IoT</h2>
      </div>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Correo Electrónico</label>
          <input type="email" id="email" v-model="email" required placeholder="admin@embalses.cl">
        </div>
        <div class="form-group">
          <label for="password">Contraseña</label>
          <input type="password" id="password" v-model="password" required placeholder="password">
        </div>
        <button type="submit" class="login-button">Iniciar Sesión</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
  /* Estilos del LoginView... (los mismos de la respuesta anterior) */
  .login-container{display:flex;justify-content:center;align-items:center;min-height:100vh;background-color:#f4f6f9;padding:1rem}.login-card{background-color:#fff;padding:2.5rem 3rem;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,.1);width:100%;max-width:400px;text-align:center}.logo{margin-bottom:2rem}.logo h2{margin:.5rem 0 0;color:#2c3e50}.login-form{display:flex;flex-direction:column}.form-group{margin-bottom:1.5rem;text-align:left}.form-group label{display:block;margin-bottom:.5rem;font-weight:600;color:#34495e}.form-group input{width:100%;padding:.75rem 1rem;border:1px solid #ced4da;border-radius:6px;font-size:1rem;box-sizing:border-box}.login-button{width:100%;padding:.85rem 1.5rem;background-color:#3498db;color:#fff;border:none;border-radius:6px;font-size:1.1rem;font-weight:700;cursor:pointer;transition:background-color .2s ease-in-out;margin-top:1rem}.login-button:hover{background-color:#2980b9}
</style>
