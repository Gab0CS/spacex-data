import { httpClient } from './http'
import type { Rocket } from '@/types'

export async function fetchRockets(): Promise<Rocket[]> {
  const { data } = await httpClient.get<Rocket[]>('/api/rockets')
  return data
}
