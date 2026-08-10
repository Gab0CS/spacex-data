<script setup lang="ts">
withDefaults(
  defineProps<{
    modelValue: string
    placeholder?: string
    label?: string
  }>(),
  { placeholder: 'Search…', label: 'Search' },
)

const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<template>
  <label class="flex flex-col gap-1 text-xs text-slate-500">
    <span class="font-medium uppercase tracking-wide">{{ label }}</span>
    <input
      type="text"
      :value="modelValue"
      :placeholder="placeholder"
      class="min-w-[12rem] rounded-md border border-slate-700 bg-slate-800 px-2.5 py-1.5 text-sm text-slate-200 placeholder:text-slate-600 focus:border-indigo-500 focus:outline-none"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
  </label>
</template>
