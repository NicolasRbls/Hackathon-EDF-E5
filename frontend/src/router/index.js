import { createRouter, createWebHistory } from 'vue-router'
import { authService } from '../services/api'

import Index from '../views/Index.vue'
import LoginView from '../views/auth/LoginView.vue'
import BoDashboard from '../views/bo/dashboard/Pages/DashboardPage.vue'
import MagasinDashboard from '../views/magasin/dashboard/Pages/DashboardPage.vue'
import LaboDashboard from '../views/labo/dashboard/Pages/DashboardPage.vue'
import AdminDashboard from '../views/admin/dahboard/Pages/DashboardPage.vue'
import dashboardDashboard from '../views/dashboard/dashboard/Pages/DashboardPage.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/',
    name: 'Index',
    component: Index,
    meta: { requiresAuth: true }
  },
  {
    path: '/bo',
    name: 'bo-index',
    component: BoDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/magasin',
    name: 'magasin-index',
    component: MagasinDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/labo',
    name: 'labo-index',
    component: LaboDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'admin-index',
    component: AdminDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'dashboard-index',
    component: dashboardDashboard,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = authService.isAuthenticated();

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'Login' });
    } else {
      next();
    }
  } else {
    // Public page (Login)
    if (to.name === 'Login' && isAuthenticated) {
      // Already logged in? Go to dashboard or home
      // Optional: Redirect to specific role dashboard
      next({ name: 'Index' });
    } else {
      next();
    }
  }
});

export default router
