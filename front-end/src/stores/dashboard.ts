import { defineStore } from 'pinia'
import { useAsyncData } from '@/composables/useAsyncData'
import { fetchDashboardStats } from '@/services/dashboardService'

export const useDashboardStore = defineStore('dashboard', () => {
  const { data: stats, isLoading, error, ensureLoaded, execute: refresh } = useAsyncData(fetchDashboardStats)

  return { stats, isLoading, error, ensureLoaded, refresh }
})
