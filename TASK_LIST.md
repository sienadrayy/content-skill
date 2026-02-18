# Moving Location Simulator - Task List

**Feature Overview:** Simulate location movement along Google Maps routes with real-time tracking, playback controls, and session management.

**Implementation Order:** Sequential - each task builds on previous foundations.

---

## T1: Directions API Service

**Feature Name:** Route Fetching & Polyline Extraction

**Description:**
Create a service to fetch route directions from Google Directions API. Retrieves optimal route, waypoints, distance, and polyline data. Called once per simulation session at start time, then cached for playback.

**Acceptance Criteria:**
- ✅ Single API call per session (no continuous polling)
- ✅ Returns route polyline (encoded), distance (meters), duration (seconds)
- ✅ Handles invalid routes with error response (origin = destination, no route found)
- ✅ Validates origin/destination are valid coordinates
- ✅ Caches polyline and route metadata for session duration
- ✅ Tracks API credit cost (1 credit per call)
- ✅ Timeout: 10 seconds max
- ✅ Returns error object on failure (no exceptions thrown)

**Dependencies:**
- Google Directions API key configured
- API credit tracking system initialized

**Complexity:** Low

---

## T2: Polyline Interpolation Engine

**Feature Name:** Position Calculator (1Hz Update)

**Description:**
Decode polyline and interpolate position at 1-second intervals. Calculates intermediate lat/lng points between polyline vertices based on elapsed time and speed (km/h). Returns position, progress percentage, and remaining distance for each tick.

**Acceptance Criteria:**
- ✅ Decodes Google-encoded polyline format
- ✅ Calculates position every 1 second (1Hz) with given speed (km/h)
- ✅ Position moves smoothly between polyline vertices
- ✅ Progress % accurate to 0.1% precision
- ✅ Returns: `{lat, lng, progress%, remainingDistanceKm, elapsed_sec}`
- ✅ Handles speed variation (1-500 km/h valid range)
- ✅ Returns final destination when complete (progress = 100%)
- ✅ No external API calls (pure calculation)

**Dependencies:**
- T1: Directions API Service (polyline input)

**Complexity:** Medium

---

## T9: Error Handling & Toast Notifications

**Feature Name:** Error Display Layer

**Description:**
Centralized error handling and user feedback system. Toast notifications for API failures, validation errors, permission issues, and user actions. Non-blocking, auto-dismiss after 3 seconds.

**Acceptance Criteria:**
- ✅ Toast shows for: API errors, invalid input, permission denials, session conflicts
- ✅ Auto-dismiss after 3 seconds (or user swipe)
- ✅ Error types: "error" (red), "warning" (yellow), "success" (green), "info" (blue)
- ✅ Toast queue: max 3 simultaneous, queue overflow automatically
- ✅ Does not crash app on unhandled errors
- ✅ Logs error details to console for debugging
- ✅ User can dismiss manually with swipe/tap

**Dependencies:**
- None (foundational)

**Complexity:** Low

---

## T10: API Credit Tracking Display

**Feature Name:** Credit Counter & Display

**Description:**
Track and display API usage credits. Autocomplete search = 1 credit, Directions API call = 1 credit. Persist credit count in SharedPreferences. Display current balance in UI with credit history log.

**Acceptance Criteria:**
- ✅ Increment credit counter on each API call
- ✅ Persist credit count across app restarts
- ✅ Display current balance in top bar / settings
- ✅ Log each transaction: timestamp, type (autocomplete/directions), credit amount
- ✅ Show warning when credits < 10
- ✅ History shows last 20 transactions
- ✅ No API call to check credits (local calculation only)

**Dependencies:**
- None (foundational)

**Complexity:** Low

---

## T7: Playback Control Logic

**Feature Name:** State Machine (Pause/Resume/Restart)

**Description:**
Implement finite state machine for simulation states: IDLE → RUNNING → PAUSED → RUNNING or RESTARTED. Manages elapsed time, pause offsets, and state transitions. Prevents invalid transitions (e.g., pause when idle).

**Acceptance Criteria:**
- ✅ States: IDLE, RUNNING, PAUSED, STOPPED, COMPLETED
- ✅ Valid transitions enforced (no invalid state changes)
- ✅ Pause: freeze elapsed time counter
- ✅ Resume: continue from pause point
- ✅ Restart: reset elapsed time to 0, continue movement
- ✅ Stop: reset to real location, close route
- ✅ onStateChanged callback fires for UI updates
- ✅ Current state accessible via getter

**Dependencies:**
- None (foundational)

**Complexity:** Low

---

## T3: Foreground Service Extension

**Feature Name:** Background Location Simulation

**Description:**
Extend existing foreground service to include location simulation. Runs 1Hz location update loop on background thread. Integrates with T2 (Polyline Engine) and T7 (State Machine). Requests location permissions, ensures service stays alive during simulation.

**Acceptance Criteria:**
- ✅ Service keeps running during lock screen / background
- ✅ Location updates emit every 1 second (1Hz)
- ✅ Location updates pause when state = PAUSED
- ✅ Integrates with existing service infrastructure (no breaking changes)
- ✅ Requests/checks FINE_LOCATION & COARSE_LOCATION permissions
- ✅ Stops simulation on service destroy
- ✅ Battery optimization: uses LOCATION_UPDATE_INTERVAL = 1000ms
- ✅ Service notification shows: current speed, progress %, elapsed time

**Dependencies:**
- T2: Polyline Interpolation Engine
- T7: Playback Control Logic
- Existing foreground service implementation

**Complexity:** Medium

---

## T8: Single-Session Management

**Feature Name:** Session Lifecycle (Auto-Close Previous)

**Description:**
Enforce only 1 active simulation at a time. When user starts new route, automatically stop and close the previous session. Cleans up resources, resets location to real position, updates route history.

**Acceptance Criteria:**
- ✅ Only 1 active route can run simultaneously
- ✅ Starting new route closes previous (with user confirmation or auto-close)
- ✅ Previous route saved to history before closing
- ✅ Location resets to real GPS on session close
- ✅ All resources (timers, listeners) cleanup properly
- ✅ No resource leaks on session switch
- ✅ Session ID generated for tracking

**Dependencies:**
- T3: Foreground Service Extension
- T6: Route History Management
- T7: Playback Control Logic

**Complexity:** Medium

---

## T4: Route Configuration Screen

**Feature Name:** Destination Input & Speed Setup

**Description:**
UI screen for user to enter destination, select speed (1-500 km/h), and view route preview. Includes autocomplete for destination input. Validates inputs before route start. Shows estimated time/distance.

**Acceptance Criteria:**
- ✅ Destination input with Google Places autocomplete
- ✅ Speed slider: 1-500 km/h with validation
- ✅ Real-time preview: route distance, estimated duration
- ✅ "Start Simulation" button (disabled until valid inputs)
- ✅ Input validation: origin ≠ destination, speed in range
- ✅ Error toast on invalid input
- ✅ Shows loading spinner during Directions API call
- ✅ Autocomplete credit tracking (1 credit per search)

**Dependencies:**
- T1: Directions API Service
- T9: Error Handling
- T10: API Credit Tracking
- Google Places API configured

**Complexity:** Medium

---

## T5: Map View with Real-Time Tracking

**Feature Name:** Live Position Marker & Progress Display

**Description:**
Google Map display showing real-time position marker, route polyline, and progress percentage. Updates position every 1 second. Shows current speed, elapsed time, remaining distance as overlays. Auto-centers map on current position.

**Acceptance Criteria:**
- ✅ Polyline route drawn on map
- ✅ Position marker updates every 1 second
- ✅ Progress % displayed as overlay (0-100%)
- ✅ Current speed (km/h) shown in overlay
- ✅ Elapsed time shown in overlay
- ✅ Remaining distance shown in overlay
- ✅ Map auto-centers on current position (smooth pan)
- ✅ Origin and destination markers visible
- ✅ Shows zoomed route on map load

**Dependencies:**
- T2: Polyline Interpolation Engine
- T3: Foreground Service Extension
- Google Maps API configured

**Complexity:** Medium

---

## T6: Route History Management

**Feature Name:** Persistent Route History & Quick-Access

**Description:**
Store and retrieve last 10 completed routes with metadata (origin, destination, distance, duration, timestamp, speed). Persist to SQLite database. Display history in UI with quick-restart option. Auto-delete oldest route when 11th route completed.

**Acceptance Criteria:**
- ✅ Stores: origin, destination, distance_km, duration_sec, speed_kmh, timestamp, route_polyline
- ✅ Persists to SQLite database
- ✅ Shows last 10 routes in history screen
- ✅ Quick-restart: tap route → auto-populate T4 screen with same origin/destination/speed
- ✅ Auto-delete oldest route when 11th added
- ✅ Delete route manually (swipe or delete button)
- ✅ Clear all history (with confirmation)
- ✅ Routes sorted by timestamp (newest first)

**Dependencies:**
- T1: Directions API Service
- T8: Single-Session Management
- SQLite database setup

**Complexity:** Medium

---

## Implementation Sequence Summary

| Order | Task ID | Feature | Rationale |
|-------|---------|---------|-----------|
| 1 | T1 | Directions API Service | Foundation - all routes depend on this |
| 2 | T2 | Polyline Interpolation Engine | Core calculation engine - needed by service & UI |
| 3 | T9 | Error Handling | Foundational for all error paths |
| 4 | T10 | API Credit Tracking | Foundational for monitoring |
| 5 | T7 | Playback Control Logic | State machine for all playback operations |
| 6 | T3 | Foreground Service Extension | Integrates T2 + T7 for background simulation |
| 7 | T8 | Single-Session Management | Session lifecycle control |
| 8 | T4 | Route Configuration Screen | User input layer |
| 9 | T5 | Map View with Tracking | Real-time visualization |
| 10 | T6 | Route History Management | Data persistence & quick access |

---

**Total Complexity:** 2 Low + 2 Medium + 2 Low (foundations) + 3 Medium (core) + 1 Medium (persistence) = **Balanced implementation path**

**Estimated Sprint:** 3-4 weeks with staggered task assignments
