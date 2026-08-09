from __future__ import annotations

_FALCON1_BASE: dict = {
    "stages": 2,
    "boosters": 0,
    "cost_per_launch": 7000000,
    "country": "Republic of the Marshall Islands",
    "company": "SpaceX",
    "height": {"meters": 22.25, "feet": 73},
    "diameter": {"meters": 1.68, "feet": 5.5},
    "mass": {"kg": 30146, "lb": 66460},
    "payload_weights": [
        {"id": "leo", "name": "Low Earth Orbit", "kg": 450, "lb": 992},
    ],
    "first_stage": {
        "reusable": False,
        "engines": 1,
        "fuel_amount_tons": 44.3,
        "burn_time_sec": 169,
        "thrust_sea_level": {"kN": 420, "lbf": 94000},
        "thrust_vacuum": {"kN": 480, "lbf": 108000},
    },
    "second_stage": {
        "engines": 1,
        "fuel_amount_tons": 3.38,
        "burn_time_sec": 378,
        "thrust": {"kN": 31, "lbf": 6900},
        "payloads": {
            "option_1": "satellite",
            "option_2": "composite fairing",
            "composite_fairing": {
                "height": {"meters": 3.5, "feet": 11.5},
                "diameter": {"meters": 1.5, "feet": 4.9},
            },
        },
    },
    "engines": {
        "number": 1,
        "type": "merlin",
        "version": "1C",
        "layout": "single",
        "engine_loss_max": 0,
        "propellant_1": "liquid oxygen",
        "propellant_2": "RP-1 kerosene",
        "thrust_sea_level": {"kN": 420, "lbf": 94000},
        "thrust_vacuum": {"kN": 480, "lbf": 108000},
        "thrust_to_weight": 96,
    },
    "landing_legs": {"number": 0, "material": None},
    "wikipedia": "https://en.wikipedia.org/wiki/Falcon_1",
    "rocket_type": "rocket",
}

_FALCON9_BASE: dict = {
    "stages": 2,
    "boosters": 0,
    "cost_per_launch": 62000000,
    "country": "United States",
    "company": "SpaceX",
    "height": {"meters": 70, "feet": 229.6},
    "diameter": {"meters": 3.7, "feet": 12},
    "mass": {"kg": 549054, "lb": 1207920},
    "payload_weights": [
        {"id": "leo", "name": "Low Earth Orbit", "kg": 22800, "lb": 50265},
        {"id": "gto", "name": "Geosynchronous Transfer Orbit", "kg": 8300, "lb": 18300},
        {"id": "mars", "name": "Mars Orbit", "kg": 4020, "lb": 8860},
    ],
    "first_stage": {
        "reusable": True,
        "engines": 9,
        "fuel_amount_tons": 385,
        "burn_time_sec": 162,
        "thrust_sea_level": {"kN": 7607, "lbf": 1710000},
        "thrust_vacuum": {"kN": 8227, "lbf": 1849500},
    },
    "second_stage": {
        "engines": 1,
        "fuel_amount_tons": 90,
        "burn_time_sec": 397,
        "thrust": {"kN": 934, "lbf": 210000},
        "payloads": {
            "option_1": "dragon",
            "option_2": "composite fairing",
            "composite_fairing": {
                "height": {"meters": 13.1, "feet": 43},
                "diameter": {"meters": 5.2, "feet": 17.1},
            },
        },
    },
    "engines": {
        "number": 9,
        "type": "merlin",
        "version": "1D+",
        "layout": "octaweb",
        "engine_loss_max": 2,
        "propellant_1": "liquid oxygen",
        "propellant_2": "RP-1 kerosene",
        "thrust_sea_level": {"kN": 845, "lbf": 190000},
        "thrust_vacuum": {"kN": 914, "lbf": 205500},
        "thrust_to_weight": 180.1,
    },
    "landing_legs": {"number": 4, "material": "carbon fiber"},
    "wikipedia": "https://en.wikipedia.org/wiki/Falcon_9",
    "rocket_type": "rocket",
}

_FALCONHEAVY_BASE: dict = {
    **_FALCON9_BASE,
    "boosters": 2,
    "cost_per_launch": 90000000,
    "mass": {"kg": 1420788, "lb": 3125735},
    "payload_weights": [
        {"id": "leo", "name": "Low Earth Orbit", "kg": 63800, "lb": 140660},
        {"id": "gto", "name": "Geosynchronous Transfer Orbit", "kg": 26700, "lb": 58860},
        {"id": "mars", "name": "Mars Orbit", "kg": 16800, "lb": 37040},
    ],
    "first_stage": {
        "reusable": True,
        "engines": 27,
        "fuel_amount_tons": 1155,
        "burn_time_sec": 162,
        "thrust_sea_level": {"kN": 22819, "lbf": 5130000},
        "thrust_vacuum": {"kN": 24681, "lbf": 5548500},
    },
    "engines": {
        **_FALCON9_BASE["engines"],
        "number": 27,
    },
    "wikipedia": "https://en.wikipedia.org/wiki/Falcon_Heavy",
}

_STARSHIP_BASE: dict = {
    "stages": 2,
    "boosters": 0,
    "cost_per_launch": 10000000,
    "country": "United States",
    "company": "SpaceX",
    "height": {"meters": 120, "feet": 394},
    "diameter": {"meters": 9, "feet": 29.5},
    "mass": {"kg": 5000000, "lb": 11023113},
    "payload_weights": [
        {"id": "leo", "name": "Low Earth Orbit", "kg": 150000, "lb": 330693},
        {"id": "mars", "name": "Mars Orbit", "kg": 100000, "lb": 220462},
    ],
    "first_stage": {
        "reusable": True,
        "engines": 33,
        "fuel_amount_tons": 3400,
        "burn_time_sec": 169,
        "thrust_sea_level": {"kN": 74500, "lbf": 16750000},
        "thrust_vacuum": {"kN": 77000, "lbf": 17300000},
    },
    "second_stage": {
        "engines": 6,
        "fuel_amount_tons": 1200,
        "burn_time_sec": 400,
        "thrust": {"kN": 12420, "lbf": 2793000},
        "payloads": {
            "option_1": "starlink",
            "option_2": "cargo bay",
            "composite_fairing": {
                "height": {"meters": 17.24, "feet": 56.6},
                "diameter": {"meters": 9, "feet": 29.5},
            },
        },
    },
    "engines": {
        "number": 39,
        "type": "raptor",
        "version": "2",
        "layout": "circular",
        "engine_loss_max": 3,
        "propellant_1": "liquid oxygen",
        "propellant_2": "liquid methane",
        "thrust_sea_level": {"kN": 2200, "lbf": 494700},
        "thrust_vacuum": {"kN": 2300, "lbf": 517100},
        "thrust_to_weight": 158,
    },
    "landing_legs": {"number": 0, "material": None},
    "wikipedia": "https://en.wikipedia.org/wiki/SpaceX_Starship",
    "rocket_type": "rocket",
}

_CONCEPT_BASE: dict = {
    "stages": 2,
    "boosters": 0,
    "cost_per_launch": None,
    "country": "United States",
    "company": "SpaceX",
    "height": {"meters": None, "feet": None},
    "diameter": {"meters": None, "feet": None},
    "mass": {"kg": None, "lb": None},
    "payload_weights": [],
    "first_stage": {
        "reusable": True,
        "engines": None,
        "fuel_amount_tons": None,
        "burn_time_sec": None,
        "thrust_sea_level": {"kN": None, "lbf": None},
        "thrust_vacuum": {"kN": None, "lbf": None},
    },
    "second_stage": {
        "engines": None,
        "fuel_amount_tons": None,
        "burn_time_sec": None,
        "thrust": {"kN": None, "lbf": None},
        "payloads": {"option_1": None, "option_2": None, "composite_fairing": None},
    },
    "engines": {
        "number": None,
        "type": "raptor",
        "version": None,
        "layout": None,
        "engine_loss_max": None,
        "propellant_1": "liquid oxygen",
        "propellant_2": "liquid methane",
        "thrust_sea_level": {"kN": None, "lbf": None},
        "thrust_vacuum": {"kN": None, "lbf": None},
        "thrust_to_weight": None,
    },
    "landing_legs": {"number": 0, "material": None},
    "wikipedia": "https://en.wikipedia.org/wiki/SpaceX_launch_vehicles",
    "rocket_type": "concept",
}


def _rocket(base: dict, **overrides: object) -> dict:
    return {**base, **overrides}


_ROCKET_DEFS: list[dict] = [
    _rocket(
        _FALCON1_BASE, rocket_id="falcon1", rocket_name="Falcon 1", active=False, success_rate_pct=40,
        first_flight="2006-03-24",
        description="The Falcon 1 was an expendable launch system privately developed and manufactured by SpaceX.",
    ),
    _rocket(
        _FALCON1_BASE, rocket_id="falcon1e", rocket_name="Falcon 1e", active=False, success_rate_pct=None,
        first_flight="2011-01-01",
        description="A planned upgrade of the Falcon 1 with a more powerful first stage; retired before flying.",
    ),
    _rocket(
        _FALCON9_BASE, rocket_id="falcon9-v1-0", rocket_name="Falcon 9 v1.0", active=False, success_rate_pct=100,
        first_flight="2010-06-04", cost_per_launch=54000000,
        description="The original Falcon 9 variant, flown five times between 2010 and 2013.",
    ),
    _rocket(
        _FALCON9_BASE, rocket_id="falcon9-v1-1", rocket_name="Falcon 9 v1.1", active=False, success_rate_pct=93,
        first_flight="2013-09-29", cost_per_launch=56500000,
        description="An upgraded Falcon 9 with 60% more thrust and stretched propellant tanks.",
    ),
    _rocket(
        _FALCON9_BASE, rocket_id="falcon9-ft", rocket_name="Falcon 9 Full Thrust", active=False, success_rate_pct=97,
        first_flight="2015-12-22", cost_per_launch=61000000,
        description="Falcon 9 Full Thrust introduced subcooled propellant and first-stage landings.",
    ),
    _rocket(
        _FALCON9_BASE, rocket_id="falcon9-block3", rocket_name="Falcon 9 Block 3", active=False, success_rate_pct=96,
        first_flight="2017-01-14", cost_per_launch=62000000,
        description="An interim Falcon 9 block focused on reliability improvements after the AMOS-6 anomaly.",
    ),
    _rocket(
        _FALCON9_BASE, rocket_id="falcon9-block4", rocket_name="Falcon 9 Block 4", active=False, success_rate_pct=98,
        first_flight="2017-08-24", cost_per_launch=62000000,
        description="Falcon 9 Block 4 bridged Block 3 and Block 5 with incremental thrust and reuse upgrades.",
    ),
    _rocket(
        _FALCON9_BASE, rocket_id="falcon9-block5", rocket_name="Falcon 9 Block 5", active=True, success_rate_pct=99,
        first_flight="2018-05-11", cost_per_launch=67000000,
        description="Falcon 9 Block 5 is the final major iteration, built for rapid reusability and high flight rates.",
    ),
    _rocket(
        _FALCON9_BASE, rocket_id="falcon9-crew", rocket_name="Falcon 9 Block 5 (Crew)", active=True, success_rate_pct=100,
        first_flight="2020-05-30", cost_per_launch=55000000,
        description="The human-rated Falcon 9 Block 5 configuration used to launch Crew Dragon missions.",
    ),
    _rocket(
        _FALCON9_BASE, rocket_id="falcon9-cargo", rocket_name="Falcon 9 Block 5 (Cargo)", active=True, success_rate_pct=98,
        first_flight="2020-12-06", cost_per_launch=62000000,
        description="The cargo-optimized Falcon 9 Block 5 configuration used for Cargo Dragon resupply missions.",
    ),
    _rocket(
        _FALCONHEAVY_BASE, rocket_id="falconheavy-demo", rocket_name="Falcon Heavy Demo", active=False, success_rate_pct=100,
        first_flight="2018-02-06",
        description="The Falcon Heavy demonstration flight, famous for launching a Tesla Roadster toward Mars.",
    ),
    _rocket(
        _FALCONHEAVY_BASE, rocket_id="falconheavy", rocket_name="Falcon Heavy", active=True, success_rate_pct=100,
        first_flight="2019-04-11",
        description="With the ability to lift into orbit over 63 metric tons, Falcon Heavy is among the most capable rockets flying.",
    ),
    _rocket(
        _FALCONHEAVY_BASE, rocket_id="falconheavy-expendable", rocket_name="Falcon Heavy (Expendable)", active=True,
        success_rate_pct=100, first_flight="2019-06-25", cost_per_launch=150000000,
        description="A fully expendable Falcon Heavy configuration used for the heaviest, highest-energy payloads.",
    ),
    _rocket(
        _FALCONHEAVY_BASE, rocket_id="falconheavy-reusable", rocket_name="Falcon Heavy (Recoverable)", active=True,
        success_rate_pct=100, first_flight="2018-04-11",
        description="A Falcon Heavy configuration that recovers all three boosters for reuse.",
    ),
    _rocket(
        _STARSHIP_BASE, rocket_id="starship-ift1", rocket_name="Starship IFT-1", active=False, success_rate_pct=0,
        first_flight="2023-04-20",
        description="The first integrated flight test of Starship and Super Heavy, ending in a flight termination.",
    ),
    _rocket(
        _STARSHIP_BASE, rocket_id="starship-ift2", rocket_name="Starship IFT-2", active=False, success_rate_pct=50,
        first_flight="2023-11-18",
        description="The second integrated flight test, achieving hot-staging separation for the first time.",
    ),
    _rocket(
        _STARSHIP_BASE, rocket_id="starship-ift3", rocket_name="Starship IFT-3", active=False, success_rate_pct=80,
        first_flight="2024-03-14",
        description="The third integrated flight test, reaching orbital velocity and testing a payload door.",
    ),
    _rocket(
        _STARSHIP_BASE, rocket_id="starship-ift4", rocket_name="Starship IFT-4", active=False, success_rate_pct=100,
        first_flight="2024-06-06",
        description="The fourth integrated flight test, completing controlled splashdowns of both stages.",
    ),
    _rocket(
        _STARSHIP_BASE, rocket_id="starship-ift5", rocket_name="Starship IFT-5", active=False, success_rate_pct=100,
        first_flight="2024-10-13",
        description="The fifth integrated flight test, marking the first catch of a Super Heavy booster with the launch tower.",
    ),
    _rocket(
        _STARSHIP_BASE, rocket_id="starship-ift6", rocket_name="Starship IFT-6", active=False, success_rate_pct=90,
        first_flight="2024-11-19",
        description="The sixth integrated flight test, demonstrating an in-space Raptor relight.",
    ),
    _rocket(
        _STARSHIP_BASE, rocket_id="starship-v2", rocket_name="Starship V2", active=True, success_rate_pct=None,
        first_flight="2025-01-16",
        description="An upgraded Starship with taller propellant tanks and redesigned forward flaps.",
    ),
    _rocket(
        _STARSHIP_BASE, rocket_id="starship-v3", rocket_name="Starship V3", active=True, success_rate_pct=None,
        first_flight="2026-01-01", height={"meters": 124, "feet": 407},
        description="The next-generation Starship upgrade aimed at full and rapid reusability for Mars missions.",
    ),
    _rocket(
        _STARSHIP_BASE, rocket_id="starship-hls", rocket_name="Starship HLS", active=True, success_rate_pct=None,
        first_flight=None, cost_per_launch=None,
        description="The Human Landing System variant of Starship developed for NASA's Artemis Moon missions.",
    ),
    _rocket(
        _STARSHIP_BASE, rocket_id="starship-cargo", rocket_name="Starship Cargo", active=True, success_rate_pct=None,
        first_flight=None,
        description="A cargo-optimized Starship variant designed to deploy next-generation Starlink satellites.",
    ),
    _rocket(
        _STARSHIP_BASE, rocket_id="starship-tanker", rocket_name="Starship Tanker", active=True, success_rate_pct=None,
        first_flight=None,
        description="A propellant-tanker Starship variant used to refuel other Starships in orbit.",
    ),
    _rocket(
        _STARSHIP_BASE, rocket_id="starship-p2p", rocket_name="Starship Point-to-Point", active=False, success_rate_pct=None,
        first_flight=None,
        description="A proposed passenger variant of Starship for ultra-fast point-to-point travel on Earth.",
    ),
    _rocket(
        _CONCEPT_BASE, rocket_id="falcon5", rocket_name="Falcon 5", active=False, success_rate_pct=None,
        first_flight=None,
        description="A proposed medium-lift rocket between Falcon 1 and Falcon 9 that was never built.",
    ),
    _rocket(
        _CONCEPT_BASE, rocket_id="falcon9-heavy-concept", rocket_name="Falcon 9 Heavy (early concept)", active=False,
        success_rate_pct=None, first_flight=None,
        description="The original 2011 concept for a triple-core heavy launch vehicle, later renamed Falcon Heavy.",
    ),
    _rocket(
        _CONCEPT_BASE, rocket_id="its", rocket_name="Interplanetary Transport System", active=False, success_rate_pct=None,
        first_flight=None,
        description="The 2016 concept vehicle for Mars colonization that Starship and Super Heavy evolved from.",
    ),
    _rocket(
        _CONCEPT_BASE, rocket_id="bfr", rocket_name="Big Falcon Rocket", active=False, success_rate_pct=None,
        first_flight=None,
        description="The 2017 successor concept to the ITS, later renamed Starship.",
    ),
]

MOCK_ROCKETS: list[dict] = [{"id": index, **rocket} for index, rocket in enumerate(_ROCKET_DEFS, start=1)]
