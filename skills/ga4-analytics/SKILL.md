---
name: ga4-analytics
description: Query Google Analytics 4 for traffic, conversions, user behavior, and performance metrics
metadata:
  openclaw:
    emoji: "📊"
    requires:
      env: ["GA4_PROPERTY_ID"]
---

# GA4 Analytics Skill

Retrieve and analyze Google Analytics 4 data for your products.

## Setup

1. **Get Property ID:** Go to Google Analytics 4 → Admin → Property → Property ID
2. **Set environment variable:**
   ```bash
   export GA4_PROPERTY_ID="YOUR_PROPERTY_ID"
   ```

## Available Metrics

| Metric | API | Purpose |
|--------|-----|---------|
| Users (DAU/WAU/MAU) | `ga:activeUsers` | Daily/weekly/monthly active users |
| Sessions | `ga:sessions` | Number of sessions |
| Pageviews | `ga:pageviews` | Total page views |
| Engagement Rate | `ga:engagementRate` | % of engaged sessions |
| Bounce Rate | `ga:bounceRate` | % of bounced sessions |
| Conversion Rate | `ga:conversionRate` | % converted |
| Revenue | `ga:totalRevenue` | Total revenue |
| Events | `ga:eventCount` | Custom event counts |

## Common Queries

### Daily Active Users
```
Time period: last 7 days
Metric: activeUsers
Dimension: date
```

### Conversion Funnel
```
Metrics: users, eventCount
Events: page_view → sign_up → payment → purchase
Dimension: eventName
```

### Traffic Source Performance
```
Metric: activeUsers, conversionRate
Dimension: sessionDefaultChannelGroup
```

### Device Performance
```
Metric: engagementRate, sessionDuration
Dimension: deviceCategory
```

## Usage in OpenClaw

```bash
# Pull last 7 days of DAU
@Analyst Pull DAU (daily active users) for the last 7 days from GA4

# Get conversion by source
@Analyst What's our conversion rate by traffic source?

# Retention analysis
@Analyst Calculate week-over-week retention for last month
```

## Tips

- Use date comparisons to spot trends
- Segment by traffic source to optimize channels
- Track custom events to measure feature adoption
- Set up conversion goals to measure business metrics
