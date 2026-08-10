export interface OrbitParams {
  reference_system: string | null
  regime: string | null
  longitude: number | null
  semi_major_axis_km: number | null
  eccentricity: number | null
  periapsis_km: number | null
  apoapsis_km: number | null
  inclination_deg: number | null
  period_min: number | null
  lifespan_years: number | null
  epoch: string | null
  mean_motion: number | null
  raan: number | null
  arg_of_pericenter: number | null
  mean_anomaly: number | null
}

export interface Payload {
  payload_id: string
  norad_id: number[]
  reused: boolean
  customers: string[]
  nationality: string | null
  manufacturer: string | null
  payload_type: string | null
  payload_mass_kg: number | null
  payload_mass_lbs: number | null
  orbit: string | null
  orbit_params: OrbitParams | null
}

export interface Core {
  core_serial: string | null
  flight: number | null
  block: number | null
  gridfins: boolean | null
  legs: boolean | null
  reused: boolean | null
  land_success: boolean | null
  landing_intent: boolean | null
  landing_type: string | null
  landing_vehicle: string | null
}

export interface FirstStageInfo {
  cores: Core[]
}

export interface SecondStageInfo {
  block: number | null
  payloads: Payload[]
}

export interface Fairings {
  reused: boolean | null
  recovery_attempt: boolean | null
  recovered: boolean | null
  ship: string | null
}

export interface LaunchRocket {
  rocket_id: string
  rocket_name: string
  rocket_type: string | null
  first_stage: FirstStageInfo | null
  second_stage: SecondStageInfo | null
  fairings: Fairings | null
}

export interface LaunchSite {
  site_id: string | null
  site_name: string | null
  site_name_long: string | null
}

export interface LaunchLinks {
  mission_patch: string | null
  mission_patch_small: string | null
  article_link: string | null
  wikipedia: string | null
  video_link: string | null
  youtube_id: string | null
  flickr_images: string[]
}

export interface LaunchFailureDetails {
  time: number | null
  altitude: number | null
  reason: string | null
}

export interface Launch {
  id: string
  flight_number: number
  mission_name: string
  mission_id: string[]
  upcoming: boolean
  launch_year: string | null
  launch_date_unix: number | null
  launch_date_utc: string
  launch_date_local: string | null
  is_tentative: boolean
  tbd: boolean
  launch_window: number | null
  rocket: LaunchRocket
  ships: string[]
  launch_site: LaunchSite | null
  launch_success: boolean | null
  launch_failure_details: LaunchFailureDetails | null
  links: LaunchLinks | null
  details: string | null
  static_fire_date_utc: string | null
}
