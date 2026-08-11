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

const props = withDefaults(
  defineProps<{
    data: ScatterDatum[]
    categoryColors: Record<string, string>
    xLabel: string
    yLabel: string
    itemLabel?: string
  }>(),
  { itemLabel: 'points' },
)

interface PixelPoint {
  datum: ScatterDatum
  cx: number
  cy: number
}

interface PointCluster {
  cx: number
  cy: number
  points: ScatterDatum[]
  pixelPoints: PixelPoint[]
}

const CLUSTER_RADIUS_PX = 5

function clusterPoints(points: PixelPoint[]): PointCluster[] {
  const clusters: PointCluster[] = []
  for (const point of points) {
    const match = clusters.find((c) => Math.hypot(c.cx - point.cx, c.cy - point.cy) <= CLUSTER_RADIUS_PX)
    if (match) {
      match.pixelPoints.push(point)
      match.points.push(point.datum)
      match.cx = d3.mean(match.pixelPoints, (p) => p.cx) ?? match.cx
      match.cy = d3.mean(match.pixelPoints, (p) => p.cy) ?? match.cy
    } else {
      clusters.push({ cx: point.cx, cy: point.cy, points: [point.datum], pixelPoints: [point] })
    }
  }
  return clusters
}

function dominantColor(points: ScatterDatum[]): string {
  const counts = d3.rollup(
    points,
    (v) => v.length,
    (p) => p.category,
  )
  const [topCategory] = [...counts.entries()].sort((a, b) => b[1] - a[1])[0]
  return props.categoryColors[topCategory] ?? ink.muted
}

function clusterTooltipLines(cluster: PointCluster): string[] {
  if (cluster.points.length === 1) {
    const d = cluster.points[0]
    return [d.id, `${props.xLabel}: ${d.x.toLocaleString()}`, `${props.yLabel}: ${d.y.toLocaleString()}`]
  }
  const labels = new Set(cluster.points.map((p) => p.id))
  const avgX = d3.mean(cluster.points, (p) => p.x) ?? 0
  const avgY = d3.mean(cluster.points, (p) => p.y) ?? 0
  return [
    `${cluster.points.length} ${props.itemLabel}`,
    labels.size === 1 ? [...labels][0] : `${labels.size} groups`,
    `${props.xLabel}: ${avgX.toFixed(1)}`,
    `${props.yLabel}: ${avgY.toFixed(1)}`,
  ]
}

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

  const pixelPoints: PixelPoint[] = props.data.map((datum) => ({ datum, cx: x(datum.x), cy: y(datum.y) }))
  const clusters = clusterPoints(pixelPoints)

  root
    .append('g')
    .selectAll('circle')
    .data(clusters)
    .join('circle')
    .attr('cx', (c) => c.cx)
    .attr('cy', (c) => c.cy)
    .attr('r', (c) => Math.min(12, 3.5 + (c.points.length - 1) * 1.5))
    .attr('fill', (c) => dominantColor(c.points))
    .attr('fill-opacity', 0.78)
    .attr('stroke', (c) => (c.points.length > 1 ? '#0f172a' : 'none'))
    .attr('stroke-width', 1.5)
    .style('cursor', 'pointer')
    .on('mousemove', (event: MouseEvent, c: PointCluster) => {
      if (!containerRef.value) return
      showTooltip(event, containerRef.value, clusterTooltipLines(c))
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
