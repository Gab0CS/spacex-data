from __future__ import annotations

from datetime import datetime

_DEFAULT_ORBIT_PARAMS: dict = {
    "reference_system": "geocentric",
    "regime": "low-earth",
    "longitude": None,
    "semi_major_axis_km": None,
    "eccentricity": None,
    "periapsis_km": None,
    "apoapsis_km": None,
    "inclination_deg": None,
    "period_min": None,
    "lifespan_years": None,
    "epoch": None,
    "mean_motion": None,
    "raan": None,
    "arg_of_pericenter": None,
    "mean_anomaly": None,
}

_DEFAULT_FAIRINGS: dict = {"reused": False, "recovery_attempt": False, "recovered": False, "ship": None}
_DEFAULT_TELEMETRY: dict = {"flight_club": None}

_CCAFS = {"site_id": "ccafs_slc_40", "site_name": "CCAFS SLC 40", "site_name_long": "Cape Canaveral Air Force Station Space Launch Complex 40"}
_VAFB = {"site_id": "vafb_slc_4e", "site_name": "VAFB SLC 4E", "site_name_long": "Vandenberg Air Force Base Space Launch Complex 4E"}
_KWAJALEIN = {"site_id": "kwajalein_atoll", "site_name": "Kwajalein Atoll", "site_name_long": "Kwajalein Atoll Omelek Island"}
_KSC = {"site_id": "ksc_lc_39a", "site_name": "KSC LC 39A", "site_name_long": "Kennedy Space Center Historic Launch Complex 39A"}
_STARBASE = {"site_id": "starbase", "site_name": "Starbase", "site_name_long": "SpaceX Starbase, Boca Chica, Texas"}


def _payload(
    payload_id: str,
    customers: list[str],
    *,
    nationality: str | None = None,
    manufacturer: str | None = None,
    payload_type: str = "Satellite",
    mass_kg: float | None = None,
    mass_lbs: float | None = None,
    orbit: str | None = "LEO",
    regime: str = "low-earth",
    norad_id: list[int] | None = None,
) -> dict:
    return {
        "payload_id": payload_id,
        "norad_id": norad_id or [],
        "reused": False,
        "customers": customers,
        "nationality": nationality,
        "manufacturer": manufacturer,
        "payload_type": payload_type,
        "payload_mass_kg": mass_kg,
        "payload_mass_lbs": mass_lbs,
        "orbit": orbit,
        "orbit_params": {**_DEFAULT_ORBIT_PARAMS, "regime": regime},
    }


def _core(
    serial: str,
    *,
    block: int | None = None,
    reused: bool = False,
    legs: bool = False,
    gridfins: bool = False,
    land_success: bool | None = None,
    landing_intent: bool = False,
    landing_type: str | None = None,
) -> dict:
    return {
        "core_serial": serial,
        "flight": 1,
        "block": block,
        "gridfins": gridfins,
        "legs": legs,
        "reused": reused,
        "land_success": land_success,
        "landing_intent": landing_intent,
        "landing_type": landing_type,
        "landing_vehicle": None,
    }


def _links(
    *,
    patch: str | None = None,
    wikipedia: str | None = None,
    video: str | None = None,
    youtube_id: str | None = None,
    article: str | None = None,
) -> dict:
    return {
        "mission_patch": patch,
        "mission_patch_small": patch,
        "reddit_campaign": None,
        "reddit_launch": None,
        "reddit_recovery": None,
        "reddit_media": None,
        "presskit": None,
        "article_link": article,
        "wikipedia": wikipedia,
        "video_link": video,
        "youtube_id": youtube_id,
        "flickr_images": [],
    }


def _rocket(
    rocket_id: str,
    rocket_name: str,
    rocket_type: str,
    cores: list[dict],
    payloads: list[dict],
) -> dict:
    return {
        "rocket_id": rocket_id,
        "rocket_name": rocket_name,
        "rocket_type": rocket_type,
        "first_stage": {"cores": cores},
        "second_stage": {"block": 1, "payloads": payloads},
        "fairings": _DEFAULT_FAIRINGS,
    }


def _launch(
    flight_number: int,
    mission_name: str,
    rocket: dict,
    date_utc: str,
    *,
    success: bool | None,
    site: dict = _CCAFS,
    upcoming: bool = False,
    details: str | None = None,
    links: dict | None = None,
    failure: dict | None = None,
    mission_id: list[str] | None = None,
    ships: list[str] | None = None,
    static_fire_date_utc: str | None = None,
    tentative_max_precision: str = "hour",
    tbd: bool = False,
) -> dict:
    dt = datetime.fromisoformat(date_utc.replace("Z", "+00:00"))
    static_fire_unix = None
    if static_fire_date_utc:
        static_fire_unix = int(datetime.fromisoformat(static_fire_date_utc.replace("Z", "+00:00")).timestamp())
    return {
        "id": f"flight-{flight_number}",
        "flight_number": flight_number,
        "mission_name": mission_name,
        "mission_id": mission_id or [],
        "upcoming": upcoming,
        "launch_year": str(dt.year),
        "launch_date_unix": int(dt.timestamp()),
        "launch_date_utc": date_utc,
        "launch_date_local": date_utc,
        "is_tentative": upcoming,
        "tentative_max_precision": tentative_max_precision,
        "tbd": tbd,
        "launch_window": 0,
        "rocket": rocket,
        "ships": ships or [],
        "telemetry": _DEFAULT_TELEMETRY,
        "launch_site": site,
        "launch_success": success,
        "launch_failure_details": failure,
        "links": links or _links(),
        "details": details,
        "static_fire_date_utc": static_fire_date_utc,
        "static_fire_date_unix": static_fire_unix,
        "timeline": {},
    }


MOCK_LAUNCHES: list[dict] = [
    _launch(
        1, "FalconSat",
        _rocket("falcon1", "Falcon 1", "Merlin A", [_core("Merlin1A")], [
            _payload("FalconSAT-2", ["DARPA"], nationality="United States", manufacturer="SSTL", mass_kg=20, mass_lbs=43),
        ]),
        "2006-03-24T22:30:00.000Z", success=False, site=_KWAJALEIN,
        details="Engine failure at 33 seconds and loss of vehicle",
        failure={"time": 33, "altitude": None, "reason": "merlin engine failure"},
        links=_links(wikipedia="https://en.wikipedia.org/wiki/DemoSat", video="https://www.youtube.com/watch?v=0a_00nJ_Y88", youtube_id="0a_00nJ_Y88"),
        static_fire_date_utc="2006-03-17T00:00:00.000Z",
    ),
    _launch(
        2, "DemoSat",
        _rocket("falcon1", "Falcon 1", "Merlin A", [_core("Merlin2A")], [
            _payload("DemoSAT", ["DARPA"], nationality="United States", manufacturer="SpaceX"),
        ]),
        "2007-03-21T01:10:00.000Z", success=False, site=_KWAJALEIN,
        details="Successful first stage burn and transition to second stage, premature engine shutdown at T+7 min 30s, failed to reach orbit",
        failure={"time": 301, "altitude": 289, "reason": "harmonic oscillation leading to premature engine shutdown"},
        links=_links(wikipedia="https://en.wikipedia.org/wiki/DemoSat", video="https://www.youtube.com/watch?v=Lk4zQ2wP-Nc", youtube_id="Lk4zQ2wP-Nc"),
    ),
    _launch(
        3, "Ratsat",
        _rocket("falcon1", "Falcon 1", "Merlin C", [_core("Merlin4A")], [
            _payload("RatSat", ["SpaceX"], nationality="United States", manufacturer="SpaceX", mass_kg=165, mass_lbs=363, norad_id=[33393]),
        ]),
        "2008-09-28T23:15:00.000Z", success=True, site=_KWAJALEIN,
        details="Ratsat was carried to orbit on the first successful orbital launch of any privately funded and developed, liquid-propelled carrier rocket, the SpaceX Falcon 1",
        links=_links(wikipedia="https://en.wikipedia.org/wiki/Ratsat", video="https://www.youtube.com/watch?v=dLQ2tZEH6G0", youtube_id="dLQ2tZEH6G0"),
        static_fire_date_utc="2008-09-20T00:00:00.000Z",
    ),
    _launch(
        4, "Falcon 9 Test Flight",
        _rocket("falcon9", "Falcon 9", "v1.0", [_core("B0003", block=1)], [
            _payload("Dragon Qualification Unit", ["SpaceX"], nationality="United States", manufacturer="SpaceX",
                      payload_type="Dragon Boilerplate", norad_id=[36595]),
        ]),
        "2010-06-04T18:45:00.000Z", success=True,
        links=_links(wikipedia="https://en.wikipedia.org/wiki/Dragon_Spacecraft_Qualification_Unit", video="https://www.youtube.com/watch?v=nxSxgBKlYws", youtube_id="nxSxgBKlYws"),
        static_fire_date_utc="2010-03-13T00:00:00.000Z",
    ),
    _launch(
        5, "COTS 2",
        _rocket("falcon9", "Falcon 9", "v1.0", [_core("B0005", block=1)], [
            _payload("COTS Demo Flight 2", ["NASA(COTS)"], nationality="United States", manufacturer="SpaceX",
                      payload_type="Dragon 1.0", mass_kg=525, mass_lbs=1157, norad_id=[38348]),
        ]),
        "2012-05-22T07:44:00.000Z", success=True, ships=["AMERICANCHAMPION"],
        details="Launch was scrubbed on first attempt, second launch attempt was successful",
        links=_links(wikipedia="https://en.wikipedia.org/wiki/Dragon_C2%2B", video="https://www.youtube.com/watch?v=tpQzDbAY7yI", youtube_id="tpQzDbAY7yI"),
        static_fire_date_utc="2012-04-30T00:00:00.000Z",
    ),
    _launch(
        6, "CASSIOPE",
        _rocket("falcon9", "Falcon 9", "v1.1", [_core("B1003", block=1, landing_intent=True, landing_type="Ocean", land_success=False)], [
            _payload("CASSIOPE", ["MDA"], nationality="Canada", manufacturer="MDA", mass_kg=500, mass_lbs=1100,
                      orbit="PO", regime="polar", norad_id=[39265]),
        ]),
        "2013-09-29T16:00:00.000Z", success=True, site=_VAFB, ships=["AMERICANSPIRIT"],
        details="Commercial mission and first Falcon 9 v1.1 flight; an ocean touchdown test of the discarded booster was attempted but the vehicle broke up on the water impact",
        links=_links(wikipedia="https://en.wikipedia.org/wiki/CASSIOPE", video="https://www.youtube.com/watch?v=uFefasS6bhc", youtube_id="uFefasS6bhc"),
        static_fire_date_utc="2013-09-19T00:00:00.000Z",
    ),
    _launch(
        7, "CRS-7",
        _rocket("falcon9", "Falcon 9", "v1.1", [_core("B1019", block=1)], [
            _payload("CRS-7", ["NASA (CRS)"], nationality="United States", manufacturer="SpaceX",
                      payload_type="Dragon 1.0", mass_kg=1952, mass_lbs=4304, orbit="ISS"),
        ]),
        "2015-06-28T14:21:00.000Z", success=False,
        details="CRS-7 was lost approximately two minutes into flight due to an overpressure event in the second stage liquid oxygen tank, caused by a faulty strut",
        failure={"time": 139, "altitude": None, "reason": "second stage helium tank strut failure"},
        links=_links(wikipedia="https://en.wikipedia.org/wiki/SpaceX_CRS-7"),
    ),
    _launch(
        8, "Orbcomm-2",
        _rocket("falcon9", "Falcon 9", "Full Thrust", [_core("B1019", block=1, legs=True, gridfins=True, landing_intent=True, landing_type="RTLS", land_success=True)], [
            _payload("Orbcomm-OG2 Mission 2", ["Orbcomm"], payload_type="Satellite", mass_kg=2034, mass_lbs=4485),
        ]),
        "2015-12-22T01:29:00.000Z", success=True,
        details="First successful landing of a Falcon 9 first stage, touching down at Landing Zone 1",
        links=_links(wikipedia="https://en.wikipedia.org/wiki/Orbcomm"),
    ),
    _launch(
        9, "AMOS-6",
        _rocket("falcon9", "Falcon 9", "Full Thrust", [_core("B1028", block=2)], [
            _payload("AMOS-6", ["Spacecom"], nationality="Israel", manufacturer="Israel Aerospace Industries",
                      mass_kg=5500, mass_lbs=12125, orbit="GTO", regime="geostationary"),
        ]),
        "2016-09-01T13:07:00.000Z", success=False,
        details="AMOS-6 and the Falcon 9 were destroyed in a launch pad explosion during a pre-launch static fire test",
        failure={"time": 0, "altitude": 0, "reason": "COPV helium tank failure during propellant loading for a static fire test"},
        links=_links(wikipedia="https://en.wikipedia.org/wiki/Spacecom_AMOS-6"),
    ),
    _launch(
        10, "Iridium NEXT 1",
        _rocket("falcon9", "Falcon 9", "Full Thrust", [_core("B1029", block=2, legs=True, gridfins=True, landing_intent=True, landing_type="ASDS", land_success=True)], [
            _payload("Iridium NEXT Constellation 1", ["Iridium Communications"], mass_kg=9600, mass_lbs=21200,
                      orbit="LEO", regime="polar"),
        ]),
        "2017-01-14T17:54:00.000Z", success=True, site=_VAFB,
        details="First SpaceX launch from Vandenberg since the AMOS-6 anomaly, deploying the first ten Iridium NEXT satellites",
        links=_links(wikipedia="https://en.wikipedia.org/wiki/Iridium_NEXT"),
    ),
    _launch(
        11, "CRS-11",
        _rocket("falcon9", "Falcon 9", "Block 3", [_core("B1035", block=3, reused=True, legs=True, gridfins=True, landing_intent=True, landing_type="ASDS", land_success=True)], [
            _payload("CRS-11", ["NASA (CRS)"], nationality="United States", manufacturer="SpaceX",
                      payload_type="Dragon 1.0", mass_kg=2708, mass_lbs=5970, orbit="ISS"),
        ]),
        "2017-06-03T21:07:00.000Z", success=True, site=_KSC,
        details="First reuse of a Dragon spacecraft on a cargo resupply mission",
        links=_links(wikipedia="https://en.wikipedia.org/wiki/SpaceX_CRS-11"),
    ),
    _launch(
        12, "Falcon Heavy Test Flight",
        _rocket("falconheavy", "Falcon Heavy", "Demo", [
            _core("B1033", block=5, landing_intent=True, landing_type="ASDS", land_success=False),
            _core("B1023", block=5, reused=True, legs=True, gridfins=True, landing_intent=True, landing_type="RTLS", land_success=True),
            _core("B1025", block=5, reused=True, legs=True, gridfins=True, landing_intent=True, landing_type="RTLS", land_success=True),
        ], [
            _payload("Elon Musk's Tesla Roadster", ["SpaceX"], payload_type="Roadster", mass_kg=1350, mass_lbs=2976,
                      orbit="Heliocentric", regime="heliocentric"),
        ]),
        "2018-02-06T20:45:00.000Z", success=True, site=_KSC,
        details="Maiden flight of Falcon Heavy; payload was Elon Musk's Tesla Roadster with 'Starman'. Side boosters landed simultaneously at LZ-1 and LZ-2; the center core missed the droneship",
        links=_links(wikipedia="https://en.wikipedia.org/wiki/Falcon_Heavy_test_flight"),
    ),
    _launch(
        13, "Telstar 18V",
        _rocket("falcon9", "Falcon 9", "Block 5", [_core("B1049", block=5, legs=True, gridfins=True, landing_intent=True, landing_type="ASDS", land_success=True)], [
            _payload("Telstar 18V", ["Telesat"], nationality="Canada", manufacturer="SSL",
                      mass_kg=7060, mass_lbs=15564, orbit="GTO", regime="geostationary"),
        ]),
        "2018-09-10T04:45:00.000Z", success=True,
        links=_links(wikipedia="https://en.wikipedia.org/wiki/Telstar_18V"),
    ),
    _launch(
        14, "Crew Dragon Demo-2",
        _rocket("falcon9-crew", "Falcon 9 Block 5 (Crew)", "Block 5", [_core("B1058", block=5, legs=True, gridfins=True, landing_intent=True, landing_type="ASDS", land_success=True)], [
            _payload("Crew Dragon Demo-2 (Endeavour)", ["NASA (CCP)"], nationality="United States", manufacturer="SpaceX",
                      payload_type="Dragon 2.0", mass_kg=12055, mass_lbs=26580, orbit="ISS"),
        ]),
        "2020-05-30T19:22:00.000Z", success=True, site=_KSC,
        details="First crewed orbital spaceflight launched by a private company, carrying NASA astronauts Bob Behnken and Doug Hurley to the ISS",
        links=_links(wikipedia="https://en.wikipedia.org/wiki/Crew_Dragon_Demo-2"),
    ),
    _launch(
        15, "Starlink 8",
        _rocket("falcon9-cargo", "Falcon 9 Block 5 (Cargo)", "Block 5", [_core("B1049", block=5, reused=True, legs=True, gridfins=True, landing_intent=True, landing_type="ASDS", land_success=True)], [
            _payload("Starlink 8 v1.0", ["SpaceX"], payload_type="Satellite", mass_kg=15600, mass_lbs=34392),
        ]),
        "2020-08-18T14:31:00.000Z", success=True, site=_KSC,
        links=_links(wikipedia="https://en.wikipedia.org/wiki/Starlink"),
    ),
    _launch(
        16, "Crew-7",
        _rocket("falcon9-crew", "Falcon 9 Block 5 (Crew)", "Block 5", [_core("B1060", block=5, reused=True, legs=True, gridfins=True, landing_intent=True, landing_type="ASDS", land_success=True)], [
            _payload("Crew Dragon Endurance (Crew-7)", ["NASA (CCP)"], nationality="United States", manufacturer="SpaceX",
                      payload_type="Dragon 2.0", mass_kg=12500, mass_lbs=27558, orbit="ISS"),
        ]),
        "2023-08-26T07:27:00.000Z", success=True, site=_KSC,
        links=_links(wikipedia="https://en.wikipedia.org/wiki/SpaceX_Crew-7"),
    ),
    _launch(
        17, "Starship IFT-3",
        _rocket("starship", "Starship", "Block 1", [_core("Booster 10", block=1)], [
            _payload("Starship Ship 28", ["SpaceX"], payload_type="Test Payload", orbit="Suborbital", regime="suborbital"),
        ]),
        "2024-03-14T13:25:00.000Z", success=True, site=_STARBASE,
        details="Third integrated flight test of Starship, reaching orbital velocity for the first time and testing payload door operation",
        links=_links(wikipedia="https://en.wikipedia.org/wiki/SpaceX_Starship_flight_test_3"),
    ),
    _launch(
        18, "Starlink 6-50",
        _rocket("falcon9-cargo", "Falcon 9 Block 5 (Cargo)", "Block 5", [_core("B1071", block=5, reused=True, legs=True, gridfins=True, landing_intent=True, landing_type="ASDS", land_success=None)], [
            _payload("Starlink 6-50 v2 Mini", ["SpaceX"], payload_type="Satellite", mass_kg=17400, mass_lbs=38360),
        ]),
        "2024-11-05T02:00:00.000Z", success=None, upcoming=True,
        links=_links(wikipedia="https://en.wikipedia.org/wiki/Starlink"),
    ),
    _launch(
        19, "Starship IFT-8",
        _rocket("starship-v2", "Starship V2", "Block 2", [_core("Booster 16", block=2)], [
            _payload("Starship HLS Uncrewed Demo", ["NASA (Artemis)"], payload_type="Test Payload",
                      orbit="Lunar Transfer", regime="cislunar"),
        ]),
        "2026-09-01T00:00:00.000Z", success=None, upcoming=True, site=_STARBASE,
        tentative_max_precision="month", tbd=True,
        links=_links(wikipedia="https://en.wikipedia.org/wiki/SpaceX_Starship"),
    ),
]
