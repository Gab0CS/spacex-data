import { httpClient } from './http'
import type { StarlinkSatellite } from '@/types'

export async function fetchStarlinkSatellites(): Promise<StarlinkSatellite[]> {
  const { data } = await httpClient.get<StarlinkSatellite[]>('/api/starlink')
  return data
}
