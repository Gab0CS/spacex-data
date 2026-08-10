import { defineStore } from 'pinia'
import { computed } from 'vue'
import { useAsyncData } from '@/composables/useAsyncData'
import { fetchRockets } from '@/services/rocketService'

export const useRocketsStore = defineStore('rockets', () => {
  const { data, isLoading, error, ensureLoaded, execute: refresh } = useAsyncData(fetchRockets)

  const rockets = computed(() => data.value ?? [])

  return { rockets, isLoading, error, ensureLoaded, refresh }
})
