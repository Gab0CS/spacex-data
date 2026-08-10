export type SortDirection = 'asc' | 'desc'

export interface SortState<TKey extends string = string> {
  key: TKey | null
  direction: SortDirection
}

export interface TableColumn<TRow, TKey extends string = string> {
  key: TKey
  label: string
  sortable?: boolean
  align?: 'left' | 'right' | 'center'
  accessor: (row: TRow) => unknown
  format?: (row: TRow) => string
}

export interface SelectOption {
  label: string
  value: string
}
