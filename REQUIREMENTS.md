# REQUIREMENTS.md - Moving Location Simulator Feature
**FakeLocation Android App**  
**Date:** 2026-02-17  
**Target SDK:** 34 (Android 14)  
**Tech Stack:** Kotlin, Jetpack Compose, Google Maps API, Play Services Location  

---

## 1. FEATURE OVERVIEW

**Feature Name:** Moving Location Simulator (Dynamic Route-Based Location Mocking)

**Purpose:** Enable users to simulate realistic movement along a predefined route at a specified speed, continuously mocking device location as if the user is traveling from point A to point B.

**Scope:** 
- Route setup & selection
- Real-time location simulation along route
- Foreground service for continuous updates
- UI for monitoring simulation progress
- Route history management

**Out of Scope:**
- Traffic pattern simulation
- ETA calculations
- Offline maps support

---

## 2. USER STORIES & ACCEPTANCE CRITERIA

### **User Story 1: Create & Setup Route**
**As a** user,  
**I want to** define a route by entering start/end destinations and average speed,  
**So that** I can simulate travel along that specific path.

**Acceptance Criteria:**
- [ ] Route Setup Screen displays two text input fields: "Start Location" and "End Location"
- [ ] User can tap fields to search for locations via Google Places Autocomplete
- [ ] Speed input field accepts numeric values (1-200 km/h with validation)
- [ ] "Calculate Route" button fetches route from Google Directions API
- [ ] Map preview shows calculated route with start/end markers
- [ ] Error handling: Display user-friendly error if route cannot be calculated
- [ ] Distance and estimated duration displayed below map preview
- [ ] Optional "Loop Route" toggle switch visible
- [ ] "Confirm & Start" button initiates simulation (with confirmation dialog)

---

### **User Story 2: Start Location Simulation**
**As a** user,  
**I want to** start the simulator and watch my location update in real-time along the route,  
**So that** I can see realistic movement happening at my specified speed.

**Acceptance Criteria:**
- [ ] "Start Simulation" confirmation dialog shows route summary (start, end, speed, duration)
- [ ] User must confirm before foreground service starts
- [ ] Foreground service launches with persistent notification (must show status)
- [ ] Location updates begin immediately after service starts
- [ ] Map view centers on current position, follows in real-time
- [ ] Progress bar or percentage indicator shows route completion
- [ ] Current speed displayed (should match user-set speed)
- [ ] Estimated time remaining calculated and updated every 1 second
- [ ] Location updates occur exactly every 1 second at calculated pace

---

### **User Story 3: Pause, Resume & Restart Simulation**
**As a** user,  
**I want to** pause, resume, or restart the simulation at any time,  
**So that** I have full control over the mock location movement.

**Acceptance Criteria:**
- [ ] Active simulation displays "Pause" button in UI
- [ ] Tapping "Pause" halts location updates (position frozen at pause point)
- [ ] Paused state shows "Resume" button instead of "Pause"
- [ ] Tapping "Resume" continues from paused position at original speed
- [ ] "Restart" button available (restarts from beginning of route)
- [ ] Restart confirmation dialog prevents accidental reset
- [ ] All buttons accessible from main simulation screen
- [ ] Foreground service continues running during pause (no location updates, but service active)

---

### **User Story 4: Stop Simulation & Reset Location**
**As a** user,  
**I want to** stop the simulation anytime and have my location reset to actual real location,  
**So that** the mock location doesn't persist after I'm done testing.

**Acceptance Criteria:**
- [ ] "Stop Simulation" button visible during active simulation
- [ ] Tapping "Stop" shows confirmation dialog: "Stop simulation and reset to real location?"
- [ ] Upon confirmation, foreground service stops
- [ ] Device location immediately reverts to actual real GPS position
- [ ] Persistent notification disappears
- [ ] UI returns to main screen or route selection screen
- [ ] No lingering mocked locations remain

---

### **User Story 5: View Real-Time Progress on Map**
**As a** user,  
**I want to** see my current position on the route in real-time with progress indication,  
**So that** I can visually confirm the simulation is working correctly.

**Acceptance Criteria:**
- [ ] Map displays entire route as a polyline
- [ ] Current position shown as animated marker on the route
- [ ] Marker updates smoothly every 1 second
- [ ] Progress bar shows % of route completed
- [ ] Route start point marked distinctly (e.g., green pin)
- [ ] Route end point marked distinctly (e.g., red pin)
- [ ] Current position marker is centered/tracked on map view
- [ ] Map remains interactive (pinch to zoom, drag to pan)
- [ ] Elevation profile or distance indicator optional but nice-to-have

---

### **User Story 6: Save & Reuse Previous Routes**
**As a** user,  
**I want to** access previously used routes for quick re-simulation,  
**So that** I don't need to re-enter destinations every time.

**Acceptance Criteria:**
- [ ] Route history stored locally (SQLite or Room database)
- [ ] Last 10 routes saved with start, end, speed, created timestamp
- [ ] Route history list displayed on main screen or accessible via menu
- [ ] Each route item shows: "Start → End" and creation date
- [ ] Tapping a saved route auto-populates Route Setup screen
- [ ] Option to delete individual routes from history
- [ ] "Clear All History" option with confirmation
- [ ] No limit errors if trying to save 11th route (oldest deleted)
- [ ] Route data persists across app restarts

---

### **User Story 7: Handle Errors & Fallback to Static Mock**
**As a** user,  
**I want to** get clear feedback if route calculation fails and have a fallback option,  
**So that** I can still test the app even if the API is unavailable.

**Acceptance Criteria:**
- [ ] If Google Directions API returns error, display user-friendly dialog
- [ ] Error message explains why (e.g., "No route found" or "Network error")
- [ ] "Retry" button allows re-attempting route calculation
- [ ] "Use Static Mock Instead?" button switches to static location mode
- [ ] If user confirms static fallback, Route Setup screen replaced with Static Location Setup
- [ ] No silent failures; all errors must be visible to user
- [ ] Network timeout error shows: "Check internet connection"
- [ ] Invalid destination error shows: "Could not find location. Try different name?"

---

## 3. DETAILED TECHNICAL SPECIFICATIONS

### **3.1 Architecture Overview**

```
┌─────────────────────────────────────────────────┐
│          UI Layer (Jetpack Compose)             │
│  - RouteSetupScreen                             │
│  - SimulationProgressScreen                     │
│  - RouteHistoryScreen                           │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│      ViewModel & State Management               │
│  - LocationSimulatorViewModel                   │
│  - RouteHistoryViewModel                        │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│         Service Layer (Business Logic)          │
│  - LocationSimulatorService (Foreground)        │
│  - RouteCalculationService                      │
│  - LocationMockingService                       │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│        Data/Repository Layer                    │
│  - RouteHistoryRepository                       │
│  - LocationRepository                           │
│  - GoogleMapsRepository                         │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▴──────────────────────────────────┐
│    External APIs & Databases                    │
│  - Google Directions API                        │
│  - Google Places API                            │
│  - Play Services Location API                   │
│  - Room Database (Local)                        │
└─────────────────────────────────────────────────┘
```

---

### **3.2 Data Models**

#### **Route Model**
```kotlin
data class Route(
    val id: Long = 0,
    val startLocation: String,           // Address or place name
    val endLocation: String,
    val startLat: Double,
    val startLng: Double,
    val endLat: Double,
    val endLng: Double,
    val speedKmh: Double,                // 1-200 km/h
    val distanceMeters: Double,          // From Directions API
    val durationSeconds: Long,           // Estimated total duration
    val polylinePoints: String,          // Encoded polyline from API
    val createdAt: Long = System.currentTimeMillis(),
    val loopRoute: Boolean = false
)
```

#### **LocationPoint Model**
```kotlin
data class LocationPoint(
    val latitude: Double,
    val longitude: Double,
    val timestamp: Long,
    val speedKmh: Double,
    val bearingDegrees: Float
)
```

#### **SimulationState Enum**
```kotlin
enum class SimulationState {
    IDLE,           // No simulation active
    RUNNING,        // Actively updating location
    PAUSED,         // Paused, can resume
    COMPLETED,      // Reached destination
    ERROR           // Error occurred
}
```

---

### **3.3 Service: LocationSimulatorService (Foreground Service)**

**Purpose:** Handle continuous location updates every 1 second along the route.

**Key Responsibilities:**
- Decode polyline into discrete lat/lng points
- Calculate interpolated position for each 1-second interval based on speed
- Request location permission (if needed)
- Update mocked location via `FusedLocationProviderClient.setMockLocation()`
- Emit location updates to ViewModel via Flow
- Post persistent notification

**Lifecycle:**
```
Intent Start → onCreate → onStartCommand 
  → startForeground(NOTIFICATION_ID, notification)
  → startLocationUpdates()
  [Every 1 second: calculate & set location]
  → [Pause/Resume/Stop]
  → stopForeground(true) → onDestroy
```

**Permissions Required:**
- `ACCESS_FINE_LOCATION`
- `ACCESS_COARSE_LOCATION`
- `FOREGROUND_SERVICE`
- `FOREGROUND_SERVICE_LOCATION`

---

### **3.4 Route Calculation Flow**

1. **User Input:** Start & end locations + speed
2. **Google Places Autocomplete:** Resolve addresses to lat/lng
3. **Google Directions API Call:**
   ```
   GET https://maps.googleapis.com/maps/api/directions/json?
     origin=lat,lng&
     destination=lat,lng&
     key=API_KEY
   ```
4. **Parse Response:**
   - Extract encoded polyline
   - Extract total distance (meters)
   - Calculate total duration (distance / speed)
5. **Decode Polyline:** Convert to lat/lng array
6. **Display Preview:** Show route on map
7. **Store Route:** Save to Room database for history

---

### **3.5 Location Interpolation Algorithm**

**Goal:** Given a route polyline and speed, calculate position at time T.

**Algorithm:**
```
1. Decode polyline into waypoints array
2. For each 1-second interval:
   a. Calculate distance traveled in 1 second:
      distance_per_second = speed_kmh / 3.6  // Convert km/h to m/s
   b. Calculate cumulative distance from start
   c. Find two waypoints that bracket current distance
   d. Interpolate linearly between them
   e. Calculate bearing (direction) from previous point
   f. Create LocationPoint(lat, lng, bearing, timestamp)
3. Emit LocationPoint to LocationSimulatorService
4. Service calls setMockLocation(location)
```

**Example:**
```
Speed: 36 km/h = 10 m/s
Route length: 1000m
Duration: 100 seconds

At t=5s: traveled 50m from start
At t=10s: traveled 100m from start
... etc
```

---

### **3.6 Foreground Service Notification**

**Notification Content:**
```
Title: "FakeLocation - Route Simulator Active"
Body: "Moving from [Start] to [End]"
SubText: "Speed: 36 km/h | Progress: 45% | Time remaining: 2:30"
Action Buttons: [Pause] [Stop]
Priority: HIGH
Ongoing: true (cannot dismiss)
```

**Notification Updates:**
- Update every 1 second with progress % and remaining time
- Change body on pause: "Paused at [Location]"
- Change action buttons to [Resume] on pause

---

### **3.7 Error Handling & Fallback**

| Error Scenario | Handling |
|---|---|
| Google API quota exceeded | Show: "API limit reached. Try again later." |
| Network unavailable | Show: "Check internet connection" |
| Invalid start/end address | Show: "Location not found. Try different name." |
| No route found | Show: "No route found between these locations." |
| Location permission denied | Show: "Grant location permission to continue" + fallback to static |
| Background location denied (Android 12+) | Show: "Approximate location only available" + continue with reduced precision |

**Fallback Behavior:**
- User taps "Use Static Mock Instead?" button
- Transition to static location setup screen
- Route history still saved (for future reference)

---

## 4. UI/UX FLOW

### **Flow Diagram:**

```
Main Screen
    ↓
[Start New Route] or [Select From History]
    ↓
Route Setup Screen
  ├─ Input: Start Location (Google Places search)
  ├─ Input: End Location (Google Places search)
  ├─ Input: Speed (km/h, 1-200)
  ├─ Toggle: Loop Route (optional)
  └─ Button: "Calculate Route"
    ↓
[Calculating...]
    ↓
Route Preview Screen
  ├─ Map with route polyline + markers
  ├─ Info: Distance, Duration, Speed
  └─ Button: "Confirm & Start Simulation"
    ↓
[Confirm Dialog] → "Start moving from [Start] to [End]?"
    ↓
[User Confirms]
    ↓
Simulation Active Screen
  ├─ Full-screen map with current position marker
  ├─ Progress bar (0-100%)
  ├─ Info: Current speed, time remaining, distance remaining
  ├─ Buttons: [Pause] [Restart] [Stop]
  └─ [Optional] List of waypoints showing next turn/street
    ↓
[Pause] → Pause Screen (buttons change to [Resume])
   or
[Resume] → Back to Simulation Active
   or
[Restart] → Confirmation → Reset to start
   or
[Stop] → Confirmation Dialog
    ↓
[User Confirms Stop]
    ↓
Location Reset to Real GPS
Foreground Service Stops
Return to Main Screen
```

---

### **Screen Wireframe Descriptions:**

#### **Screen 1: Route Setup**
```
┌──────────────────────────────┐
│     Route Setup              │
├──────────────────────────────┤
│                              │
│ Start Location:              │
│ [_____________________]      │
│ (Google Places search)       │
│                              │
│ End Location:                │
│ [_____________________]      │
│ (Google Places search)       │
│                              │
│ Speed (km/h):                │
│ [________] km/h              │
│ (Range: 1-200)               │
│                              │
│ ☐ Loop Route                 │
│                              │
│  [Calculate Route]           │
│                              │
└──────────────────────────────┘
```

#### **Screen 2: Route Preview**
```
┌──────────────────────────────┐
│  Route Preview               │
├──────────────────────────────┤
│                              │
│  ┌──────────────────────┐    │
│  │ [MAP WITH POLYLINE]  │    │
│  │ ● Start              │    │
│  │ ======== Route       │    │
│  │ ● End                │    │
│  └──────────────────────┘    │
│                              │
│ Distance: 12.5 km           │
│ Duration: 21 min            │
│ Speed: 36 km/h              │
│                              │
│ [Confirm & Start Simulation] │
│                              │
└──────────────────────────────┘
```

#### **Screen 3: Simulation Active**
```
┌──────────────────────────────┐
│  FakeLocation Simulator      │
├──────────────────────────────┤
│                              │
│  ┌──────────────────────┐    │
│  │ [MAP - LIVE]         │    │
│  │ ◆ Current Position   │    │
│  │                      │    │
│  └──────────────────────┘    │
│                              │
│ ████████░░░░░░░░░░ 45%       │
│                              │
│ Speed: 36 km/h               │
│ Distance Remaining: 6.88 km  │
│ Time Remaining: 11m 30s      │
│                              │
│ [Pause] [Restart] [Stop]     │
│                              │
└──────────────────────────────┘
```

#### **Screen 4: Route History**
```
┌──────────────────────────────┐
│  Recent Routes               │
├──────────────────────────────┤
│                              │
│ × New Route                  │
│                              │
│ > Home → Office              │
│   36 km/h | Feb 17, 22:45    │
│                              │
│ > Central Park → Museum      │
│   10 km/h | Feb 17, 20:30    │
│                              │
│ > City Center → Airport      │
│   60 km/h | Feb 16, 18:15    │
│                              │
│ [Clear History]              │
│                              │
└──────────────────────────────┘
```

---

## 5. TECHNICAL REQUIREMENTS

### **5.1 Dependencies**

**Gradle Dependencies:**
```kotlin
// Google Play Services
implementation("com.google.android.gms:play-services-location:21.0.1")
implementation("com.google.android.gms:play-services-maps:18.2.0")

// Google Maps SDK
implementation("com.google.maps.android:maps-ktx:4.0.1")
implementation("com.google.maps.android:android-maps-sdk:18.2.0")

// Kotlin Coroutines
implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.1")
implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.1")

// Jetpack Compose
implementation("androidx.compose.ui:ui:1.6.1")
implementation("androidx.compose.material3:material3:1.1.2")
implementation("androidx.compose.runtime:runtime:1.6.1")

// Room Database
implementation("androidx.room:room-runtime:2.6.1")
implementation("androidx.room:room-ktx:2.6.1")
kapt("androidx.room:room-compiler:2.6.1")

// Retrofit (HTTP)
implementation("com.squareup.retrofit2:retrofit:2.9.0")
implementation("com.squareup.retrofit2:converter-gson:2.9.0")

// Lifecycle
implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")

// Navigation
implementation("androidx.navigation:navigation-compose:2.7.6")
```

### **5.2 API Keys & Configuration**

**Required API Keys:**
- Google Directions API (server-side)
- Google Maps API (mobile SDK)
- Google Places API (mobile SDK)

**AndroidManifest.xml entries:**
```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_LOCATION" />
<uses-permission android:name="android.permission.INTERNET" />

<service
    android:name=".service.LocationSimulatorService"
    android:foregroundServiceType="location"
    android:exported="false" />
```

### **5.3 Android Compatibility**

| Requirement | Details |
|---|---|
| Min SDK | 26 (Android 8.0) |
| Target SDK | 34 (Android 14) |
| Foreground Service | Requires declaration in manifest |
| Location Mocking | Requires `ALLOW_MOCK_LOCATION` system permission (for testing) |
| Background Execution | Foreground service required for reliable updates |
| Battery Optimization | 1-second updates at wake lock requirement acceptable for test app |

---

## 6. ACCEPTANCE CRITERIA CHECKLIST

### **Feature Complete When:**

- [ ] Route Setup screen fully functional with Google Places autocomplete
- [ ] Google Directions API integration working (realistic road-based routes)
- [ ] Route preview displays on map with start/end markers
- [ ] Distance and duration calculated and displayed
- [ ] Speed validation enforces 1-200 km/h range
- [ ] Loop Route toggle visible and functional
- [ ] Confirmation dialog appears before simulation starts
- [ ] Foreground service launches successfully
- [ ] Location updates occur precisely every 1 second
- [ ] Location updates follow polyline path (not straight line)
- [ ] Current position marker appears on map
- [ ] Progress bar updates correctly (0-100%)
- [ ] Speed, distance remaining, and time remaining all display correctly
- [ ] Pause button halts location updates
- [ ] Resume button continues from pause point
- [ ] Restart button resets to beginning with confirmation
- [ ] Stop button resets device to real GPS location
- [ ] All buttons accessible and responsive
- [ ] Route history saves to local database (Room)
- [ ] Last 10 routes accessible from history list
- [ ] Routes persist across app restarts
- [ ] Delete individual route functionality works
- [ ] Clear all history with confirmation works
- [ ] Error dialog appears for failed route calculations
- [ ] Error messages are user-friendly and actionable
- [ ] "Use Static Mock Instead?" fallback option works
- [ ] Persistent notification shows during active simulation
- [ ] Notification updates every second with progress
- [ ] Notification contains Pause/Stop action buttons
- [ ] Persistent notification disappears when simulation stops
- [ ] No location updates leak after service stops
- [ ] All error cases handled gracefully (no crashes)
- [ ] Performance: No UI lag during location updates
- [ ] Performance: Service runs continuously without freezing
- [ ] Permissions properly requested and handled
- [ ] Background location access handled for Android 12+
- [ ] Code follows Kotlin best practices
- [ ] ViewModel state survives screen rotation
- [ ] No memory leaks in service/coroutines

---

## 7. DEPENDENCIES & INTEGRATION POINTS

### **External Dependencies:**
- **Google Directions API** - Route calculation
- **Google Places API** - Location autocomplete
- **Google Maps SDK** - Map display & rendering
- **Play Services Location** - Location mocking & updates
- **Room Database** - Local route history storage

### **Internal Integration:**
- Must integrate with existing static location mock feature
- When dynamic simulator active → disable static mock
- Must not interfere with other app features
- Should leverage existing location mocking infrastructure

### **Conflict Resolution:**
- Dynamic route simulator takes precedence over static mock
- If both somehow active, dynamic overrides and static is disabled
- Stopping dynamic simulator does NOT re-enable static mock (user must manually)

---

## 8. EDGE CASES & ERROR SCENARIOS

| Edge Case | Handling |
|---|---|
| User pauses, then kills app | Service stops, location resets to real on next app open |
| Route crosses international dateline | Use encoded polyline (handles naturally) |
| Very short route (< 100m) | Still works; duration will be very short |
| User sets extremely high speed (e.g., 200 km/h) | Validate & allow; show warning if > 150 km/h |
| Internet lost mid-simulation | Foreground service continues with cached route data |
| Location permission denied at runtime | Show graceful error, offer static mock fallback |
| Device runs out of storage for Route history | Delete oldest route automatically |
| GPS spoofing blocked by system | Show error: "Mock locations not supported on this device" |
| Polyline decoding fails | Catch exception, show error, offer fallback |
| Speed = 0 km/h entered | Reject input, show validation error |
| Same start & end location | Warn user but allow (0m route, instant completion) |
| Simulation interrupts system location request | Foreground service ensures location continues mocking |

---

## 9. MOCK DATA EXAMPLES

### **Example Route 1: Short City Drive**
```json
{
  "id": 1,
  "startLocation": "Central Park, New York",
  "endLocation": "Times Square, New York",
  "startLat": 40.7829,
  "startLng": -73.9654,
  "endLat": 40.7580,
  "endLng": -73.9855,
  "speedKmh": 20,
  "distanceMeters": 3200,
  "durationSeconds": 576,
  "polylinePoints": "encoded_polyline_string_here...",
  "createdAt": 1708188345000,
  "loopRoute": false
}
```

### **Example Route 2: Highway Route**
```json
{
  "id": 2,
  "startLocation": "New York, NY",
  "endLocation": "Boston, MA",
  "startLat": 40.7128,
  "startLng": -74.0060,
  "endLat": 42.3601,
  "endLng": -71.0589,
  "speedKmh": 100,
  "distanceMeters": 346000,
  "durationSeconds": 12456,
  "polylinePoints": "encoded_polyline_string_here...",
  "createdAt": 1708100000000,
  "loopRoute": false
}
```

### **Example Location Update (Emitted Every 1 Second)**
```json
{
  "latitude": 40.7850,
  "longitude": -73.9700,
  "timestamp": 1708188346000,
  "speedKmh": 20,
  "bearingDegrees": 215.5
}
```

---

## 10. TESTING STRATEGY

### **Unit Tests:**
- Polyline decoding algorithm
- Location interpolation math
- Speed validation (1-200 km/h)
- Route history CRUD operations
- Error handling & fallback logic

### **Integration Tests:**
- Google Directions API mocking
- Foreground service lifecycle
- Location update emission & capture
- Room database persistence

### **UI Tests:**
- Route Setup screen interactions
- Map rendering with polyline
- Progress bar updates
- Button state changes (pause/resume/stop)
- Route history list display

### **Functional Tests:**
- Complete flow: Setup → Preview → Simulate → Stop
- Pause/Resume/Restart functionality
- Real location reset after stop
- Notification display & updates
- Error dialog appearance & fallback

---

## 11. DELIVERABLES

**Coding Team will deliver:**
1. ✅ LocationSimulatorService (Foreground service)
2. ✅ RouteCalculationService (Google API integration)
3. ✅ LocationInterpolationEngine (Position calculation)
4. ✅ RouteSetupScreen (Compose UI)
5. ✅ SimulationProgressScreen (Live map + progress)
6. ✅ RouteHistoryScreen (Saved routes list)
7. ✅ RouteHistoryDatabase (Room schema & DAO)
8. ✅ LocationSimulatorViewModel (State management)
9. ✅ Integration with existing static mock system
10. ✅ Unit & integration tests (>80% coverage)
11. ✅ Error handling & graceful fallbacks
12. ✅ Notification implementation with actions

---

## 12. TIMELINE & MILESTONES

| Milestone | Deliverable | Estimated Duration |
|---|---|---|
| **Phase 1** | Core Service & Location Updates | 3-4 days |
| **Phase 2** | Route Calculation & UI | 3-4 days |
| **Phase 3** | Route History & State Management | 2-3 days |
| **Phase 4** | Testing & Bug Fixes | 2-3 days |
| **Phase 5** | Error Handling & Fallback | 1-2 days |
| **TOTAL** | Feature Complete & Tested | **11-16 days** |

---

## APPENDIX: Reference Links

- [Google Directions API Docs](https://developers.google.com/maps/documentation/directions)
- [Google Places API Docs](https://developers.google.com/maps/documentation/places)
- [Polyline Algorithm Format](https://developers.google.com/maps/documentation/utilities/polylinealgorithm)
- [Foreground Services (Android 12+)](https://developer.android.com/guide/components/foreground-services)
- [Location Mocking (Play Services)](https://developer.android.com/reference/com/google/android/gms/location/FusedLocationProviderClient)

---

**Status:** READY FOR DEVELOPMENT  
**Reviewed by:** PM Agent  
**Approved for:** Coding Team  
**Next Step:** Break into sprint tasks & assign to developers
