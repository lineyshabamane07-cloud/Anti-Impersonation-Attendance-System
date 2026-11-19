# AIAS – Team Contract (frozen 4 Oct)

Goal: nobody waits for anybody. Every person builds against the SAME three frozen things:
1. `schema.sql` – table and column names
2. `services/*.py` – function names, arguments and return shapes (already stubbed, return fake data)
3. The JSON shapes below

`USE_MOCK=true` (default) → services return fake data. On integration day (Wed 7 Oct) Lineysha's real
code replaces the stubs, everyone sets `USE_MOCK=false`, and the pages just work.
`DEV_MODE=true` → open `/dev/login/faculty`, `/dev/login/student`, `/dev/login/admin` to be logged in as a
fake user (stored as `session["user"] = {"id", "name", "role"}`). No real login needed while building.

## Session user (set by Mrunal's real login, by /dev/login in dev)
`session["user"] = {"id": int, "name": str, "role": "student"|"faculty"|"admin"}`

## Service functions (Lineysha implements; everyone else just calls them)
| Function | Called by | Returns |
|---|---|---|
| `qr_service.create_session(class_id, lat, lng, radius_m=None, refresh_s=None, duration_min=10)` | Tanmai | `session_id` (int) |
| `qr_service.get_current_token(session_id)` | Tanmai | `{"token": str, "expires_in": int}` |
| `qr_service.end_session(session_id)` | Tanmai | `None` |
| `verify_service.mark_attendance(token, student_id, lat, lng, device_id)` | Reet | `{"status": "present"/"rejected"/"flagged", "reason": str, "distance_m": float}` |
| `report_service.list_marked(session_id)` | Tanmai | `[{"student_id","name","status","distance_m","marked_at"}]` |
| `report_service.session_summary(session_id)` | Tanmai | `{"session_id","subject","division","room","total_students","present","flagged","rejected"}` |
| `report_service.list_attempts(only_problems=True)` | Mrunal | `[{"created_at","student","outcome","reason","distance_m"}]` |
| `geo_service.haversine_m(lat1,lng1,lat2,lng2)` | Lineysha | metres (float) – already written |

**Note:** `get_current_token` returns `{"token": None, "expires_in": 0}` when the session has ended or does not exist. The faculty page must show "Session ended" in that case.

## Testing every screen with mock data (Reet)
With `USE_MOCK=true`, the mock result depends on how the token ENDS:
`...-expired`, `...-far`, `...-dup`, `...-device`, `...-flag` → that result; anything else → success.
Use the "paste token manually" box on the scan page to try each one.

## HTTP routes (owner in brackets)
- `POST /login`, `GET /logout` [Mrunal]
- `POST /faculty/session/start` → `{"session_id": int}` [Tanmai]
- `GET  /faculty/session/<id>/qr` → `{"token","expires_in"}` [Tanmai]
- `GET  /faculty/session/<id>/live` → `{"marked": [...], "summary": {...}}` [Tanmai]
- `POST /faculty/session/<id>/end` [Tanmai]
- `POST /student/mark` body `{"token","lat","lng","device_id"}` → same shape as `mark_attendance` [Reet]

## Rules
- Never change a name or shape above without telling everyone in the group chat.
- Need something extra from another module? Ask for it by message; meanwhile mock it locally.
