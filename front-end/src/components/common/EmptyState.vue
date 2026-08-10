<script setup lang="ts">
withDefaults(defineProps<{ message?: string }>(), { message: 'No results match your filters.' })
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-2 py-16 text-center text-slate-500">
    <p class="text-sm">{{ message }}</p>
  </div>
</template>
