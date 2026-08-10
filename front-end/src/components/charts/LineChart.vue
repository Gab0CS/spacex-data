<script setup lang="ts">
import { ref, watch, watchEffect } from 'vue'
import * as d3 from 'd3'
import { useChartDimensions } from '@/composables/useChartDimensions'
import { useChartTooltip } from '@/composables/useChartTooltip'
import { gridline, ink } from './chartTheme'
import ChartTooltip from './ChartTooltip.vue'

interface LineDatum {
  x: number
  y: number
}

const props = withDefaults(
  defineProps<{
    data: LineDatum[]
    color?: string
    valueFormat?: (value: number) => string
    xFormat?: (value: number) => string
  }>(),
  {
    color: '#3987e5',
    valueFormat: (value: number) => value.toLocaleString(),
    xFormat: (value: number) => String(value),
  },
)

const containerRef = ref<HTMLElement | null>(null)
const svgRef = ref<SVGSVGElement | null>(null)
const { dimensions } = useChartDimensions(containerRef, 0.42)
const { tooltip, showTooltip, hideTooltip } = useChartTooltip()

const margin = { top: 16, right: 20, bottom: 28, left: 44 }

function render(): void {
  if (!svgRef.value || dimensions.value.width === 0 || props.data.length === 0) return
  const { width, height } = dimensions.value
  const innerWidth = Math.max(0, width - margin.left - margin.right)
  const innerHeight = Math.max(0, height - margin.top - margin.bottom)

  const svg = d3.select(svgRef.value)
  svg.selectAll('*').remove()
  svg.attr('viewBox', `0 0 ${width} ${height}`)

  const root = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`)

  const xExtent = d3.extent(props.data, (d) => d.x) as [number, number]
  const x = d3.scaleLinear().domain(xExtent).range([0, innerWidth])

  const maxY = d3.max(props.data, (d) => d.y) ?? 0
  const y = d3
    .scaleLinear()
    .domain([0, maxY === 0 ? 1 : maxY])
    .nice()
    .range([innerHeight, 0])

  root
    .append('g')
    .call(d3.axisLeft(y).ticks(4).tickSize(-innerWidth).tickFormat(() => ''))
    .call((g) => g.select('.domain').remove())
    .call((g) => g.selectAll('line').attr('stroke', gridline).attr('stroke-width', 1))

  root
    .append('g')
    .attr('transform', `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x).ticks(Math.min(props.data.length, 8)).tickFormat((v) => props.xFormat(v as number)).tickSize(0))
    .call((g) => g.select('.domain').attr('stroke', gridline))
    .call((g) => g.selectAll('text').attr('fill', ink.muted).attr('font-size', 11))

  root
    .append('g')
    .call(d3.axisLeft(y).ticks(4).tickSize(0).tickFormat((v) => d3.format('~s')(v as number)))
    .call((g) => g.select('.domain').remove())
    .call((g) => g.selectAll('text').attr('fill', ink.muted).attr('font-size', 11))

  const area = d3
    .area<LineDatum>()
    .x((d) => x(d.x))
    .y0(innerHeight)
    .y1((d) => y(d.y))
    .curve(d3.curveMonotoneX)

  const line = d3
    .line<LineDatum>()
    .x((d) => x(d.x))
    .y((d) => y(d.y))
    .curve(d3.curveMonotoneX)

  root.append('path').datum(props.data).attr('fill', props.color).attr('fill-opacity', 0.1).attr('d', area)

  root
    .append('path')
    .datum(props.data)
    .attr('fill', 'none')
    .attr('stroke', props.color)
    .attr('stroke-width', 2)
    .attr('stroke-linejoin', 'round')
    .attr('stroke-linecap', 'round')
    .attr('d', line)

  root
    .append('g')
    .selectAll('circle')
    .data(props.data)
    .join('circle')
    .attr('cx', (d) => x(d.x))
    .attr('cy', (d) => y(d.y))
    .attr('r', 5)
    .attr('fill', props.color)
    .attr('stroke', '#0f172a')
    .attr('stroke-width', 2)
    .style('cursor', 'pointer')
    .on('mousemove', (event: MouseEvent, d: LineDatum) => {
      if (!containerRef.value) return
      showTooltip(event, containerRef.value, [props.xFormat(d.x), props.valueFormat(d.y)])
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
