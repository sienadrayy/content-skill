# T1: Directions API Service - Implementation Briefing for Codex

**Status:** Ready for Implementation  
**Date:** 2026-02-17 23:03 GMT+5:30  
**Coordinator:** Claude Code (Agent Main)

---

## Task Overview

Implement the Directions API Service layer for the Moving Location Simulator feature. This is a **foundational task** - all subsequent tasks depend on this API integration.

---

## Specifications

### What to Build

A service to fetch route directions from Google Directions API with these constraints:

- **Single Call per Session:** API called ONCE when user starts route, then polyline cached
- **No Continuous Polling:** Results reused for entire playback duration
- **Return Data:**
  - Encoded polyline (Google format)
  - Distance (in meters)
  - Duration (in seconds)
  - Route legs/waypoints (if multi-point)
  - Status (success/error)

### Input Parameters

```kotlin
// Expected function signature
fun fetchRoute(
    origin: LatLng,              // Starting location (lat, lng)
    destination: LatLng,         // Ending location (lat, lng)
    mode: String = "driving"     // DRIVING, WALKING, BICYCLING, TRANSIT
): DirectionsResult
```

### Output Model

```kotlin
data class DirectionsResult(
    val success: Boolean,
    val polyline: String,              // Encoded polyline
    val distanceMeters: Int,           // Total route distance
    val durationSeconds: Int,          // Total route duration
    val originLatLng: LatLng,
    val destinationLatLng: LatLng,
    val error: String? = null,         // Error message if failed
    val waypointsCount: Int = 0        // Number of intermediate stops (0 = direct route)
)
```

---

## Acceptance Criteria (Testable)

- ✅ **Single API Call:** Only 1 HTTP request per session (verify via logs)
- ✅ **Valid Routes:** Fetches polyline for real origin/destination pairs
- ✅ **Error Handling:** Returns error object (no exceptions) for:
  - Invalid coordinates
  - Origin = Destination
  - No route found
  - API quota exceeded
  - Network timeout
- ✅ **Timeout:** Completes within 10 seconds
- ✅ **Caching:** Polyline cached in memory during session
- ✅ **Credit Tracking:** Increments API credit counter by 1
- ✅ **API Response Parsing:** Extracts polyline, distance, duration accurately
- ✅ **Unit Correctness:** Distance in meters, duration in seconds

---

## Implementation Details

### Google Directions API Setup

**Endpoint:**
```
https://maps.googleapis.com/maps/api/directions/json
```

**Required Parameters:**
- `origin` - "latitude,longitude"
- `destination` - "latitude,longitude"
- `key` - Google API key

**Optional Parameters:**
- `mode` - "driving" (default for simulator)
- `alternatives` - false (only fastest route)
- `units` - "metric" (kilometers/meters)

**Response Fields to Extract:**
```json
{
  "routes": [
    {
      "legs": [
        {
          "distance": { "value": 1234 },      // meters
          "duration": { "value": 567 }        // seconds
        }
      ],
      "overview_polyline": {
        "points": "encoded_string..."
      }
    }
  ],
  "status": "OK"
}
```

### Error Scenarios

| Scenario | Return | HTTP Code |
|----------|--------|-----------|
| Valid route found | success=true + polyline | 200 |
| Origin = Destination | success=false, error="Origin cannot equal destination" | 200 |
| No route found | success=false, error="No route found between locations" | 200 |
| Invalid coordinates | success=false, error="Invalid origin/destination coordinates" | 400 |
| API key invalid | success=false, error="Invalid API key" | 403 |
| Over quota | success=false, error="API quota exceeded" | 429 |
| Network timeout | success=false, error="Request timeout (10s)" | Connection error |

### API Credit Tracking

Each Directions API call should:
```kotlin
// In service implementation
creditTracker.addCredit(creditType = "DIRECTIONS_API", amount = 1)
// This increments T10 (API Credit Tracking)
```

---

## Project Context

**Project Location:** `C:\Users\mohit\AndroidStudioProjects\FakeLocation`

**Architecture Pattern:** MVVM with Retrofit + Coroutines

**Dependencies Already Available:**
- Retrofit (HTTP client)
- Gson (JSON parsing)
- Google Play Services (Maps, Location)
- Coroutines (async operations)

**Where to Implement:**

```
src/main/java/com/example/fakelocation/
├── data/
│   └── remote/
│       └── DirectionsApiService.kt      ← CREATE THIS
├── models/
│   ├── DirectionsResult.kt              ← CREATE THIS
│   └── DirectionsApiResponse.kt         ← CREATE THIS (API response DTO)
├── repository/
│   └── RouteRepository.kt               ← CREATE THIS (wraps service)
└── utils/
    └── PolylineUtils.kt                 ← MAY ALREADY EXIST
```

---

## Implementation Checklist

- [ ] Create `DirectionsResult.kt` data class
- [ ] Create `DirectionsApiResponse.kt` DTO for Google API response
- [ ] Create `DirectionsApiService.kt` interface with Retrofit
- [ ] Create `DirectionsRepository.kt` with business logic
- [ ] Add Google Directions API key to `local.properties` or `BuildConfig`
- [ ] Implement error handling for all scenarios
- [ ] Integrate with credit tracking system (T10 dependency)
- [ ] Add logging for debugging API calls
- [ ] Write unit tests for polyline extraction
- [ ] Verify timeout handling (10 second max)
- [ ] Git commit: "feat(T1): Implement Directions API Service"

---

## Testing Approach

### Manual Tests
1. **Valid Route:** Start Mumbai → Delhi, verify polyline returned
2. **Same Origin/Destination:** Try "current location" twice, verify error
3. **Network Timeout:** Disable internet, start route, verify timeout error
4. **Quota Exceeded:** (Simulate) Verify error toast displays
5. **Multiple Sessions:** Start route 1, verify API called once; start route 2, verify new API call

### Debug Logging
Add these logs to verify behavior:
```kotlin
Log.d("DirectionsAPI", "Fetching route: $origin → $destination")
Log.d("DirectionsAPI", "API Response: status=${response.status}, polyline=${result.polyline}")
Log.d("DirectionsAPI", "Route distance: ${result.distanceMeters}m, duration: ${result.durationSeconds}s")
```

---

## Dependencies

**For T1 (None blocking):**
- Google Directions API key
- Network permissions in AndroidManifest.xml

**T1 blocks:**
- T2 (Polyline Interpolation Engine) - needs polyline from T1
- T4 (Route Configuration Screen) - calls T1 on "Start Simulation"
- T5 (Map View) - displays polyline from T1

---

## Notes

- **No caching layers:** Just fetch and return (T8 will manage session lifecycle)
- **No database calls:** This is a pure HTTP service layer
- **Keep it simple:** Single responsibility - fetch route data only
- **Async:** Use Coroutines/suspend functions for non-blocking calls
- **Errors are data:** Always return DirectionsResult, never throw exceptions

---

## Success Criteria

✅ **Build passes:** `./gradlew build` succeeds  
✅ **No lint errors:** Android Lint check passes  
✅ **Git committed:** Changes pushed with clear commit message  
✅ **Tested:** Manual tests above pass  
✅ **Ready for T2:** Polyline extraction verified and working  

---

**Start Implementation Now** - Report back when:
1. Code complete and compiling
2. Manual tests passed
3. Changes committed to git
4. Ready for T2 (Polyline Interpolation Engine)

---

**Coordinator:** Claude Code (Agent Main)  
**Next Task After T1:** T9 (Error Handling) - can run in parallel
