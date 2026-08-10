<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useLaunchesStore } from '@/stores/launches'
import { useTableControls } from '@/composables/useTableControls'
import type { Launch, SelectOption, TableColumn } from '@/types'
import PanelCard from '@/components/common/PanelCard.vue'
import AsyncSection from '@/components/common/AsyncSection.vue'
import DataTable from '@/components/common/DataTable.vue'
import PaginationControls from '@/components/common/PaginationControls.vue'
import SelectFilter from '@/components/common/SelectFilter.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import LineChart from '@/components/charts/LineChart.vue'
import { categoricalColor, statusPalette } from '@/components/charts/chartTheme'

const launchesStore = useLaunchesStore()

onMounted(() => launchesStore.ensureLoaded())

// --- Chart: launch frequency over time (fleet-wide) ---

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
</script>

<template>
  <div class="flex flex-col gap-6">
    <div>
      <h1 class="text-2xl font-semibold text-slate-50">Launches</h1>
      <p class="mt-1 text-sm text-slate-500">Explore every recorded SpaceX launch.</p>
    </div>

    <AsyncSection
      :is-loading="launchesStore.isLoading"
      :error="launchesStore.error"
      loading-label="Loading launches…"
      @retry="launchesStore.refresh"
    >
      <div class="flex flex-col gap-6">
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
    </AsyncSection>
  </div>
</template>
