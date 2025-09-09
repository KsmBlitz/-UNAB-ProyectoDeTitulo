// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/',
      component: () => import('../views/DashboardLayout.vue'), // El componente padre
      meta: { requiresAuth: true },
      children: [ // <-- Rutas que se renderizan dentro de DashboardLayout
        {
          path: '', // La ruta raíz ('/')
          name: 'DashboardHome',
          component: () => import('../views/DashboardHomeView.vue')
        },
        // Aquí añadiremos /reportes, /configuracion, etc. en el futuro
      ]
    },
    { path: '/:catchAll(.*)', redirect: '/' }
  ]
})

// ...el guardia de navegación (beforeEach) se mantiene igual...
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('userToken');
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else if (to.name === 'Login' && isAuthenticated) {
    next('/');
  } else {
    next();
  }
});

export default router
