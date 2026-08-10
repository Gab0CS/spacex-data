<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useLaunchesStore } from '@/stores/launches'
import { useRocketsStore } from '@/stores/rockets'
import { useTableControls } from '@/composables/useTableControls'
import type { Launch, Rocket, SelectOption, TableColumn } from '@/types'
import PanelCard from '@/components/common/PanelCard.vue'
import AsyncSection from '@/components/common/AsyncSection.vue'
import DataTable from '@/components/common/DataTable.vue'
import PaginationControls from '@/components/common/PaginationControls.vue'
import SelectFilter from '@/components/common/SelectFilter.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import TabBar from '@/components/common/TabBar.vue'
import HorizontalBarChart from '@/components/charts/HorizontalBarChart.vue'
import LineChart from '@/components/charts/LineChart.vue'
import { categoricalColor, statusPalette } from '@/components/charts/chartTheme'

const launchesStore = useLaunchesStore()
const rocketsStore = useRocketsStore()

const tabs: SelectOption[] = [
  { label: 'Rockets', value: 'rockets' },
  { label: 'Launches', value: 'launches' },
]
const activeTab = ref<'rockets' | 'launches'>('rockets')

onMounted(() => {
  launchesStore.ensureLoaded()
  rocketsStore.ensureLoaded()
})

const isLoading = computed(() => launchesStore.isLoading || rocketsStore.isLoading)
const error = computed(() => launchesStore.error ?? rocketsStore.error)

function retry(): void {
  if (launchesStore.error) launchesStore.refresh()
  if (rocketsStore.error) rocketsStore.refresh()
}

// --- Charts (fleet-wide, unaffected by table filters) ---

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

const launchFrequencyData = computed(() => {
  const counts = new Map<number, number>()
  for (const launch of launchesStore.launches) {
    const year = new Date(launch.launch_date_utc).getFullYear()
    counts.set(year, (counts.get(year) ?? 0) + 1)
  }
  return [...counts.entries()].map(([x, y]) => ({ x, y })).sort((a, b) => a.x - b.x)
})

// --- Launches table: filters, sorting, pagination ---

const selectedRocket = ref('all')
const selectedYear = ref('all')
const selectedOutcome = ref('all')
const search = ref('')

const rocketOptions = computed<SelectOption[]>(() => {
  const names = new Set(launchesStore.launches.map((l) => l.rocket.rocket_name))
  return [{ label: 'All rockets', value: 'all' }, ...[...names].sort().map((name) => ({ label: name, value: name }))]
})

const yearOptions = computed<SelectOption[]>(() => {
  const years = new Set(launchesStore.launches.map((l) => String(new Date(l.launch_date_utc).getFullYear())))
  return [
    { label: 'All years', value: 'all' },
    ...[...years].sort((a, b) => Number(b) - Number(a)).map((year) => ({ label: year, value: year })),
  ]
})

const outcomeOptions: SelectOption[] = [
  { label: 'All outcomes', value: 'all' },
  { label: 'Successful', value: 'success' },
  { label: 'Failed', value: 'failed' },
  { label: 'Upcoming', value: 'upcoming' },
]

const filteredLaunches = computed(() => {
  const query = search.value.trim().toLowerCase()
  return launchesStore.launches.filter((launch) => {
    if (selectedRocket.value !== 'all' && launch.rocket.rocket_name !== selectedRocket.value) return false
    if (selectedYear.value !== 'all' && String(new Date(launch.launch_date_utc).getFullYear()) !== selectedYear.value) {
      return false
    }
    if (selectedOutcome.value === 'success' && launch.launch_success !== true) return false
    if (selectedOutcome.value === 'failed' && launch.launch_success !== false) return false
    if (selectedOutcome.value === 'upcoming' && !launch.upcoming) return false
    if (query && !launch.mission_name.toLowerCase().includes(query)) return false
    return true
  })
})

type LaunchColumnKey = 'flight_number' | 'mission_name' | 'rocket_name' | 'launch_date_utc' | 'launch_success'

const launchColumns: TableColumn<Launch, LaunchColumnKey>[] = [
  { key: 'flight_number', label: '#', sortable: true, accessor: (l) => l.flight_number },
  { key: 'mission_name', label: 'Mission', sortable: true, accessor: (l) => l.mission_name },
  { key: 'rocket_name', label: 'Rocket', sortable: true, accessor: (l) => l.rocket.rocket_name },
  {
    key: 'launch_date_utc',
    label: 'Date',
    sortable: true,
    accessor: (l) => l.launch_date_utc,
    format: (l) => new Date(l.launch_date_utc).toLocaleDateString(undefined, { dateStyle: 'medium' }),
  },
  { key: 'launch_success', label: 'Outcome', sortable: true, accessor: (l) => l.launch_success },
]

const {
  sortState: launchSortState,
  toggleSort: toggleLaunchSort,
  page: launchPage,
  pageSize: launchPageSize,
  goToPage: goToLaunchPage,
  totalItems: totalLaunches,
  totalPages: totalLaunchPages,
  pagedItems: pagedLaunches,
} = useTableControls<Launch, LaunchColumnKey>(filteredLaunches, {
  sortAccessors: {
    flight_number: (l) => l.flight_number,
    mission_name: (l) => l.mission_name,
    rocket_name: (l) => l.rocket.rocket_name,
    launch_date_utc: (l) => new Date(l.launch_date_utc).getTime(),
    launch_success: (l) => (l.upcoming ? 2 : l.launch_success === true ? 1 : l.launch_success === false ? 0 : -1),
  },
  defaultSortKey: 'launch_date_utc',
  defaultSortDirection: 'desc',
  pageSize: 10,
})

function outcomeLabel(launch: Launch): { text: string; color: string } {
  if (launch.upcoming) return { text: 'Upcoming', color: statusPalette.warning }
  if (launch.launch_success === true) return { text: 'Success', color: statusPalette.good }
  if (launch.launch_success === false) return { text: 'Failed', color: statusPalette.critical }
  return { text: 'Unknown', color: statusPalette.serious }
}

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
      <h1 class="text-2xl font-semibold text-slate-50">Rockets &amp; Launches</h1>
      <p class="mt-1 text-sm text-slate-500">Compare the fleet and explore every recorded launch.</p>
    </div>

    <AsyncSection :is-loading="isLoading" :error="error" loading-label="Loading rockets and launches…" @retry="retry">
      <div class="flex flex-col gap-6">
        <TabBar v-model="activeTab" :tabs="tabs" />

        <div v-if="activeTab === 'rockets'" class="flex flex-col gap-6">
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

        <div v-else class="flex flex-col gap-6">
          <PanelCard title="Launch frequency over time" subtitle="Launches recorded per year, across the fleet">
            <LineChart :data="launchFrequencyData" :color="categoricalColor(0)" />
          </PanelCard>

          <PanelCard title="Launches">
            <template #actions>
              <div class="flex flex-wrap items-end gap-3">
                <SearchInput v-model="search" label="Mission" placeholder="Search missions…" />
                <SelectFilter v-model="selectedRocket" label="Rocket" :options="rocketOptions" />
                <SelectFilter v-model="selectedYear" label="Year" :options="yearOptions" />
                <SelectFilter v-model="selectedOutcome" label="Outcome" :options="outcomeOptions" />
              </div>
            </template>

            <DataTable
              :columns="launchColumns"
              :rows="pagedLaunches"
              :sort-state="launchSortState"
              :row-key="(l) => l.id"
              empty-message="No launches match your filters."
              @sort="(key) => toggleLaunchSort(key as LaunchColumnKey)"
            >
              <template #cell-launch_success="{ row }">
                <span class="inline-flex items-center gap-1.5 text-xs font-medium" :style="{ color: outcomeLabel(row).color }">
                  <span class="h-1.5 w-1.5 rounded-full" :style="{ backgroundColor: outcomeLabel(row).color }" />
                  {{ outcomeLabel(row).text }}
                </span>
              </template>
            </DataTable>

            <PaginationControls
              class="mt-4"
              :page="launchPage"
              :total-pages="totalLaunchPages"
              :total-items="totalLaunches"
              :page-size="launchPageSize"
              @update:page="goToLaunchPage"
              @update:page-size="(size) => (launchPageSize = size)"
            />
          </PanelCard>
        </div>
      </div>
    </AsyncSection>
  </div>
</template>
