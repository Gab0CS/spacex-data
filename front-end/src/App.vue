<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'

const navLinks = [
  { to: '/', label: 'Dashboard' },
  { to: '/rockets', label: 'Rockets' },
  { to: '/launches', label: 'Launches' },
  { to: '/starlink', label: 'Starlink' },
]
</script>

<template>
  <div class="min-h-screen bg-slate-950">
    <header class="sticky top-0 z-20 border-b border-slate-800 bg-slate-950/80 backdrop-blur-sm">
      <div class="mx-auto flex max-w-7xl items-center justify-between gap-6 px-6 py-4">
        <div class="flex items-center gap-2">
          <span class="h-2.5 w-2.5 rounded-full bg-indigo-400" />
          <span class="text-sm font-semibold tracking-wide text-slate-100">SpaceX Dashboard API</span>
        </div>
        <nav class="flex items-center gap-1 rounded-full border border-slate-800 bg-slate-900/60 p-1">
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="rounded-full px-3.5 py-1.5 text-xs font-medium text-slate-400 transition hover:text-slate-100"
            active-class="!bg-indigo-500/15 !text-indigo-300"
            exact-active-class="!bg-indigo-500/15 !text-indigo-300"
          >
            {{ link.label }}
          </RouterLink>
        </nav>
      </div>
    </header>
    <main class="mx-auto max-w-7xl px-6 py-8">
      <RouterView />
    </main>
  </div>
</template>
