import { httpClient } from './http'
import type { Launch } from '@/types'

export async function fetchLaunches(): Promise<Launch[]> {
  const { data } = await httpClient.get<Launch[]>('/api/launches')
  return data
}
