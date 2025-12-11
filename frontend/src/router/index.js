import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/Index.vue'
import BoDashboard from '../views/bo/dashboard/Pages/DashboardPage.vue'
import MagasinDashboard from '../views/magasin/dashboard/Pages/DashboardPage.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
