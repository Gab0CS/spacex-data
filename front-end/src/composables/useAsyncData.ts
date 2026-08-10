import { ref, shallowRef } from 'vue'
import { ApiError } from '@/services/http'

export function useAsyncData<T>(fetcher: () => Promise<T>) {
  const data = shallowRef<T | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const hasLoaded = ref(false)

  async function execute(): Promise<void> {
    isLoading.value = true
    error.value = null
    try {
      data.value = await fetcher()
      hasLoaded.value = true
    } catch (err) {
      error.value = err instanceof ApiError ? err.message : 'Something went wrong. Please try again.'
    } finally {
      isLoading.value = false
    }
  }

  async function ensureLoaded(): Promise<void> {
    if (hasLoaded.value || isLoading.value) return
    await execute()
  }

  return { data, isLoading, error, hasLoaded, execute, ensureLoaded }
}
