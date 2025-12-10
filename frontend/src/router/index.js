import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/Index.vue'
import StaffDashboard from '../views/staff/dashboard/Pages/DashboardPage.vue'
import ManagerDashboard from '../views/manager/dashboard/Pages/DashboardPage.vue'

const routes = [
  {
    path: '/',
    name: 'Index',
    component: Index
  },
  {
    path: '/staff',
    name: 'StaffDashboard',
    component: StaffDashboard
  },
  {
    path: '/manager',
    name: 'ManagerDashboard',
    component: ManagerDashboard
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
