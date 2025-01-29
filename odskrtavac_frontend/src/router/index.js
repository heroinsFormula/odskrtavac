import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '/src/views/Dashboard.vue';
import AuthForm from '/src/views/AuthForm.vue';
import NotFound from '/src/views/NotFound.vue';

const routes = [
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
  },
  {
    path: '/login',
    name: 'login',
    component: AuthForm
  },
  {
    path: "/:catchAll(.*)",
    component: NotFound,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('auth');

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
