# NJ Transit Rail GTFS – Populated Fields Reference

This document lists every **populated** field in the static GTFS feed stored in `data/GTFS_data/` (downloaded by `src/njtran_backend/getGTFS.py`), with its definition from the GTFS spec and notes on how NJ Transit actually uses it.

Fields that exist as column headers but are empty in every row are listed under "Empty columns" for each file and can be ignored.

> Profiled from the feed covering **2026-06-11 → 2027-05-01**. Row counts and values will shift as new feeds are downloaded, but the structure should stay the same.

## Files at a glance

| File | Rows | Purpose |
|---|---|---|
| `agency.txt` | 2 | Transit agencies in the feed |
| `routes.txt` | 12 | Rail lines |
| `trips.txt` | 2,702 | Individual scheduled train runs |
| `stop_times.txt` | 26,388 | Arrival/departure time of each trip at each stop |
| `stops.txt` | 173 | Stations |
| `calendar_dates.txt` | 9,649 | Which dates each service runs |
| `shapes.txt` | 272,630 | Track geometry for drawing lines on a map |

**Not present in this feed:** `calendar.txt`, `feed_info.txt`, `transfers.txt`, `frequencies.txt`, fare files (`fare_attributes`, `fare_rules`, `fare_*`), `pathways.txt`, `levels.txt`, `translations.txt`.

### How the files link together

```
agency.agency_id ──< routes.agency_id
routes.route_id  ──< trips.route_id
calendar_dates.service_id >── trips.service_id
shapes.shape_id  ──< trips.shape_id
trips.trip_id    ──< stop_times.trip_id
stops.stop_id    ──< stop_times.stop_id
```

---

## `agency.txt`

| Field | Type | Definition | Notes / values in this feed |
|---|---|---|---|
| `agency_id` | ID | Uniquely identifies a transit agency. | `NJB` (bus), `NJT` (rail). Only `NJT` is used by routes. |
| `agency_name` | Text | Full name of the agency. | `NJ TRANSIT BUS`, `NJ TRANSIT RAIL` |
| `agency_url` | URL | Agency website. | `http://www.njtransit.com/` |
| `agency_timezone` | Timezone | Timezone the agency is in. All times in the feed are local to this timezone. | `America/New_York` |
| `agency_lang` | Language code | Primary language used by the agency. | `en` |

**Empty columns:** `agency_phone`, `agency_fare_url`

---

## `routes.txt`

| Field | Type | Definition | Notes / values in this feed |
|---|---|---|---|
| `route_id` | ID | Uniquely identifies a route. | Numeric strings: `1, 2, 5, 6, 7, 8, 9, 10, 13, 14, 15, 17` |
| `agency_id` | ID (→ agency) | Agency that operates the route. | Always `NJT` |
| `route_short_name` | Text | Short, abstract identifier for the route. | e.g. `NEC`, `NJCL`, `MNE`, `RARV` |
| `route_long_name` | Text | Full name of the route. | e.g. `Northeast Corridor Line` |
| `route_type` | Enum | Type of transportation used on the route. | Always `113`. That's from the **extended** route types ("All Rail Services"), not the basic `2` (rail). |
| `route_color` | Hex color | Route color for display in apps and maps. | 10 distinct colors. Main/Bergen share `FFD411`; NEC/Princeton Shuttle share `DD3439`. |

**Empty columns:** `route_desc`, `route_url`, `route_text_color`

### Route list

| route_id | short | long name | color |
|---|---|---|---|
| 1 | ACRL | Atlantic City Rail Line | `#075AAA` |
| 2 | MNBTN | Montclair-Boonton Line | `#E66859` |
| 5 | BERG | Bergen County Line | `#FFD411` |
| 6 | MAIN | Main Line | `#FFD411` |
| 7 | MNE | Morris & Essex Line | `#08A652` |
| 8 | MNEG | Gladstone Branch | `#A4C9AA` |
| 9 | NEC | Northeast Corridor Line | `#DD3439` |
| 10 | NJCL | North Jersey Coast Line | `#03A3DF` |
| 13 | PASC | Pascack Valley Line | `#94219A` |
| 14 | PRIN | Princeton Shuttle | `#DD3439` |
| 15 | RARV | Raritan Valley Line | `#F2A537` |
| 17 | MRL | Meadowlands Rail Line | `#C1AA72` |

---

## `trips.txt`

| Field | Type | Definition | Notes / values in this feed |
|---|---|---|---|
| `trip_id` | ID | Uniquely identifies a trip (one run of a train along a route). | Numeric strings, e.g. `2134529` |
| `route_id` | ID (→ routes) | Route the trip belongs to. | All 12 routes are used. |
| `service_id` | ID (→ calendar_dates) | Set of dates on which the trip runs. | 78 distinct service IDs |
| `trip_headsign` | Text | Destination text shown to riders. | 39 distinct values, e.g. `Penn Station New York`, `Hoboken`, `Trenton Station` |
| `trip_short_name` | Text | Public-facing trip identifier. | The **train number**, e.g. `0703` |
| `direction_id` | Enum (0/1) | Direction of travel. Used to separate trips in opposite directions on the same route. | `0` ≈ toward NY Penn / Hoboken / Secaucus, `1` = the opposite direction |
| `block_id` | ID | Groups sequential trips run by the same vehicle. | **Identical to `trip_short_name`** on every trip, so it can't be used to chain trips together. |
| `shape_id` | ID (→ shapes) | Geographic path the trip follows. | 36 distinct shapes are used. |

**Empty columns:** `wheelchair_accessible`

---

## `stop_times.txt`

| Field | Type | Definition | Notes / values in this feed |
|---|---|---|---|
| `trip_id` | ID (→ trips) | Trip this stop time belongs to. | Every trip has at least one stop time. |
| `arrival_time` | Time (HH:MM:SS) | Arrival time at the stop, in local time measured from "noon minus 12h" of the service day. | Accurate to the second (e.g. `18:06:30`). **Can go past 24:00** (max `25:36:00`) for trips that run after midnight. |
| `departure_time` | Time (HH:MM:SS) | Departure time from the stop. | Differs from `arrival_time` in about 86% of rows, so dwell times are real data. |
| `stop_id` | ID (→ stops) | Stop being served. | |
| `stop_sequence` | Non-negative int | Order of stops within a trip. Values must increase along the trip but **don't need to be consecutive**. | Not numbered 1, 2, 3… in any trip, so sort by it rather than using it as an index. |
| `pickup_type` | Enum | Whether riders can board here. `0` = regular, `1` = no pickup, `2` = phone agency, `3` = coordinate with driver. | Only `0` and `1`. The **last stop** of every trip is `1`. |
| `drop_off_type` | Enum | Whether riders can alight here. Same values as `pickup_type`. | Only `0` and `1`. The **first stop** of every trip is `1`. |
| `shape_dist_traveled` | Float | Distance traveled along the trip's shape from the first point up to this stop. Same units as `shapes.shape_dist_traveled`. | Appears to be **miles**. Missing in 85 rows (the single-stop trips described below). |

**Empty columns:** `stop_headsign`

**Data quirks:**
- 67 trips (NEC and Morris & Essex, evenings) have only **one** stop, with both pickup and drop-off disallowed. These are probably placeholder or non-revenue moves and should be filtered out for route finding.
- 667 trips have exactly 2 stops.
- Stops per trip: min 1, max 26, average about 9.8.

---

## `stops.txt`

| Field | Type | Definition | Notes / values in this feed |
|---|---|---|---|
| `stop_id` | ID | Uniquely identifies a stop or station. | Numeric strings |
| `stop_code` | Text | Short rider-facing code for the stop. | 2-letter station codes, e.g. `AM` (Aberdeen-Matawan), `NY`, `SE` |
| `stop_name` | Text | Name of the stop as riders know it. | e.g. `Aberdeen-Matawan`. No duplicate names. |
| `stop_desc` | Text | Description of the stop. | Used for an internal **line + station code** (e.g. `NCMATWN`, `RVANNAN`) instead of a real description. |
| `stop_lat` | Latitude | WGS84 latitude. | |
| `stop_lon` | Longitude | WGS84 longitude. | |
| `zone_id` | ID | Fare zone of the stop (meant to be used with fare rules). | Filled for 164/173 stops, with 31 distinct zones. **No fare files exist**, so zones can't be priced. |

**Empty columns:** `stop_url`, `location_type`, `parent_station`, `stop_timezone`, `wheelchair_boarding`

**Notes:**
- Every stop is a standalone station. There are no parent stations or platforms.
- 7 stops are never served by any trip: Washington, Baltimore, B.W.I. Airport, New Carrollton, Wilmington and North Philadelphia (Amtrak-connection stations), plus Manville-Finderne.

---

## `calendar_dates.txt`

| Field | Type | Definition | Notes / values in this feed |
|---|---|---|---|
| `service_id` | ID | Identifies a set of dates when service is available. | 78 distinct |
| `date` | Date (YYYYMMDD) | Date of the service exception. | 325 dates, from `20260611` to `20270501` |
| `exception_type` | Enum | `1` = service added for this date, `2` = service removed for this date. | Always `1` |

**How to use it:** There is no `calendar.txt`, so this file is the **only** source of service dates. Each row means "service X runs on date Y". To get the trips for a date:

1. Filter `calendar_dates` on `date == YYYYMMDD` and collect the `service_id`s.
2. Filter `trips` on those `service_id`s.

Typical volume is about 765–770 trips on weekdays and about 460–476 on weekends, with holiday variations.

---

## `shapes.txt`

| Field | Type | Definition | Notes / values in this feed |
|---|---|---|---|
| `shape_id` | ID | Identifies a shape (a path a vehicle follows). | 40 distinct (36 referenced by trips) |
| `shape_pt_lat` | Latitude | Latitude of a point on the shape. | |
| `shape_pt_lon` | Longitude | Longitude of a point on the shape. | |
| `shape_pt_sequence` | Non-negative int | Order in which points connect to form the shape. | |
| `shape_dist_traveled` | Float | Distance from the first shape point up to this point. | Appears to be **miles** (max about 152.8) |

---

## Summary: what this data can and can't support

**Supported**
- Timetables for any date in the feed window
- Point-to-point trip planning with second-level arrival, departure and dwell times
- Train number lookups (`trip_short_name`)
- Mapping lines with official colors and accurate track geometry
- Distance and progress along a trip

**Not supported (needs other sources)**
- Fares (only `zone_id` exists, with no fare tables)
- Transfer rules and minimum connection times (no `transfers.txt`)
- Accessibility (all wheelchair fields are empty)
- Real-time delays and cancellations (that's GTFS-Realtime, a separate feed)
