import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/LoginView.vue') // Apuntamos a la vista de Login que crearemos
    },
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('../views/DashboardLayout.vue'), // Apuntamos al layout del dashboard
      meta: { requiresAuth: true } // Marcamos esta ruta como protegida
    },
    // Redireccionar cualquier ruta no encontrada
    {
      path: '/:catchAll(.*)',
      redirect: '/'
    }
  ]
})

// "Guardia de Navegación": Se ejecuta antes de cada cambio de ruta
router.beforeEach((to, from, next) => {
  // Simulamos la autenticación revisando si existe un "token"
  const isAuthenticated = localStorage.getItem('userToken');

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login'); // Si la ruta requiere auth y no hay token, va al login.
  }
  else if (to.name === 'Login' && isAuthenticated) {
    next('/'); // Si ya está autenticado e intenta ir al login, va al dashboard.
  }
  else {
    next(); // En cualquier otro caso, permite el acceso.
  }
});

export default router
