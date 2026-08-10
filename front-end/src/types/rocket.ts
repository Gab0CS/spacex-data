export interface Distance {
  meters: number | null
  feet: number | null
}

export interface Mass {
  kg: number | null
  lb: number | null
}

export interface PayloadWeight {
  id: string
  name: string
  kg: number | null
  lb: number | null
}

export interface Thrust {
  kN: number | null
  lbf: number | null
}

export interface FirstStage {
  reusable: boolean | null
  engines: number | null
  fuel_amount_tons: number | null
  burn_time_sec: number | null
  thrust_sea_level: Thrust | null
  thrust_vacuum: Thrust | null
}

export interface SecondStage {
  engines: number | null
  fuel_amount_tons: number | null
  burn_time_sec: number | null
  thrust: Thrust | null
}

export interface Engines {
  number: number | null
  type: string | null
  version: string | null
  layout: string | null
  propellant_1: string | null
  propellant_2: string | null
  thrust_to_weight: number | null
}

export interface LandingLegs {
  number: number | null
  material: string | null
}

export interface Rocket {
  id: number | string | null
  rocket_id: string
  rocket_name: string
  rocket_type: string | null
  active: boolean
  stages: number
  boosters: number
  cost_per_launch: number | null
  success_rate_pct: number | null
  first_flight: string | null
  country: string | null
  company: string | null
  height: Distance | null
  diameter: Distance | null
  mass: Mass | null
  payload_weights: PayloadWeight[]
  first_stage: FirstStage | null
  second_stage: SecondStage | null
  engines: Engines | null
  landing_legs: LandingLegs | null
  wikipedia: string | null
  description: string | null
}
