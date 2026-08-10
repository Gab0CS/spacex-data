export interface SpaceTrack {
  OBJECT_NAME: string | null
  OBJECT_ID: string | null
  EPOCH: string | null
  MEAN_MOTION: number | null
  ECCENTRICITY: number | null
  INCLINATION: number | null
  RA_OF_ASC_NODE: number | null
  ARG_OF_PERICENTER: number | null
  MEAN_ANOMALY: number | null
  NORAD_CAT_ID: number | null
  SEMIMAJOR_AXIS: number | null
  PERIOD: number | null
  APOAPSIS: number | null
  PERIAPSIS: number | null
  OBJECT_TYPE: string | null
  COUNTRY_CODE: string | null
  LAUNCH_DATE: string | null
  SITE: string | null
  DECAY_DATE: string | null
  DECAYED: number | null
}

export interface StarlinkSatellite {
  id: string
  version: string | null
  launch: string | null
  longitude: number | null
  latitude: number | null
  height_km: number | null
  velocity_kms: number | null
  spaceTrack: SpaceTrack | null
  is_active: boolean
}
