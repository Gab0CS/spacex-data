<script setup lang="ts">
type Accent = 'indigo' | 'emerald' | 'amber' | 'rose' | 'cyan'

const props = withDefaults(
  defineProps<{
    label: string
    value: string
    hint?: string
    accent?: Accent
  }>(),
  { hint: undefined, accent: 'indigo' },
)

const accentClasses: Record<Accent, string> = {
  indigo: 'text-indigo-400 bg-indigo-500/10 ring-indigo-500/20',
  emerald: 'text-emerald-400 bg-emerald-500/10 ring-emerald-500/20',
  amber: 'text-amber-400 bg-amber-500/10 ring-amber-500/20',
  rose: 'text-rose-400 bg-rose-500/10 ring-rose-500/20',
  cyan: 'text-cyan-400 bg-cyan-500/10 ring-cyan-500/20',
}

const dotClass = accentClasses[props.accent]
</script>

<template>
  <div class="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 shadow-lg shadow-black/20">
    <div class="flex items-center gap-2">
      <span :class="['h-2 w-2 rounded-full ring-4', dotClass]" />
      <p class="text-xs font-medium uppercase tracking-wider text-slate-500">{{ label }}</p>
    </div>
    <p class="mt-3 text-3xl font-semibold text-slate-50">{{ value }}</p>
    <p v-if="hint" class="mt-1 text-xs text-slate-500">{{ hint }}</p>
  </div>
</template>
