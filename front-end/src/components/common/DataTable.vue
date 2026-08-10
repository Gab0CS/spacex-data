<script setup lang="ts" generic="T">
import type { SortState, TableColumn } from '@/types'
import EmptyState from './EmptyState.vue'

defineProps<{
  columns: TableColumn<T>[]
  rows: T[]
  sortState: SortState
  rowKey: (row: T) => string | number
  emptyMessage?: string
}>()

const emit = defineEmits<{ sort: [key: string] }>()
</script>

<template>
  <div class="scrollbar-thin overflow-x-auto">
    <table class="w-full min-w-[640px] text-left text-sm">
      <thead>
        <tr class="border-b border-slate-800 text-xs uppercase tracking-wide text-slate-500">
          <th
            v-for="col in columns"
            :key="col.key"
            :class="['py-2 pr-4 font-medium', col.align === 'right' && 'text-right']"
          >
            <button
              v-if="col.sortable"
              type="button"
              class="inline-flex items-center gap-1 transition hover:text-slate-200"
              @click="emit('sort', col.key)"
            >
              {{ col.label }}
              <span v-if="sortState.key === col.key" class="text-indigo-400">
                {{ sortState.direction === 'asc' ? '▲' : '▼' }}
              </span>
            </button>
            <span v-else>{{ col.label }}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="row in rows"
          :key="rowKey(row)"
          class="border-b border-slate-800/60 last:border-0 hover:bg-slate-800/40"
        >
          <td
            v-for="col in columns"
            :key="col.key"
            :class="['py-2.5 pr-4 text-slate-300', col.align === 'right' && 'text-right']"
          >
            <slot :name="`cell-${col.key}`" :row="row">
              {{ col.format ? col.format(row) : String(col.accessor(row) ?? '—') }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
    <EmptyState v-if="rows.length === 0" :message="emptyMessage" />
  </div>
</template>
