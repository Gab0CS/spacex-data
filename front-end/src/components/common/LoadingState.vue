<script setup lang="ts">
withDefaults(defineProps<{ label?: string }>(), { label: 'Loading data…' })
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-3 py-16 text-slate-500">
    <span class="h-8 w-8 animate-spin rounded-full border-2 border-slate-700 border-t-indigo-400" />
    <p class="text-sm">{{ label }}</p>
  </div>
</template>
