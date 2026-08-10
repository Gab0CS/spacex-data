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
      path: '/rockets-launches',
      name: 'rockets-launches',
      component: () => import('@/views/RocketsLaunchesView.vue'),
      meta: { title: 'Rockets & Launches' },
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
