import { reactive } from 'vue'

interface TooltipState {
  visible: boolean
  x: number
  y: number
  lines: string[]
}

export function useChartTooltip() {
  const tooltip = reactive<TooltipState>({ visible: false, x: 0, y: 0, lines: [] })

  function showTooltip(event: MouseEvent, container: HTMLElement, lines: string[]): void {
    const rect = container.getBoundingClientRect()
    tooltip.x = event.clientX - rect.left
    tooltip.y = event.clientY - rect.top
    tooltip.lines = lines
    tooltip.visible = true
  }

  function hideTooltip(): void {
    tooltip.visible = false
  }

  return { tooltip, showTooltip, hideTooltip }
}
