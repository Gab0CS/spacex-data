import { httpClient } from './http'
import type { DashboardStats } from '@/types'

export async function fetchDashboardStats(): Promise<DashboardStats> {
  const { data } = await httpClient.get<DashboardStats>('/api/dashboard')
  return data
}
