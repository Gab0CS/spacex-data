<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import PanelCard from '@/components/common/PanelCard.vue'
import StatCard from '@/components/common/StatCard.vue'
import AsyncSection from '@/components/common/AsyncSection.vue'
import BarChart from '@/components/charts/BarChart.vue'
import DonutChart from '@/components/charts/DonutChart.vue'
import { statusPalette, categoricalColor } from '@/components/charts/chartTheme'

const dashboardStore = useDashboardStore()

onMounted(() => dashboardStore.ensureLoaded())

const launchesPerYear = computed(() => {
  const stats = dashboardStore.stats
  if (!stats) return []
  return Object.entries(stats.launches_per_year)
    .map(([year, count]) => ({ label: year, value: count }))
    .sort((a, b) => Number(a.label) - Number(b.label))
})

const successRateData = computed(() => {
  const stats = dashboardStore.stats
  if (!stats) return []
  return [
    { label: 'Successful', value: stats.successful_launches, color: statusPalette.good },
    { label: 'Failed', value: stats.failed_launches, color: statusPalette.critical },
  ]
})

const satelliteStatusData = computed(() => {
  const stats = dashboardStore.stats
  if (!stats) return []
  return [
    { label: 'Active', value: stats.active_starlink_satellites, color: categoricalColor(0) },
    { label: 'Inactive', value: stats.inactive_starlink_satellites, color: categoricalColor(3) },
  ]
})
</script>

<template>
  <div class="flex flex-col gap-6">
    <div>
      <h1 class="text-2xl font-semibold text-slate-50">Dashboard</h1>
      <p class="mt-1 text-sm text-slate-500">Fleet-wide overview of SpaceX rockets, launches, and Starlink satellites.</p>
    </div>

    <AsyncSection
      :is-loading="dashboardStore.isLoading"
      :error="dashboardStore.error"
      loading-label="Loading dashboard…"
      @retry="dashboardStore.refresh"
    >
      <div v-if="dashboardStore.stats" class="flex flex-col gap-6">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard label="Total rockets" :value="dashboardStore.stats.total_rockets.toLocaleString()" accent="indigo" />
          <StatCard label="Total launches" :value="dashboardStore.stats.total_launches.toLocaleString()" accent="cyan" />
          <StatCard
            label="Launch success rate"
            :value="`${dashboardStore.stats.launch_success_rate.toFixed(1)}%`"
            accent="emerald"
          />
          <StatCard
            label="Active satellites"
            :value="dashboardStore.stats.active_starlink_satellites.toLocaleString()"
            accent="amber"
          />
        </div>

        <PanelCard title="Launches per year" subtitle="Number of launches recorded each year">
          <BarChart :data="launchesPerYear" :color="categoricalColor(0)" />
        </PanelCard>

        <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <PanelCard title="Launch success rate" subtitle="Successful vs. failed launches">
            <DonutChart
              :data="successRateData"
              center-label="Success rate"
              :center-value="`${dashboardStore.stats.launch_success_rate.toFixed(1)}%`"
            />
          </PanelCard>
          <PanelCard title="Starlink fleet status" subtitle="Active vs. inactive satellites">
            <DonutChart
              :data="satelliteStatusData"
              center-label="Active"
              :center-value="dashboardStore.stats.active_starlink_satellites.toLocaleString()"
            />
          </PanelCard>
        </div>
      </div>
    </AsyncSection>
  </div>
</template>
