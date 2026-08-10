<script setup lang="ts">
import { ref, watch, watchEffect } from 'vue'
import * as d3 from 'd3'
import { useChartDimensions } from '@/composables/useChartDimensions'
import { useChartTooltip } from '@/composables/useChartTooltip'
import { gridline, ink } from './chartTheme'
import ChartTooltip from './ChartTooltip.vue'

interface ScatterDatum {
  id: string
  x: number
  y: number
  category: string
}

const props = defineProps<{
  data: ScatterDatum[]
  categoryColors: Record<string, string>
  xLabel: string
  yLabel: string
}>()

const containerRef = ref<HTMLElement | null>(null)
const svgRef = ref<SVGSVGElement | null>(null)
const { dimensions } = useChartDimensions(containerRef, 0.55)
const { tooltip, showTooltip, hideTooltip } = useChartTooltip()

const margin = { top: 16, right: 16, bottom: 40, left: 52 }

function render(): void {
  if (!svgRef.value || dimensions.value.width === 0) return
  const { width, height } = dimensions.value
  const innerWidth = Math.max(0, width - margin.left - margin.right)
  const innerHeight = Math.max(0, height - margin.top - margin.bottom)

  const svg = d3.select(svgRef.value)
  svg.selectAll('*').remove()
  svg.attr('viewBox', `0 0 ${width} ${height}`)

  const root = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`)

  const xExtent = d3.extent(props.data, (d) => d.x) as [number, number]
  const yExtent = d3.extent(props.data, (d) => d.y) as [number, number]
  const xPad = (xExtent[1] - xExtent[0]) * 0.05 || 1
  const yPad = (yExtent[1] - yExtent[0]) * 0.08 || 1

  const x = d3
    .scaleLinear()
    .domain([xExtent[0] - xPad, xExtent[1] + xPad])
    .range([0, innerWidth])
  const y = d3
    .scaleLinear()
    .domain([yExtent[0] - yPad, yExtent[1] + yPad])
    .nice()
    .range([innerHeight, 0])

  root
    .append('g')
    .call(d3.axisLeft(y).ticks(5).tickSize(-innerWidth).tickFormat(() => ''))
    .call((g) => g.select('.domain').remove())
    .call((g) => g.selectAll('line').attr('stroke', gridline).attr('stroke-width', 1))

  root
    .append('g')
    .attr('transform', `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x).ticks(6).tickSize(0))
    .call((g) => g.select('.domain').attr('stroke', gridline))
    .call((g) => g.selectAll('text').attr('fill', ink.muted).attr('font-size', 11))

  root
    .append('g')
    .call(d3.axisLeft(y).ticks(5).tickSize(0))
    .call((g) => g.select('.domain').remove())
    .call((g) => g.selectAll('text').attr('fill', ink.muted).attr('font-size', 11))

  root
    .append('text')
    .attr('x', innerWidth / 2)
    .attr('y', innerHeight + 34)
    .attr('text-anchor', 'middle')
    .attr('fill', ink.muted)
    .attr('font-size', 11)
    .text(props.xLabel)

  root
    .append('text')
    .attr('transform', 'rotate(-90)')
    .attr('x', -innerHeight / 2)
    .attr('y', -38)
    .attr('text-anchor', 'middle')
    .attr('fill', ink.muted)
    .attr('font-size', 11)
    .text(props.yLabel)

  root
    .append('g')
    .selectAll('circle')
    .data(props.data)
    .join('circle')
    .attr('cx', (d) => x(d.x))
    .attr('cy', (d) => y(d.y))
    .attr('r', 3.5)
    .attr('fill', (d) => props.categoryColors[d.category] ?? ink.muted)
    .attr('fill-opacity', 0.75)
    .style('cursor', 'pointer')
    .on('mousemove', (event: MouseEvent, d: ScatterDatum) => {
      if (!containerRef.value) return
      showTooltip(event, containerRef.value, [
        d.id,
        `${props.xLabel}: ${d.x.toLocaleString()}`,
        `${props.yLabel}: ${d.y.toLocaleString()}`,
      ])
    })
    .on('mouseleave', hideTooltip)
}

watchEffect(render)
watch(
  () => props.data,
  () => render(),
  { deep: true },
)
</script>

<template>
  <div class="flex flex-col gap-3">
    <div ref="containerRef" class="relative w-full">
      <svg ref="svgRef" class="w-full overflow-visible"></svg>
      <ChartTooltip v-bind="tooltip" />
    </div>
    <ul class="flex flex-wrap gap-4 text-xs text-slate-400">
      <li v-for="(color, category) in categoryColors" :key="category" class="flex items-center gap-1.5">
        <span class="h-2.5 w-2.5 rounded-full" :style="{ backgroundColor: color }" />
        {{ category }}
      </li>
    </ul>
  </div>
</template>
