import { createRouter, createWebHistory } from 'vue-router'
import { authService } from '../services/api'

import Index from '../views/Index.vue'
import LoginView from '../views/auth/LoginView.vue'
import BoDashboard from '../views/bo/dashboard/Pages/DashboardPage.vue'
import MagasinDashboard from '../views/magasin/dashboard/Pages/DashboardPage.vue'
import LaboDashboard from '../views/labo/dashboard/Pages/DashboardPage.vue'
import AdminDashboard from '../views/admin/dashboard/Pages/DashboardPage.vue'
import dashboardDashboard from '../views/dashboard/dashboard/Pages/DashboardPage.vue'
import ScanPage from '../views/magasin/scan/Pages/ScanPage.vue'
// BO Views
import BoSearchPage from '../views/bo/devices/Pages/SearchPage.vue'
import BoDevicePage from '../views/bo/devices/Pages/DevicePage.vue'
// Admin Views
import UsersPage from '../views/admin/users/Pages/UsersPage.vue'
import HistoryPage from '../views/admin/history/Pages/HistoryPage.vue'

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
  },
  {
    path: '/magasin/scan',
    name: 'scan-index',
    component: ScanPage,
    meta: { requiresAuth: true }
  },
  // BO Routes
  {
    path: '/bo/devices',
    name: 'bo-device-search',
    component: BoSearchPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/bo/devices/:serial',
    name: 'bo-device-details',
    component: BoDevicePage,
    meta: { requiresAuth: true }
  },
  // Admin Routes
  {
    path: '/admin/users',
    name: 'admin-users',
    component: UsersPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/history',
    name: 'admin-history',
    component: HistoryPage,
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
      next({ name: 'Index' });
    } else {
      next();
    }
  }
});

export default router
