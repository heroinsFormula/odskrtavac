import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '/src/components/views/Dashboard.vue';
import AuthForm from '/src/components/views/AuthForm.vue';
import NotFound from '/src/components/views/NotFound.vue';

const routes = [
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
  },
  {
    path: '/login',
    name: 'Login',
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
  const isAuthenticated = localStorage.getItem('auth'); // Check for auth in localStorage or another auth source

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login'); // Redirect to login if not authenticated
  } else {
    next(); // Otherwise, proceed to the route
  }
});

export default router;
