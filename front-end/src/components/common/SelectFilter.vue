<script setup lang="ts">
import type { SelectOption } from '@/types'

defineProps<{
  label: string
  modelValue: string
  options: SelectOption[]
}>()

const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<template>
  <label class="flex flex-col gap-1 text-xs text-slate-500">
    <span class="font-medium uppercase tracking-wide">{{ label }}</span>
    <select
      :value="modelValue"
      class="min-w-[9rem] rounded-md border border-slate-700 bg-slate-800 px-2.5 py-1.5 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none"
      @change="emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
    >
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
  </label>
</template>
