import { onBeforeUnmount, onMounted, ref, type Ref } from 'vue'

interface ChartDimensions {
  width: number
  height: number
}

export function useChartDimensions(
  containerRef: Ref<HTMLElement | null>,
  aspectRatio = 0.5,
) {
  const dimensions = ref<ChartDimensions>({ width: 0, height: 0 })
  let observer: ResizeObserver | null = null

  function measure(entry: HTMLElement): void {
    const width = entry.clientWidth
    dimensions.value = { width, height: Math.max(220, width * aspectRatio) }
  }

  onMounted(() => {
    if (!containerRef.value) return
    measure(containerRef.value)
    observer = new ResizeObserver((entries) => {
      const entry = entries[0]
      if (entry) measure(entry.target as HTMLElement)
    })
    observer.observe(containerRef.value)
  })

  onBeforeUnmount(() => {
    observer?.disconnect()
  })

  return { dimensions }
}
