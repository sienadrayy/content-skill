---
name: mixpanel
description: Product analytics - funnels, retention cohorts, user segmentation, event tracking
metadata:
  openclaw:
    emoji: "📈"
---

# Mixpanel Skill

Advanced product analytics - understand how users engage with your product.

## Setup

1. **Create Mixpanel Project:** https://mixpanel.com
2. **Get Credentials:** Project ID + API Secret from Project Settings
3. **Set environment variables:**
   ```bash
   export MIXPANEL_PROJECT_ID="YOUR_PROJECT_ID"
   export MIXPANEL_API_SECRET="YOUR_API_SECRET"
   ```

## Key Analyses

### Funnel Analysis
Track user drop-off through critical flows:
- Sign-up funnel
- Purchase funnel
- Feature adoption funnel

### Retention Cohorts
Measure how many users return:
- Day 1 / Day 7 / Day 30 retention
- Cohort retention curves
- Feature impact on retention

### User Segmentation
Create segments to understand:
- High-value users vs. casual
- Feature users vs. non-users
- Churned vs. active

### Event Tracking
Monitor custom events:
- Feature clicks
- Form submissions
- API calls
- Errors

## Typical Metrics

| Metric | Formula | Purpose |
|--------|---------|---------|
| DAU | Distinct users/day | Activity level |
| MAU | Distinct users/month | Monthly engagement |
| Retention Rate | Users(t+n) / Users(t) | Long-term engagement |
| Churn Rate | Lost users / Starting users | Product health |
| LTV | Total revenue / Users | User value |

## Usage Examples

```bash
@Analyst What's our Day 7 retention rate?

@Analyst Create a cohort of users who clicked feature X - how do they differ in retention?

@Analyst Show me the sign-up funnel - where do we lose the most users?

@Analyst Segment users by revenue - what behaviors differentiate high-value from low-value?
```

## Best Practices

- Track every critical user action as an event
- Use properties (user_id, plan_type, etc.) to segment
- Set up funnels for revenue-critical flows
- Review cohort retention weekly
- Use segments to target marketing campaigns
