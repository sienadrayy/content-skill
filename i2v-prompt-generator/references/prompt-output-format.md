# I2V Prompt Output Format - STRICT

This is the EXACT format for outputting prompts to the user before ComfyUI submission.

## Rules (CRITICAL)
- NO extra tags (no `<Video 1>`, `<Image 1>`, etc.)
- NO section headers like `**IMAGE PROMPTS:**`
- NO blank lines between prompts
- Images first, all stacked together
- Videos second, all stacked together
- Simple separator line between image and video sections
- Each prompt is ONE continuous line

## EXACT EXAMPLE FORMAT

```
Close-up portrait of siena in warm bathroom shower light, wearing minimal bikini top, water drops cascading on skin, confident direct eye contact, bare shoulders and collarbone visible, sensual expression, golden warm bathroom lighting, professional beauty photography, 8.5/10 intensity
Extreme close-up face of siena, direct intense eye contact with subtle lip bite, warm shower lighting on skin, water streaming visible, minimal wet coverage evident, bare shoulders exposed, intimate vulnerable yet confident expression, professional sensual portraiture, 9/10 intensity, cinematic photography
Medium shot of siena in shower dynamic moment, hair flip motion captured mid-air with water spray, confident knowing smile, direct camera engagement, minimal coverage power pose, bare shoulders and upper back visible, golden warm shower lighting, energetic playful sensuality, professional glamorous photography, 8.5/10 intensity

---

Slow camera pan down from face to shoulders, 3-second duration revealing body, siena maintains confident eye contact throughout, water cascade visible throughout motion, warm golden bathroom lighting preserved, end on shoulder/neck reveal, cut to next segment
Slow body roll rotation from side profile to front over 4 seconds, water streams emphasize curves through movement, camera fixed, siena maintains sensual expression, golden rim lighting catches water and body lines, emphasize silhouette and curves, continuous fade to next segment
Hair flip over 2 seconds with water motion captured, then hold confident power pose with knowing smile and direct eye contact for remaining 2 seconds, soft golden lighting catches hair movement and body, dynamic sensual energy building, hard cut to next moment
```

## Structure

1. **Image prompts** (stacked, no newlines between)
   - Prompt 1
   - Prompt 2
   - Prompt 3

2. **Separator line:** `---`

3. **Video prompts** (stacked, no newlines between)
   - Prompt 1
   - Prompt 2
   - Prompt 3

## What NOT to do

❌ `**IMAGE PROMPTS:**` - No headers  
❌ `<Video 1>` - No tags  
❌ `Image 1:` - No numbering  
❌ Blank lines between prompts - Keep them stacked  
❌ Markdown formatting - Plain text only  

## Single Reel Example

```
Close-up portrait of siena in rain, confident eye contact, minimal coverage, golden hour lighting, professional photography
Slow pan down from face to shoulders, water drops visible, warm golden lighting preserved, siena maintains eye contact, cut to next
```

## Multi-Part Example (like shower 3 parts)

```
[Image Prompt 1 - all one line]
[Image Prompt 2 - all one line]
[Image Prompt 3 - all one line]

---

[Video Prompt 1 - all one line]
[Video Prompt 2 - all one line]
[Video Prompt 3 - all one line]
```
