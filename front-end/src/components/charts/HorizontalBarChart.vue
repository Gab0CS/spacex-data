<script setup lang="ts">
import { ref, watch, watchEffect } from 'vue'
import * as d3 from 'd3'
import { useChartDimensions } from '@/composables/useChartDimensions'
import { useChartTooltip } from '@/composables/useChartTooltip'
import { gridline, ink } from './chartTheme'
import ChartTooltip from './ChartTooltip.vue'

interface BarDatum {
  label: string
  value: number
  color?: string
}

const props = withDefaults(
  defineProps<{
    data: BarDatum[]
    color?: string
    valueFormat?: (value: number) => string
    domainMax?: number
  }>(),
  {
    color: '#3987e5',
    valueFormat: (value: number) => value.toLocaleString(),
    domainMax: undefined,
  },
)

const containerRef = ref<HTMLElement | null>(null)
const svgRef = ref<SVGSVGElement | null>(null)
const { dimensions } = useChartDimensions(containerRef, 0.09)
const { tooltip, showTooltip, hideTooltip } = useChartTooltip()

const margin = { top: 8, right: 44, bottom: 8, left: 120 }

function render(): void {
  if (!svgRef.value || dimensions.value.width === 0) return
  const rowHeight = 32
  const height = props.data.length * rowHeight + margin.top + margin.bottom
  const width = dimensions.value.width
  const innerWidth = Math.max(0, width - margin.left - margin.right)

  const svg = d3.select(svgRef.value)
  svg.selectAll('*').remove()
  svg.attr('viewBox', `0 0 ${width} ${height}`)

  const root = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`)

  const y = d3
    .scaleBand()
    .domain(props.data.map((d) => d.label))
    .range([0, height - margin.top - margin.bottom])
    .padding(0.35)

  const maxValue = props.domainMax ?? d3.max(props.data, (d) => d.value) ?? 0
  const x = d3
    .scaleLinear()
    .domain([0, maxValue === 0 ? 1 : maxValue])
    .nice()
    .range([0, innerWidth])

  root
    .append('g')
    .call(d3.axisTop(x).ticks(4).tickSize(-(height - margin.top - margin.bottom)).tickFormat(() => ''))
    .call((g) => g.select('.domain').remove())
    .call((g) => g.selectAll('line').attr('stroke', gridline).attr('stroke-width', 1))

  root
    .append('g')
    .call(d3.axisLeft(y).tickSize(0))
    .call((g) => g.select('.domain').remove())
    .call((g) => g.selectAll('text').attr('fill', ink.secondary).attr('font-size', 12))

  const barHeight = Math.min(20, y.bandwidth())

  root
    .append('g')
    .selectAll('rect')
    .data(props.data)
    .join('rect')
    .attr('x', 0)
    .attr('y', (d) => (y(d.label) ?? 0) + (y.bandwidth() - barHeight) / 2)
    .attr('width', (d) => Math.max(2, x(d.value)))
    .attr('height', barHeight)
    .attr('rx', 4)
    .attr('fill', (d) => d.color ?? props.color)
    .style('cursor', 'pointer')
    .on('mousemove', (event: MouseEvent, d: BarDatum) => {
      if (!containerRef.value) return
      showTooltip(event, containerRef.value, [d.label, props.valueFormat(d.value)])
    })
    .on('mouseleave', hideTooltip)

  root
    .append('g')
    .selectAll('text')
    .data(props.data)
    .join('text')
    .attr('x', (d) => x(d.value) + 8)
    .attr('y', (d) => (y(d.label) ?? 0) + y.bandwidth() / 2)
    .attr('dominant-baseline', 'middle')
    .attr('fill', ink.secondary)
    .attr('font-size', 11)
    .text((d) => props.valueFormat(d.value))
}

watchEffect(render)
watch(
  () => props.data,
  () => render(),
  { deep: true },
)
</script>

<template>
  <div ref="containerRef" class="relative w-full">
    <svg ref="svgRef" class="w-full overflow-visible"></svg>
    <ChartTooltip v-bind="tooltip" />
  </div>
</template>
