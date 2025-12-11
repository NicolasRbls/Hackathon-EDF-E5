import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/Index.vue'
import BoDashboard from '../views/bo/dashboard/Pages/DashboardPage.vue'
import MagasinDashboard from '../views/magasin/dashboard/Pages/DashboardPage.vue'
import LaboDashboard from '../views/labo/dashboard/Pages/DashboardPage.vue'
import AdminDashboard from '../views/admin/dahboard/Pages/DashboardPage.vue'
import dashboardDashboard from '../views/dashboard/dashboard/Pages/DashboardPage.vue'

const routes = [
  {
    path: '/',
    name: 'Index',
    component: Index
  },
  {
    path: '/bo',
    name: 'bo-index',
    component: BoDashboard
  },
  {
    path: '/magasin',
    name: 'magasin-index',
    component: MagasinDashboard
  },

  {
    path: '/labo',
    name: 'labo-index',
    component: LaboDashboard
  },


  {
    path: '/admin',
    name: 'admin-index',
    component: AdminDashboard
  }, 


  {
    path: '/dashboard',
    name: 'dashboard-index',
    component: dashboardDashboard
  }


  
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
