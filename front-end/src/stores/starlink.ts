import { defineStore } from 'pinia'
import { computed } from 'vue'
import { useAsyncData } from '@/composables/useAsyncData'
import { fetchStarlinkSatellites } from '@/services/starlinkService'

export const useStarlinkStore = defineStore('starlink', () => {
  const { data, isLoading, error, ensureLoaded, execute: refresh } = useAsyncData(fetchStarlinkSatellites)

  const satellites = computed(() => data.value ?? [])

  return { satellites, isLoading, error, ensureLoaded, refresh }
})
