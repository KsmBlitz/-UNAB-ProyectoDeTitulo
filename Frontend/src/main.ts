
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'primeicons/primeicons.css';

import { authStore } from './auth/store';
import { jwtDecode } from 'jwt-decode';

const token = localStorage.getItem('userToken');
if (token) {
  try {
    const decodedToken: { sub: string; role: string } = jwtDecode(token);
    authStore.user = {
      email: decodedToken.sub,
      role: decodedToken.role
    };
  } catch (error) {
    console.error("Token inválido encontrado en localStorage", error);
    localStorage.removeItem('userToken');
  }
}


const app = createApp(App)
app.use(router)
app.mount('#app')
