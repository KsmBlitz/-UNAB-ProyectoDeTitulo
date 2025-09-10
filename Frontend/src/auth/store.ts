import { reactive } from 'vue';

interface User {
  email: string;
  role: string;
}

// Exportamos un objeto reactivo que contendrá los datos del usuario
export const authStore = reactive({
  user: null as User | null,
});
