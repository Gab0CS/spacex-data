<script setup lang="ts">
const props = defineProps<{
  page: number
  totalPages: number
  totalItems: number
  pageSize: number
}>()

const emit = defineEmits<{
  'update:page': [value: number]
  'update:pageSize': [value: number]
}>()

const pageSizeOptions = [10, 25, 50]

function rangeLabel(): string {
  if (props.totalItems === 0) return '0 results'
  const start = (props.page - 1) * props.pageSize + 1
  const end = Math.min(props.page * props.pageSize, props.totalItems)
  return `${start}-${end} of ${props.totalItems}`
}
</script>

<template>
  <div class="flex flex-wrap items-center justify-between gap-3 border-t border-slate-800 pt-4 text-sm text-slate-400">
    <div class="flex items-center gap-2">
      <span>{{ rangeLabel() }}</span>
      <label class="ml-3 flex items-center gap-2">
        <span class="text-xs text-slate-500">Rows</span>
        <select
          :value="pageSize"
          class="rounded-md border border-slate-700 bg-slate-800 px-2 py-1 text-xs text-slate-200 focus:border-indigo-500 focus:outline-none"
          @change="emit('update:pageSize', Number(($event.target as HTMLSelectElement).value))"
        >
          <option v-for="size in pageSizeOptions" :key="size" :value="size">{{ size }}</option>
        </select>
      </label>
    </div>
    <div class="flex items-center gap-2">
      <button
        type="button"
        class="rounded-md border border-slate-700 bg-slate-800 px-3 py-1 text-xs font-medium text-slate-200 transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-40"
        :disabled="page <= 1"
        @click="emit('update:page', page - 1)"
      >
        Prev
      </button>
      <span class="text-xs text-slate-500">Page {{ page }} / {{ totalPages }}</span>
      <button
        type="button"
        class="rounded-md border border-slate-700 bg-slate-800 px-3 py-1 text-xs font-medium text-slate-200 transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-40"
        :disabled="page >= totalPages"
        @click="emit('update:page', page + 1)"
      >
        Next
      </button>
    </div>
  </div>
</template>
