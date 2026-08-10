export const categoricalPalette = [
  '#3987e5',
  '#d95926',
  '#199e70',
  '#c98500',
  '#d55181',
  '#008300',
  '#9085e9',
  '#e66767',
]

export const statusPalette = {
  good: '#0ca30c',
  warning: '#fab219',
  serious: '#ec835a',
  critical: '#d03b3b',
}

export const ink = {
  primary: '#ffffff',
  secondary: '#c3c2b7',
  muted: '#898781',
}

export const gridline = '#2c2c2a'
export const baseline = '#383835'

export function categoricalColor(index: number): string {
  return categoricalPalette[index % categoricalPalette.length]
}
