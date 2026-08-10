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
}

const props = withDefaults(
  defineProps<{
    data: BarDatum[]
    color?: string
    valueFormat?: (value: number) => string
  }>(),
  {
    color: '#3987e5',
    valueFormat: (value: number) => value.toLocaleString(),
  },
)

const containerRef = ref<HTMLElement | null>(null)
const svgRef = ref<SVGSVGElement | null>(null)
const { dimensions } = useChartDimensions(containerRef, 0.42)
const { tooltip, showTooltip, hideTooltip } = useChartTooltip()

const margin = { top: 16, right: 16, bottom: 28, left: 44 }

function render(): void {
  if (!svgRef.value || dimensions.value.width === 0) return
  const { width, height } = dimensions.value
  const innerWidth = Math.max(0, width - margin.left - margin.right)
  const innerHeight = Math.max(0, height - margin.top - margin.bottom)

  const svg = d3.select(svgRef.value)
  svg.selectAll('*').remove()
  svg.attr('viewBox', `0 0 ${width} ${height}`)

  const root = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`)

  const x = d3
    .scaleBand()
    .domain(props.data.map((d) => d.label))
    .range([0, innerWidth])
    .padding(0.35)

  const maxValue = d3.max(props.data, (d) => d.value) ?? 0
  const y = d3
    .scaleLinear()
    .domain([0, maxValue === 0 ? 1 : maxValue])
    .nice()
    .range([innerHeight, 0])

  root
    .append('g')
    .attr('class', 'grid')
    .call(d3.axisLeft(y).ticks(4).tickSize(-innerWidth).tickFormat(() => ''))
    .call((g) => g.select('.domain').remove())
    .call((g) => g.selectAll('line').attr('stroke', gridline).attr('stroke-width', 1))

  root
    .append('g')
    .attr('transform', `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x).tickSize(0))
    .call((g) => g.select('.domain').attr('stroke', gridline))
    .call((g) => g.selectAll('text').attr('fill', ink.muted).attr('font-size', 11))

  root
    .append('g')
    .call(d3.axisLeft(y).ticks(4).tickSize(0).tickFormat((v) => d3.format('~s')(v as number)))
    .call((g) => g.select('.domain').remove())
    .call((g) => g.selectAll('text').attr('fill', ink.muted).attr('font-size', 11))

  const barWidth = Math.min(24, x.bandwidth())

  root
    .append('g')
    .selectAll('rect')
    .data(props.data)
    .join('rect')
    .attr('x', (d) => (x(d.label) ?? 0) + (x.bandwidth() - barWidth) / 2)
    .attr('y', (d) => y(d.value))
    .attr('width', barWidth)
    .attr('height', (d) => innerHeight - y(d.value))
    .attr('rx', 4)
    .attr('fill', props.color)
    .style('cursor', 'pointer')
    .on('mousemove', (event: MouseEvent, d: BarDatum) => {
      if (!containerRef.value) return
      showTooltip(event, containerRef.value, [d.label, props.valueFormat(d.value)])
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
  <div ref="containerRef" class="relative w-full">
    <svg ref="svgRef" class="w-full overflow-visible"></svg>
    <ChartTooltip v-bind="tooltip" />
  </div>
</template>
