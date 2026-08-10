<script setup lang="ts">
import type { SelectOption } from '@/types'

defineProps<{
  modelValue: string
  tabs: SelectOption[]
}>()

const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<template>
  <div class="inline-flex w-fit items-center gap-1 rounded-full border border-slate-800 bg-slate-900/60 p-1">
    <button
      v-for="tab in tabs"
      :key="tab.value"
      type="button"
      class="rounded-full px-4 py-1.5 text-xs font-medium transition"
      :class="
        modelValue === tab.value
          ? 'bg-indigo-500/15 text-indigo-300'
          : 'text-slate-400 hover:text-slate-100'
      "
      @click="emit('update:modelValue', tab.value)"
    >
      {{ tab.label }}
    </button>
  </div>
</template>
