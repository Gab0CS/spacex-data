import { computed, ref, watch, type ComputedRef, type Ref } from 'vue'
import type { SortDirection, SortState } from '@/types'

interface UseTableControlsOptions<T, TKey extends string> {
  sortAccessors: Record<TKey, (row: T) => unknown>
  defaultSortKey?: TKey | null
  defaultSortDirection?: SortDirection
  pageSize?: number
}

export function useTableControls<T, TKey extends string = string>(
  source: ComputedRef<T[]> | Ref<T[]>,
  options: UseTableControlsOptions<T, TKey>,
) {
  const sortState = ref<SortState<TKey>>({
    key: options.defaultSortKey ?? null,
    direction: options.defaultSortDirection ?? 'asc',
  })
  const page = ref(1)
  const pageSize = ref(options.pageSize ?? 10)

  function toggleSort(key: TKey): void {
    if (sortState.value.key !== key) {
      sortState.value = { key, direction: 'asc' }
      return
    }
    sortState.value = {
      key,
      direction: sortState.value.direction === 'asc' ? 'desc' : 'asc',
    }
  }

  const sortedItems = computed<T[]>(() => {
    const { key, direction } = sortState.value
    if (!key) return source.value
    const accessor = options.sortAccessors[key as TKey]
    const factor = direction === 'asc' ? 1 : -1
    return [...source.value].sort((a, b) => {
      const valueA = accessor(a)
      const valueB = accessor(b)
      if (valueA == null && valueB == null) return 0
      if (valueA == null) return 1
      if (valueB == null) return -1
      if (typeof valueA === 'string' && typeof valueB === 'string') {
        return valueA.localeCompare(valueB) * factor
      }
      if (valueA < valueB) return -1 * factor
      if (valueA > valueB) return 1 * factor
      return 0
    })
  })

  const totalItems = computed(() => sortedItems.value.length)
  const totalPages = computed(() => Math.max(1, Math.ceil(totalItems.value / pageSize.value)))

  const pagedItems = computed<T[]>(() => {
    const start = (page.value - 1) * pageSize.value
    return sortedItems.value.slice(start, start + pageSize.value)
  })

  watch([source, pageSize], () => {
    page.value = 1
  })

  watch(totalPages, (newTotal) => {
    if (page.value > newTotal) page.value = newTotal
  })

  function goToPage(target: number): void {
    page.value = Math.min(Math.max(1, target), totalPages.value)
  }

  return {
    sortState,
    toggleSort,
    page,
    pageSize,
    goToPage,
    totalItems,
    totalPages,
    sortedItems,
    pagedItems,
  }
}
