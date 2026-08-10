export interface DashboardStats {
  total_rockets: number
  total_launches: number
  successful_launches: number
  failed_launches: number
  launch_success_rate: number
  active_starlink_satellites: number
  inactive_starlink_satellites: number
  launches_per_year: Record<number, number>
}
