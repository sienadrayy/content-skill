---
name: i2v-prompt-generator
description: Convert sensual-reels scripts with narrative progression into consistent image-to-video prompts. Extracts 8-10 key narrative states from scripts, generates detailed image prompts that maintain scene consistency and outfit progression, and corresponding video motion prompts showing transitions between states. Output format optimized for i2v AI generation with LoRA model and scene/outfit consistency throughout.

**⚠️ CRITICAL:** Scripts must have clear narrative progression. Image prompts must specify SCENE STATE to ensure consistency. No random outfit changes. No scene jumps.
---

# i2v Prompt Generator - NARRATIVE PROGRESSION FOCUSED 🎬

Convert scripts with NARRATIVE PROGRESSION into consistent, scene-coherent image + video prompts.

## How It Works - NARRATIVE PROGRESSION FOCUSED

**Input:** sensual-reels timeline script (60 seconds) - WITH CLEAR NARRATIVE PROGRESSION

**Process:**
1. **Extract narrative states from script:**
   - Setup state [0-10s]: What's the starting scene, outfit, makeup state?
   - Progression states [10-30s]: What's changing visually? What states appear?
   - Climax state [30-50s]: What's the full achieved state?
   - Finale state [50-60s]: Final confirmation of complete state

2. **For each state: generate paired image + video**
   - 1 image showing that STATE clearly (makeup level, outfit piece, scene, etc.)
   - 1 video showing TRANSITION INTO or WITHIN that state
   - 6-second video segments (per current config)

3. **CRITICAL CONSISTENCY RULES:**
   - ✅ Same scene throughout (same bathroom, same lighting, etc.)
   - ✅ Same outfit progression (not random changes)
   - ✅ Same character appearance consistent
   - ✅ Lighting consistent throughout
   - ✅ Track what STATE we're in at each moment

4. **Image prompts must specify:**
   - Current scene/location (specific: "bathroom vanity with mirror" not just "bathroom")
   - Current outfit/makeup state (e.g., "fresh face, no makeup" OR "full makeup complete + in complete dress")
   - What just happened or is about to happen
   - Specific visual details showing the narrative state
   - **SAME LIGHTING THROUGHOUT**

5. **Video prompts must show:**
   - Transition or progression within current state
   - Actions showing the narrative progression (not just poses)
   - Scene consistency throughout motion
   - Breathing/natural movement reflecting the narrative moment

**Output:** 
```
Image Prompts (stacked, no headers, each specifies SCENE STATE)
[Image 1 with specific outfit/makeup state + scene]
[Image 2 showing progression to next state]
[Image 3 showing further progression]
...

---

Video Prompts (stacked, no headers, each shows TRANSITIONS between states)
[Video 1 motion showing transition/action relevant to narrative]
[Video 2 motion showing progression within or into next state]
...
```

## Quick Start

**Just paste your narrative script:**

```
I have this GRWM script:
[0-10s] SETUP: Bathroom vanity, fresh face (no makeup), wearing undershirt, reaching toward makeup drawer
[10-20s] PROGRESSION: Applying eyeshadow, makeup visible being applied, same bathroom
[20-35s] PROGRESSION: Full makeup complete, now putting on dress, same vanity lighting
[35-50s] CLIMAX: Complete makeup + complete dress visible, confident pose
[50-60s] FINALE: Final power moment, complete look, direct confidence
```

**You'll get:**
- 8 auto-selected narrative states
- Image prompt for each (specifying scene, outfit state, progression)
- Video prompt for each (showing transitions/actions)
- Complete consistency throughout

## Image Prompt Structure - SCENE STATE & NARRATIVE FOCUSED

Each image prompt EXPLICITLY STATES the NARRATIVE STATE to ensure consistency and progress.

**MANDATORY ELEMENTS:**

1. **Scene/Location:**
   - Specific location ("bathroom vanity with mirror" not just "bathroom")
   - Lighting setup ("warm golden bathroom vanity light" - specify exactly)
   - Background details consistent across entire sequence
   - **SAME SCENE throughout entire sequence**

2. **Current Narrative State (CRITICAL):**
   - GRWM: "fresh face with no makeup visible", OR "makeup applied to eyes only", OR "full makeup complete with glowing finish", OR "complete makeup + full dress visible"
   - Shower: "fully clothed before shower", OR "undressing, clothes partially off", OR "minimal coverage in water", OR "wet body, post-shower moment"
   - Lingerie: "wearing casual jeans and shirt", OR "first lingerie piece visible on body", OR "complete lingerie set visible", OR "lingerie + robe final look"
   - **BE SPECIFIC** - don't say "wearing minimal" say "wearing black bikini with straps down showing upper ribs"

3. **Subject Appearance:**
   - Siena (always include name)
   - Body position/pose (standing at vanity, sitting on bed, etc.)
   - Body angle (direct to camera, 45-degree side, profile, etc.)
   - Visible body parts (shoulders, collarbone, chest, legs - based on outfit state)

4. **Outfit/Styling State:**
   - Exactly what's visible at THIS STATE (undershirt, no makeup | eyeshadow applied, undershirt | full makeup, dress on | etc.)
   - Coverage level specific to state (not vague "minimal")
   - Colors, materials relevant to state
   - Progressive state number if multi-step ("Makeup State 1 of 3" or "Outfit State 2 of 4")

5. **Expression & Eyes:**
   - Eye contact (direct to camera, intense, or looking at task)
   - Expression reflecting narrative moment (anticipation, focus, confidence)
   - Breathing or subtle movement visible if relevant

6. **Lighting Details (CRITICAL FOR CONSISTENCY):**
   - EXACT COLOR TEMP (2700K warm golden, 5600K daylight, etc.)
   - **MUST BE CONSISTENT throughout entire sequence**
   - Direction (front-lit, side-lit, etc.)
   - Quality (soft, dramatic, etc.)

7. **Action/Context:**
   - What's actively happening (applying makeup with visible brush, dress being adjusted, etc.)
   - Hands if relevant (reaching toward makeup, holding dress, etc.)
   - Show the PROGRESSION - not static poses

8. **Professional Quality:**
   - Photography quality appropriate to moment (beauty, body, glamour, etc.)
   - Cinematic or professional emphasis

**CRITICAL CONSISTENCY RULES:**
- ✅ SAME SCENE throughout entire sequence (same bathroom, bedroom, shower)
- ✅ SAME LIGHTING throughout (warm golden 2700K start to finish)
- ✅ OUTFIT/STATE explicitly defined at each image
- ✅ PROGRESSION visible (state 1 → 2 → 3 clearly)
- ❌ NO random outfit changes
- ❌ NO scene jumps (bathroom → bedroom → back)
- ❌ NO vague descriptions
- ❌ NO "same as previous"

**Example - GRWM Sequence (ALL in same bathroom vanity with warm golden light):**
```
Siena at bathroom vanity mirror, fresh face with no makeup visible, wearing casual undershirt, reaching toward makeup drawer with confidence, warm golden vanity lighting (2700K), bathroom mirror and counter visible, direct eye contact, professional beauty photography

Siena at bathroom vanity mirror, makeup actively being applied with visible makeup brush to eyes, eyeshadow visible appearing, eyes transforming, same undershirt, same warm golden bathroom vanity lighting (2700K), focused confident expression, professional beauty photography

Siena at bathroom vanity, full face makeup complete and glowing, now holding dress in hands putting it on, same warm golden lighting (2700K), complete makeup visible on face, anticipation in expression, professional beauty photography

Siena full body at bathroom mirror, complete dress visible and fitted on body, full makeup complete and visible, same warm golden vanity lighting (2700K), complete look visible (makeup + dress), confident powerful expression, professional glamorous photography

Siena at bathroom mirror in final power moment, complete look locked in (full makeup + complete outfit), direct camera eye contact, confident ownership, same warm golden lighting (2700K), breathing visible, freeze on ready moment, professional photography
```

## Video Prompt Structure - MOTION SHOWING TRANSITIONS

Each video prompt shows transitions between narrative states, not static poses.

**MANDATORY ELEMENTS:**

1. **Narrative Context:**
   - What state are we transitioning FROM?
   - What state are we transitioning TO?
   - What action shows this transition?

2. **Motion Details - EXPLICIT:**
   - Camera movement (fixed, pan, zoom, etc.)
   - Subject motion (reaching, applying, adjusting, stepping, etc.)
   - Motion speed and duration (over 3 seconds, fast 2-second adjust, etc.)
   - Hand movements if showing action
   - Head/eye movements reflecting the action
   - Body movement (not just poses)

3. **Scene/Lighting Consistency:**
   - SAME location throughout motion
   - SAME lighting throughout motion
   - No jumping between scenes

4. **Progression Visibility:**
   - Motion should show visible change/progress
   - Before/after states somewhat visible in segment
   - Action clearly demonstrates what's happening

5. **Expression/Eyes Progression:**
   - Starting expression
   - Transition expression
   - Ending expression (showing building confidence)
   - Eye contact maintained or building

**Example Video Prompts:**
```
Fixed camera on siena at bathroom vanity, reaching toward makeup drawer [motion over 2 seconds], opening drawer, selecting makeup brush, bringing brush to face, warm golden bathroom vanity lighting (2700K) maintained throughout, anticipation building in expression, eye contact with camera, hard cut to next

Fixed camera at bathroom vanity, makeup brush applying eyeshadow [visible motion over 4 seconds], eyes visibly transforming with makeup appearing, siena maintains confident focus on task, same warm golden vanity lighting (2700K), breathing visible, expression shifting to confidence as makeup appears, hard cut to next

Fixed camera, siena reaching for dress [1-second motion], pulling dress up over body [motion over 3 seconds], dress sliding on and settling, siena adjusting fit with hands, same bathroom setting, warm golden lighting (2700K), direct eye contact after dress is on, confidence building, hard cut to next

Fixed camera at full body bathroom mirror, siena in final power pose, direct eye contact for full 6 seconds, complete makeup visible on face, complete dress visible on body, same warm golden lighting (2700K), breathing visible, confident ownership expression, freeze or fade to black
```

## Generation Requirements ⭐ MANDATORY

When generating prompts from narrative scripts:

1. **Match Script Narrative:**
   - Extract the states from script
   - Image prompts must show STATE PROGRESSION clearly
   - Video prompts must show TRANSITIONS between states
   - ✅ Script says "makeup being applied" → video shows brush and eyes transforming
   - ✅ Script says "dress being put on" → video shows dress sliding on
   - ❌ Don't show random body poses when script is about applying makeup

2. **Scene Consistency - CRITICAL:**
   - ✅ Same bathroom throughout bathroom-based script
   - ✅ Same bedroom throughout bedroom-based script
   - ✅ Same shower throughout shower-based script
   - ❌ NO jumping between locations
   - ❌ NO changing lighting midway

3. **Outfit/State Progression - EXPLICIT:**
   - ✅ Image 1: "fresh face, no makeup, undershirt"
   - ✅ Image 2: "eyeshadow applied, undershirt"
   - ✅ Image 3: "full makeup, dress being put on"
   - ✅ Image 4: "full makeup, dress on"
   - ❌ NOT "sensual woman with makeup"
   - ❌ NOT vague state descriptions

4. **Each Prompt is STANDALONE but CONSISTENT:**
   - ✅ Each image specifies its STATE clearly
   - ✅ Each video shows relevant TRANSITION
   - ✅ All images use SAME scene, lighting, character
   - ❌ NO "same as previous"
   - ❌ NO cross-references between prompts

5. **Lighting Specifications:**
   - ALWAYS specify exact color temp: "2700K warm golden"
   - **MUST BE CONSISTENT throughout entire sequence**
   - Describe effect (catching light, highlighting, etc.)

6. **No Time Markers in Prompt:**
   - ❌ Don't: "At 1 second mark"
   - ✅ Do: Motion descriptions without time stamps

7. **No Branding/Tags:**
   - ❌ NO @desire.siena, usernames, hashtags
   - Prompts are pure visual descriptions only

8. **Segment Progression (6-second videos):**
   - Segment 1: Setup state introduction or start of action
   - Segment 2-5: Progressive transitions toward goal
   - Segment 6+: Peak state confirmation or power moment

**Remember:** Image prompts that DON'T specify scene/outfit state → inconsistent AI output. Image prompts that DO specify clearly → consistent, coherent sequence that tells a story.
