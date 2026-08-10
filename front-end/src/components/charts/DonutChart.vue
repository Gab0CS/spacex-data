<script setup lang="ts">
import { ref, watch, watchEffect } from 'vue'
import * as d3 from 'd3'
import { useChartDimensions } from '@/composables/useChartDimensions'
import { useChartTooltip } from '@/composables/useChartTooltip'
import { ink } from './chartTheme'
import ChartTooltip from './ChartTooltip.vue'

interface DonutDatum {
  label: string
  value: number
  color: string
}

const props = withDefaults(
  defineProps<{
    data: DonutDatum[]
    valueFormat?: (value: number) => string
    centerLabel?: string
    centerValue?: string
  }>(),
  {
    valueFormat: (value: number) => value.toLocaleString(),
    centerLabel: undefined,
    centerValue: undefined,
  },
)

const containerRef = ref<HTMLElement | null>(null)
const svgRef = ref<SVGSVGElement | null>(null)
const { dimensions } = useChartDimensions(containerRef, 0.6)
const { tooltip, showTooltip, hideTooltip } = useChartTooltip()

function render(): void {
  if (!svgRef.value || dimensions.value.width === 0) return
  const { width, height } = dimensions.value
  const radius = Math.min(width, height) / 2 - 8

  const svg = d3.select(svgRef.value)
  svg.selectAll('*').remove()
  svg.attr('viewBox', `0 0 ${width} ${height}`)

  const root = svg.append('g').attr('transform', `translate(${width / 2},${height / 2})`)

  const total = d3.sum(props.data, (d) => d.value)
  const pie = d3
    .pie<DonutDatum>()
    .value((d) => d.value)
    .sort(null)
    .padAngle(0.02)
  const arc = d3
    .arc<d3.PieArcDatum<DonutDatum>>()
    .innerRadius(radius * 0.62)
    .outerRadius(radius)
    .cornerRadius(4)

  root
    .append('g')
    .selectAll('path')
    .data(pie(props.data))
    .join('path')
    .attr('d', arc)
    .attr('fill', (d) => d.data.color)
    .style('cursor', 'pointer')
    .on('mousemove', (event: MouseEvent, d: d3.PieArcDatum<DonutDatum>) => {
      if (!containerRef.value) return
      const pct = total ? ((d.data.value / total) * 100).toFixed(1) : '0'
      showTooltip(event, containerRef.value, [d.data.label, `${props.valueFormat(d.data.value)} (${pct}%)`])
    })
    .on('mouseleave', hideTooltip)

  if (props.centerValue) {
    root
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '-0.1em')
      .attr('fill', ink.primary)
      .attr('font-size', Math.max(18, radius * 0.32))
      .attr('font-weight', 600)
      .text(props.centerValue)
  }
  if (props.centerLabel) {
    root
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '1.4em')
      .attr('fill', ink.muted)
      .attr('font-size', 11)
      .text(props.centerLabel)
  }
}

watchEffect(render)
watch(
  () => props.data,
  () => render(),
  { deep: true },
)
</script>

<template>
  <div class="flex flex-col items-center gap-4 sm:flex-row sm:items-center">
    <div ref="containerRef" class="relative w-full max-w-55 shrink-0">
      <svg ref="svgRef" class="w-full overflow-visible"></svg>
      <ChartTooltip v-bind="tooltip" />
    </div>
    <ul class="flex flex-1 flex-col gap-2 text-sm">
      <li v-for="item in props.data" :key="item.label" class="flex items-center justify-between gap-3">
        <span class="flex items-center gap-2 text-slate-300">
          <span class="h-2.5 w-2.5 shrink-0 rounded-full" :style="{ backgroundColor: item.color }" />
          {{ item.label }}
        </span>
        <span class="font-medium text-slate-400">{{ props.valueFormat(item.value) }}</span>
      </li>
    </ul>
  </div>
</template>
