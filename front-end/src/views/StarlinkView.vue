<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useStarlinkStore } from '@/stores/starlink'
import { useTableControls } from '@/composables/useTableControls'
import type { SelectOption, StarlinkSatellite, TableColumn } from '@/types'
import PanelCard from '@/components/common/PanelCard.vue'
import AsyncSection from '@/components/common/AsyncSection.vue'
import DataTable from '@/components/common/DataTable.vue'
import PaginationControls from '@/components/common/PaginationControls.vue'
import SelectFilter from '@/components/common/SelectFilter.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import ScatterChart from '@/components/charts/ScatterChart.vue'
import DonutChart from '@/components/charts/DonutChart.vue'
import { categoricalColor } from '@/components/charts/chartTheme'

const starlinkStore = useStarlinkStore()

onMounted(() => starlinkStore.ensureLoaded())

const statusColors = { Active: categoricalColor(0), Inactive: categoricalColor(3) }

// --- Charts ---

const orbitScatterData = computed(() =>
  starlinkStore.satellites
    .filter((s) => s.height_km != null && s.spaceTrack?.INCLINATION != null)
    .map((s) => ({
      id: s.version ? `Starlink ${s.version}` : s.id,
      x: s.spaceTrack!.INCLINATION as number,
      y: s.height_km as number,
      category: s.is_active ? 'Active' : 'Inactive',
    })),
)

const statusDistributionData = computed(() => {
  const active = starlinkStore.satellites.filter((s) => s.is_active).length
  const inactive = starlinkStore.satellites.length - active
  return [
    { label: 'Active', value: active, color: statusColors.Active },
    { label: 'Inactive', value: inactive, color: statusColors.Inactive },
  ]
})

// --- Table: filters, sorting, pagination ---

const selectedStatus = ref('all')
const search = ref('')

const statusOptions: SelectOption[] = [
  { label: 'All statuses', value: 'all' },
  { label: 'Active', value: 'active' },
  { label: 'Inactive', value: 'inactive' },
]

const filteredSatellites = computed(() => {
  const query = search.value.trim().toLowerCase()
  return starlinkStore.satellites.filter((s) => {
    if (selectedStatus.value === 'active' && !s.is_active) return false
    if (selectedStatus.value === 'inactive' && s.is_active) return false
    if (query) {
      const haystack = `${s.id} ${s.version ?? ''}`.toLowerCase()
      if (!haystack.includes(query)) return false
    }
    return true
  })
})

type SatelliteColumnKey = 'version' | 'height_km' | 'velocity_kms' | 'inclination' | 'is_active'

const columns: TableColumn<StarlinkSatellite, SatelliteColumnKey>[] = [
  { key: 'version', label: 'Version', sortable: true, accessor: (s) => s.version, format: (s) => s.version ?? 'Unknown' },
  {
    key: 'height_km',
    label: 'Altitude (km)',
    sortable: true,
    align: 'right',
    accessor: (s) => s.height_km,
    format: (s) => (s.height_km != null ? s.height_km.toFixed(1) : '—'),
  },
  {
    key: 'velocity_kms',
    label: 'Velocity (km/s)',
    sortable: true,
    align: 'right',
    accessor: (s) => s.velocity_kms,
    format: (s) => (s.velocity_kms != null ? s.velocity_kms.toFixed(2) : '—'),
  },
  {
    key: 'inclination',
    label: 'Inclination (°)',
    sortable: true,
    align: 'right',
    accessor: (s) => s.spaceTrack?.INCLINATION,
    format: (s) => (s.spaceTrack?.INCLINATION != null ? s.spaceTrack.INCLINATION.toFixed(1) : '—'),
  },
  { key: 'is_active', label: 'Status', sortable: true, accessor: (s) => s.is_active },
]

const {
  sortState,
  toggleSort,
  page,
  pageSize,
  goToPage,
  totalItems,
  totalPages,
  pagedItems,
} = useTableControls<StarlinkSatellite, SatelliteColumnKey>(filteredSatellites, {
  sortAccessors: {
    version: (s) => s.version,
    height_km: (s) => s.height_km,
    velocity_kms: (s) => s.velocity_kms,
    inclination: (s) => s.spaceTrack?.INCLINATION,
    is_active: (s) => s.is_active,
  },
  defaultSortKey: 'height_km',
  defaultSortDirection: 'desc',
  pageSize: 10,
})
</script>

<template>
  <div class="flex flex-col gap-6">
    <div>
      <h1 class="text-2xl font-semibold text-slate-50">Starlink</h1>
      <p class="mt-1 text-sm text-slate-500">Orbital characteristics and operational status of the Starlink constellation.</p>
    </div>

    <AsyncSection
      :is-loading="starlinkStore.isLoading"
      :error="starlinkStore.error"
      loading-label="Loading Starlink satellites…"
      @retry="starlinkStore.refresh"
    >
      <div class="flex flex-col gap-6">
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <PanelCard
            title="Altitude vs. inclination"
            subtitle="Each point is one satellite — larger points are overlapping satellites in the same shell"
            class="lg:col-span-2"
          >
            <ScatterChart
              :data="orbitScatterData"
              :category-colors="statusColors"
              x-label="Inclination (degrees)"
              y-label="Altitude (km)"
              item-label="satellites"
            />
          </PanelCard>
          <PanelCard title="Operational status" subtitle="Active vs. inactive satellites">
            <DonutChart :data="statusDistributionData" center-label="Active" :center-value="String(statusDistributionData[0]?.value ?? 0)" />
          </PanelCard>
        </div>

        <PanelCard title="Satellites">
          <template #actions>
            <div class="flex flex-wrap items-end gap-3">
              <SearchInput v-model="search" label="Search" placeholder="ID or version…" />
              <SelectFilter v-model="selectedStatus" label="Status" :options="statusOptions" />
            </div>
          </template>

          <DataTable
            :columns="columns"
            :rows="pagedItems"
            :sort-state="sortState"
            :row-key="(s) => s.id"
            empty-message="No satellites match your filters."
            @sort="(key) => toggleSort(key as SatelliteColumnKey)"
          >
            <template #cell-is_active="{ row }">
              <span class="inline-flex items-center gap-1.5 text-xs font-medium" :style="{ color: row.is_active ? statusColors.Active : statusColors.Inactive }">
                <span class="h-1.5 w-1.5 rounded-full" :style="{ backgroundColor: row.is_active ? statusColors.Active : statusColors.Inactive }" />
                {{ row.is_active ? 'Active' : 'Inactive' }}
              </span>
            </template>
          </DataTable>

          <PaginationControls
            class="mt-4"
            :page="page"
            :total-pages="totalPages"
            :total-items="totalItems"
            :page-size="pageSize"
            @update:page="goToPage"
            @update:page-size="(size) => (pageSize = size)"
          />
        </PanelCard>
      </div>
    </AsyncSection>
  </div>
</template>
