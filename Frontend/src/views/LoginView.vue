<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const errorMessage = ref(''); // Variable para mostrar errores al usuario
const router = useRouter();

const handleLogin = async () => {
  errorMessage.value = ''; // Limpia errores previos

  // Preparamos los datos para el formato que espera OAuth2
  const formData = new URLSearchParams();
  formData.append('username', email.value);
  formData.append('password', password.value);

  try {
    const response = await fetch('http://127.0.0.1:8000/api/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });

    if (!response.ok) {
      // Si el status no es 2xx, la autenticación falló
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Error de autenticación');
    }

    const data = await response.json();

    // Guardamos el token REAL que nos envió el backend
    localStorage.setItem('userToken', data.access_token);

    // Redirigimos al dashboard
    router.push('/');

  } catch (error: unknown) {
    if (error instanceof Error) {
      errorMessage.value = error.message || 'No se pudo conectar con el servidor.';
    } else {
      errorMessage.value = 'No se pudo conectar con el servidor.';
    }
    password.value = ''; // Limpiamos la contraseña en caso de error
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
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div class="form-group">
          <label for="email">Correo Electrónico</label>
          <input type="email" id="email" v-model="email" required placeholder="admin@embalses.cl">
        </div>
        <div class="form-group">
          <label for="password">Contraseña</label>
          <input type="password" id="password" v-model="password" required placeholder="********">
        </div>
        <button type="submit" class="login-button">Iniciar Sesión</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* Los estilos se mantienen igual, solo añadimos uno para el error */
.error-message {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  padding: 0.75rem 1.25rem;
  margin-bottom: 1rem;
  border-radius: 0.25rem;
  text-align: center;
}
.login-container{display:flex;justify-content:center;align-items:center;min-height:100vh;background-color:#f4f6f9;padding:1rem}.login-card{background-color:#fff;padding:2.5rem 3rem;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,.1);width:100%;max-width:400px;text-align:center}.logo{margin-bottom:2rem}.logo h2{margin:.5rem 0 0;color:#2c3e50}.login-form{display:flex;flex-direction:column}.form-group{margin-bottom:1.5rem;text-align:left}.form-group label{display:block;margin-bottom:.5rem;font-weight:600;color:#34495e}.form-group input{width:100%;padding:.75rem 1rem;border:1px solid #ced4da;border-radius:6px;font-size:1rem;box-sizing:border-box}.login-button{width:100%;padding:.85rem 1.5rem;background-color:#3498db;color:#fff;border:none;border-radius:6px;font-size:1.1rem;font-weight:700;cursor:pointer;transition:background-color .2s ease-in-out;margin-top:1rem}.login-button:hover{background-color:#2980b9}
</style>
