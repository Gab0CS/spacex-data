<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useLaunchesStore } from '@/stores/launches'
import { useRocketsStore } from '@/stores/rockets'
import { useTableControls } from '@/composables/useTableControls'
import type { Rocket, TableColumn } from '@/types'
import PanelCard from '@/components/common/PanelCard.vue'
import AsyncSection from '@/components/common/AsyncSection.vue'
import DataTable from '@/components/common/DataTable.vue'
import HorizontalBarChart from '@/components/charts/HorizontalBarChart.vue'
import { categoricalColor, statusPalette } from '@/components/charts/chartTheme'

const launchesStore = useLaunchesStore()
const rocketsStore = useRocketsStore()

onMounted(() => {
  rocketsStore.ensureLoaded()
  launchesStore.ensureLoaded()
})

const isLoading = computed(() => rocketsStore.isLoading || launchesStore.isLoading)
const error = computed(() => rocketsStore.error ?? launchesStore.error)

function retry(): void {
  if (rocketsStore.error) rocketsStore.refresh()
  if (launchesStore.error) launchesStore.refresh()
}

// --- Charts (derived from /api/launches, grouped by rocket) ---

const rocketComparisonData = computed(() => {
  const counts = new Map<string, number>()
  for (const launch of launchesStore.launches) {
    const name = launch.rocket.rocket_name
    counts.set(name, (counts.get(name) ?? 0) + 1)
  }
  return [...counts.entries()]
    .map(([label, value], index) => ({ label, value, color: categoricalColor(index) }))
    .sort((a, b) => b.value - a.value)
})

const successRateByRocketData = computed(() => {
  const totals = new Map<string, { success: number; decided: number }>()
  for (const launch of launchesStore.launches) {
    if (launch.launch_success === null || launch.launch_success === undefined) continue
    const name = launch.rocket.rocket_name
    const entry = totals.get(name) ?? { success: 0, decided: 0 }
    entry.decided += 1
    if (launch.launch_success) entry.success += 1
    totals.set(name, entry)
  }
  return [...totals.entries()]
    .map(([label, { success, decided }]) => ({
      label,
      value: decided ? Math.round((success / decided) * 1000) / 10 : 0,
      color: statusPalette.good,
    }))
    .sort((a, b) => b.value - a.value)
})

// --- Rockets table: sorting + pagination ---

type RocketColumnKey = 'rocket_name' | 'rocket_type' | 'active' | 'first_flight' | 'success_rate_pct' | 'cost_per_launch'

const rocketColumns: TableColumn<Rocket, RocketColumnKey>[] = [
  { key: 'rocket_name', label: 'Rocket', sortable: true, accessor: (r) => r.rocket_name },
  { key: 'rocket_type', label: 'Type', sortable: true, accessor: (r) => r.rocket_type },
  { key: 'active', label: 'Active', sortable: true, accessor: (r) => r.active },
  { key: 'first_flight', label: 'First flight', sortable: true, accessor: (r) => r.first_flight },
  {
    key: 'success_rate_pct',
    label: 'Success rate',
    sortable: true,
    align: 'right',
    accessor: (r) => r.success_rate_pct,
    format: (r) => (r.success_rate_pct != null ? `${r.success_rate_pct}%` : '—'),
  },
  {
    key: 'cost_per_launch',
    label: 'Cost / launch',
    sortable: true,
    align: 'right',
    accessor: (r) => r.cost_per_launch,
    format: (r) => (r.cost_per_launch != null ? `$${(r.cost_per_launch / 1_000_000).toFixed(0)}M` : '—'),
  },
]

const rockets = computed(() => rocketsStore.rockets)

const {
  sortState: rocketSortState,
  toggleSort: toggleRocketSort,
  pagedItems: pagedRockets,
} = useTableControls<Rocket, RocketColumnKey>(rockets, {
  sortAccessors: {
    rocket_name: (r) => r.rocket_name,
    rocket_type: (r) => r.rocket_type,
    active: (r) => r.active,
    first_flight: (r) => r.first_flight,
    success_rate_pct: (r) => r.success_rate_pct,
    cost_per_launch: (r) => r.cost_per_launch,
  },
  defaultSortKey: 'rocket_name',
  defaultSortDirection: 'asc',
  pageSize: 10,
})
</script>

<template>
  <div class="flex flex-col gap-6">
    <div>
      <h1 class="text-2xl font-semibold text-slate-50">Rockets</h1>
      <p class="mt-1 text-sm text-slate-500">Compare the SpaceX fleet by launch volume and reliability.</p>
    </div>

    <AsyncSection :is-loading="isLoading" :error="error" loading-label="Loading rockets…" @retry="retry">
      <div class="flex flex-col gap-6">
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <PanelCard title="Rocket comparison" subtitle="Total launches per rocket">
            <HorizontalBarChart :data="rocketComparisonData" />
          </PanelCard>
          <PanelCard title="Success rate by rocket" subtitle="Share of decided launches that succeeded">
            <HorizontalBarChart :data="successRateByRocketData" :domain-max="100" :value-format="(v) => `${v}%`" />
          </PanelCard>
        </div>

        <PanelCard title="Rockets">
          <DataTable
            :columns="rocketColumns"
            :rows="pagedRockets"
            :sort-state="rocketSortState"
            :row-key="(r) => r.rocket_id"
            empty-message="No rockets available."
            @sort="(key) => toggleRocketSort(key as RocketColumnKey)"
          >
            <template #cell-active="{ row }">
              <span :class="row.active ? 'text-emerald-400' : 'text-slate-500'">{{ row.active ? 'Active' : 'Retired' }}</span>
            </template>
          </DataTable>
        </PanelCard>
      </div>
    </AsyncSection>
  </div>
</template>
