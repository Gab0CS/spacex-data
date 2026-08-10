import { defineStore } from 'pinia'
import { computed } from 'vue'
import { useAsyncData } from '@/composables/useAsyncData'
import { fetchLaunches } from '@/services/launchService'

export const useLaunchesStore = defineStore('launches', () => {
  const { data, isLoading, error, ensureLoaded, execute: refresh } = useAsyncData(fetchLaunches)

  const launches = computed(() => data.value ?? [])

  return { launches, isLoading, error, ensureLoaded, refresh }
})
