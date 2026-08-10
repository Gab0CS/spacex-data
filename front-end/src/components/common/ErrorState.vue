<script setup lang="ts">
withDefaults(defineProps<{ message?: string }>(), {
  message: 'Something went wrong while loading data.',
})

const emit = defineEmits<{ retry: [] }>()
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-3 py-16 text-center">
    <div class="flex h-10 w-10 items-center justify-center rounded-full bg-rose-500/10 text-rose-400 ring-4 ring-rose-500/20">
      !
    </div>
    <p class="max-w-sm text-sm text-slate-400">{{ message }}</p>
    <button
      type="button"
      class="rounded-lg border border-slate-700 bg-slate-800 px-4 py-1.5 text-xs font-medium text-slate-200 transition hover:bg-slate-700"
      @click="emit('retry')"
    >
      Try again
    </button>
  </div>
</template>
