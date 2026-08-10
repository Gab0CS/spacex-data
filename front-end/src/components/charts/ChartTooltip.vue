<script setup lang="ts">
defineProps<{
  visible: boolean
  x: number
  y: number
  lines: string[]
}>()
</script>

<template>
  <div
    v-if="visible"
    class="pointer-events-none absolute z-10 -translate-x-1/2 -translate-y-full whitespace-nowrap rounded-md border border-slate-700 bg-slate-800/95 px-2.5 py-1.5 text-xs shadow-lg shadow-black/40"
    :style="{ left: `${x}px`, top: `${y - 12}px` }"
  >
    <div
      v-for="(line, index) in lines"
      :key="index"
      :class="index === 0 ? 'font-medium text-slate-100' : 'text-slate-400'"
    >
      {{ line }}
    </div>
  </div>
</template>
