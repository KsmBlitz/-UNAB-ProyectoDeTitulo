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
      component: () => import('../views/DashboardLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'DashboardHome',
          component: () => import('../views/DashboardHomeView.vue')
        },
        {
          path: 'users', // Se accederá en la URL /users
          name: 'UserManagement',
          component: () => import('../views/UserManagementView.vue'),
          meta: { requiresAuth: true } // También la protegemos
        }
      ]
    },
    { path: '/:catchAll(.*)', redirect: '/' }
  ]
})

// ... el guardia de navegación (beforeEach) se mantiene igual ...
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
