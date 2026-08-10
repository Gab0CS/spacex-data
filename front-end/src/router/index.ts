import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior: () => ({ top: 0 }),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { title: 'Dashboard' },
    },
    {
      path: '/rockets',
      name: 'rockets',
      component: () => import('@/views/RocketsView.vue'),
      meta: { title: 'Rockets' },
    },
    {
      path: '/launches',
      name: 'launches',
      component: () => import('@/views/LaunchesView.vue'),
      meta: { title: 'Launches' },
    },
    {
      path: '/starlink',
      name: 'starlink',
      component: () => import('@/views/StarlinkView.vue'),
      meta: { title: 'Starlink' },
    },
  ],
})

export default router
