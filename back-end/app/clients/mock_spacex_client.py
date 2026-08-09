from __future__ import annotations

_MOCK_ROCKETS: list[dict] = [
    {
        "id": "falcon1",
        "name": "Falcon 1",
        "active": False,
        "stages": 2,
        "boosters": 0,
        "success_rate_pct": 40,
        "first_flight": "2006-03-24",
        "country": "Republic of the Marshall Islands",
        "description": "The Falcon 1 was an expendable launch system privately developed and manufactured by SpaceX.",
    },
    {
        "id": "falcon9",
        "name": "Falcon 9",
        "active": True,
        "stages": 2,
        "boosters": 0,
        "success_rate_pct": 98,
        "first_flight": "2010-06-04",
        "country": "United States",
        "description": "Falcon 9 is a two-stage rocket designed and manufactured by SpaceX for reliable and safe transport.",
    },
    {
        "id": "falconheavy",
        "name": "Falcon Heavy",
        "active": True,
        "stages": 2,
        "boosters": 2,
        "success_rate_pct": 100,
        "first_flight": "2018-02-06",
        "country": "United States",
        "description": "With the ability to lift into orbit over 54 metric tons, Falcon Heavy is the most capable rocket flying.",
    },
    {
        "id": "starship",
        "name": "Starship",
        "active": True,
        "stages": 2,
        "boosters": 0,
        "success_rate_pct": None,
        "first_flight": "2023-04-20",
        "country": "United States",
        "description": "Starship is a fully reusable transportation system for crew and cargo to Earth orbit, the Moon, and Mars.",
    },
]

_MOCK_LAUNCHES: list[dict] = [
    {"id": "l1", "name": "FalconSat", "rocket": "falcon1", "date_utc": "2006-03-24T22:30:00.000Z", "success": False, "upcoming": False},
    {"id": "l2", "name": "DemoSat", "rocket": "falcon1", "date_utc": "2007-03-21T01:10:00.000Z", "success": False, "upcoming": False},
    {"id": "l3", "name": "Ratsat", "rocket": "falcon1", "date_utc": "2008-09-28T23:15:00.000Z", "success": True, "upcoming": False},
    {"id": "l4", "name": "Falcon 9 Test Flight", "rocket": "falcon9", "date_utc": "2010-06-04T18:45:00.000Z", "success": True, "upcoming": False},
    {"id": "l5", "name": "COTS 2", "rocket": "falcon9", "date_utc": "2012-05-22T07:44:00.000Z", "success": True, "upcoming": False},
    {"id": "l6", "name": "CASSIOPE", "rocket": "falcon9", "date_utc": "2013-09-29T16:00:00.000Z", "success": True, "upcoming": False},
    {"id": "l7", "name": "CRS-7", "rocket": "falcon9", "date_utc": "2015-06-28T14:21:00.000Z", "success": False, "upcoming": False},
    {"id": "l8", "name": "Orbcomm-2", "rocket": "falcon9", "date_utc": "2015-12-22T01:29:00.000Z", "success": True, "upcoming": False},
    {"id": "l9", "name": "AMOS-6", "rocket": "falcon9", "date_utc": "2016-09-01T13:07:00.000Z", "success": False, "upcoming": False},
    {"id": "l10", "name": "Iridium NEXT 1", "rocket": "falcon9", "date_utc": "2017-01-14T17:54:00.000Z", "success": True, "upcoming": False},
    {"id": "l11", "name": "CRS-11", "rocket": "falcon9", "date_utc": "2017-06-03T21:07:00.000Z", "success": True, "upcoming": False},
    {"id": "l12", "name": "Falcon Heavy Test Flight", "rocket": "falconheavy", "date_utc": "2018-02-06T20:45:00.000Z", "success": True, "upcoming": False},
    {"id": "l13", "name": "Telstar 18V", "rocket": "falcon9", "date_utc": "2018-09-10T04:45:00.000Z", "success": True, "upcoming": False},
    {"id": "l14", "name": "Crew Dragon Demo-2", "rocket": "falcon9", "date_utc": "2020-05-30T19:22:00.000Z", "success": True, "upcoming": False},
    {"id": "l15", "name": "Starlink 8", "rocket": "falcon9", "date_utc": "2020-08-18T14:31:00.000Z", "success": True, "upcoming": False},
    {"id": "l16", "name": "Crew-7", "rocket": "falcon9", "date_utc": "2023-08-26T07:27:00.000Z", "success": True, "upcoming": False},
    {"id": "l17", "name": "Starship IFT-3", "rocket": "starship", "date_utc": "2024-03-14T13:25:00.000Z", "success": True, "upcoming": False},
    {"id": "l18", "name": "Starlink 6-50", "rocket": "falcon9", "date_utc": "2024-11-05T02:00:00.000Z", "success": None, "upcoming": True},
    {"id": "l19", "name": "Starship IFT-8", "rocket": "starship", "date_utc": "2026-09-01T00:00:00.000Z", "success": None, "upcoming": True},
]

_MOCK_STARLINK: list[dict] = [
    {"id": "s1", "version": "v1.0", "launch": "l15", "spaceTrack": {"OBJECT_NAME": "STARLINK-1130", "DECAYED": 0}},
    {"id": "s2", "version": "v1.0", "launch": "l15", "spaceTrack": {"OBJECT_NAME": "STARLINK-1131", "DECAYED": 0}},
    {"id": "s3", "version": "v1.0", "launch": "l15", "spaceTrack": {"OBJECT_NAME": "STARLINK-1132", "DECAYED": 0}},
    {"id": "s4", "version": "v0.9", "launch": "l9", "spaceTrack": {"OBJECT_NAME": "STARLINK-30", "DECAYED": 1}},
    {"id": "s5", "version": "v0.9", "launch": "l9", "spaceTrack": {"OBJECT_NAME": "STARLINK-31", "DECAYED": 1}},
    {"id": "s6", "version": "v1.5", "launch": "l16", "spaceTrack": {"OBJECT_NAME": "STARLINK-4001", "DECAYED": 0}},
    {"id": "s7", "version": "v1.5", "launch": "l16", "spaceTrack": {"OBJECT_NAME": "STARLINK-4002", "DECAYED": 0}},
    {"id": "s8", "version": "v1.5", "launch": "l16", "spaceTrack": {"OBJECT_NAME": "STARLINK-4003", "DECAYED": 0}},
    {"id": "s9", "version": "v2.0", "launch": "l18", "spaceTrack": {"OBJECT_NAME": "STARLINK-6050", "DECAYED": 0}},
    {"id": "s10", "version": "v0.9", "launch": "l9", "spaceTrack": {"OBJECT_NAME": "STARLINK-32", "DECAYED": 1}},
]


class MockSpaceXClient:
    async def get_rockets(self) -> list[dict]:
        return _MOCK_ROCKETS

    async def get_launches(self) -> list[dict]:
        return _MOCK_LAUNCHES

    async def get_starlink(self) -> list[dict]:
        return _MOCK_STARLINK

    async def aclose(self) -> None:
        return None
