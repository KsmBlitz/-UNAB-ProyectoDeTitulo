// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { authStore } from '@/auth/store'; // <-- 1. Importar el store

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
      component: () => import('../views/DashboardLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'DashboardHome',
          component: () => import('../views/DashboardHomeView.vue')
        },
        {
          path: 'users',
          name: 'UserManagement',
          component: () => import('../views/UserManagementView.vue'),
          // 2. Añadimos el rol requerido a la metadata de la ruta
          meta: { requiresAuth: true, requiresRole: 'admin' }
        }
      ]
    },
    { path: '/:catchAll(.*)', redirect: '/' }
  ]
})

// 3. Guardia de navegación actualizado con chequeo de rol
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('userToken');

  if (to.meta.requiresAuth && !isAuthenticated) {
    // Si requiere auth y no está logueado, va al login
    next('/login');
  } else if (to.name === 'Login' && isAuthenticated) {
    // Si está logueado e intenta ir al login, va al dashboard
    next('/');
  } else if (to.meta.requiresRole) {
    // Si la ruta requiere un rol...
    const userRole = authStore.user?.role;
    if (userRole === to.meta.requiresRole) {
      // ...y el usuario tiene ese rol, le permitimos pasar
      next();
    } else {
      // ...si no tiene el rol, le negamos el acceso y lo enviamos al inicio
      alert('No tienes permisos para acceder a esta página.');
      next('/');
    }
  } else {
    // Para todas las demás rutas, permitimos el paso
    next();
  }
});

export default router
