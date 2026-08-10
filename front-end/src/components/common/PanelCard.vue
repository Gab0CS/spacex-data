<script setup lang="ts">
withDefaults(
  defineProps<{
    title?: string
    subtitle?: string
  }>(),
  { title: undefined, subtitle: undefined },
)
</script>

<template>
  <section
    class="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 shadow-lg shadow-black/20 backdrop-blur-sm"
  >
    <header v-if="title || $slots.actions" class="mb-4 flex items-start justify-between gap-4">
      <div v-if="title">
        <h3 class="text-sm font-semibold tracking-wide text-slate-200">{{ title }}</h3>
        <p v-if="subtitle" class="mt-0.5 text-xs text-slate-500">{{ subtitle }}</p>
      </div>
      <div v-if="$slots.actions" class="flex shrink-0 items-center gap-2">
        <slot name="actions" />
      </div>
    </header>
    <slot />
  </section>
</template>
