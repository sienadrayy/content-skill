# Video Prompt Language Reference

Vocabulary for describing 4-second motion segments for i2v models. Each segment should be clear, specific, and optimized for smooth multi-clip assembly.

## Structure Template

Every video prompt follows this structure:

```
[Primary motion] [direction/type], [camera movement], [speed/intensity], [duration], [transition cue]
```

## Primary Motions

### Face/Head Motions
- **Eye contact hold** - Maintain direct gaze for duration
- **Blink** - Single or multiple blinks with held gaze
- **Slow blink** - Deliberate, sensual eye closure and opening
- **Gaze shift** - Eyes move from one direction to another
- **Head tilt** - Side-to-side head movement
- **Head turn** - Rotate head to face different direction
- **Look back** - Turn to look back over shoulder
- **Glance away** - Look away then return to camera

### Upper Body Motions
- **Shoulder roll** - Shoulders rotate back, open chest
- **Shoulder shimmy** - Subtle shoulder movement
- **Hair movement** - Hair flip, toss, or drift
- **Hair flip** - Quick dramatic hair movement
- **Clothing adjustment** - Adjust robe, strap, or garment
- **Neck elongate** - Subtle stretching of neck
- **Chest rise/fall** - Breathing visible

### Full Body Motions
- **Body roll** - Rotation from one side to front to other side
- **Recline** - Move from sitting to lying back position
- **Sit up** - Move from reclined to seated position
- **Slow walk** - Deliberate, intentional walking
- **Rotation/spin** - Turn 180° or 360°
- **Lean** - Shift weight and lean in direction
- **Stretch** - Elongate and stretch body

### Pose Transitions
- **Transition pose** - Move from one pose to another
- **Fluid transition** - Smooth, continuous movement between poses
- **Quick transition** - Snappy movement between positions
- **Slow transition** - Deliberate, extended movement between poses

## Camera Movements

### Camera Types
- **Fixed camera** - No camera movement, subject moves
- **Moving camera** - Camera itself moves

### Fixed Camera (Subject Moves)
- **Subject rotates** - Person spins/rotates in frame
- **Subject walks** - Movement through static frame
- **Subject poses** - Transition between poses without camera motion

### Moving Camera
- **Slow pan down** - Camera gradually moves downward
- **Pan up** - Camera moves upward
- **Pan left/right** - Camera moves horizontally
- **Tracking shot** - Camera follows subject movement
- **Zoom in** - Camera gets closer to subject
- **Zoom out** - Camera pulls back from subject
- **Slow dolly** - Smooth camera forward/back movement

### Combination Movements
- **Pan + subject motion** - Camera and subject move together
- **Zoom + subject holds** - Camera zooms while subject poses
- **Track + rotate** - Camera follows while subject rotates

## Speed & Intensity

### Movement Speed
- **Slow** - Takes 3-4 seconds for full motion
- **Deliberate** - Intentional, controlled pace
- **Smooth** - Flowing, no jerky movements
- **Fluid** - Continuous, seamless motion
- **Moderate** - Medium pace
- **Flowing** - Natural, graceful speed
- **Suspended** - Held moment with minimal motion

### Intensity Levels
- **Subtle** - Barely noticeable, minimal movement
- **Gentle** - Soft, delicate motion
- **Confident** - Strong, assured movement
- **Sensual** - Smooth, inviting motion
- **Dynamic** - More energetic, purposeful

## Duration & Timing

### Segment Duration
- **4 seconds** - Standard segment length
- **Hold for 3 seconds** - Pose stays static for 3s
- **Transition in 1 second** - Quick change within segment
- **Held throughout** - Motion maintained for full duration

### Rhythm
- **Slow paced** - Extended, leisurely motion
- **Beat matched** - Synced to music tempo
- **Continuous** - No pause or break
- **With pause** - Held moment in middle
- **Accelerating** - Gets faster through segment
- **Decelerating** - Slows down toward end

## Expression & Engagement

### Eyes
- **Direct eye contact** - Looking straight at camera
- **Eyes held** - Gaze maintained throughout
- **Eyes intense** - Strong, confident gaze
- **Eyes soften** - Gaze becomes gentler
- **Eyes sparkle** - Highlight/catchlight in eyes
- **Blink naturally** - Organic blinking pattern

### Face/Mouth
- **Confident expression** - Assured, present energy
- **Slight smile** - Subtle mouth curvature
- **Knowing smile** - Aware, playful expression
- **Sensual expression** - Inviting, alluring face
- **Lip bite** - Subtle teeth on lower lip
- **Lips parted slightly** - Mouth slightly open

### Overall Engagement
- **Connected to camera** - Aware of audience
- **Intimate** - Personal, close connection
- **Playful** - Fun, teasing energy
- **Mysterious** - Guarded, intriguing
- **Confident** - Self-assured, powerful

## Transitions Between Segments

### Transition Types
- **Cut** - Abrupt change to next segment
- **Fade** - Dissolve to black then fade in next
- **Dissolve** - Smooth crossfade to next segment
- **Continuous** - Seamless flow to next motion
- **Match cut** - Visual similarity between segments
- **Hard cut** - Quick, no fade

### Transition Positioning
- **Fade to next** - End with fade to black
- **Cut to [next description]** - Hard transition to specific next moment
- **Continuous to [next motion]** - Flows directly into next movement
- **Hold final pose** - End pose stays static for transition

## Lighting Maintenance

### During Motion
- **Lighting preserved** - No changes to light during segment
- **Lighting consistent** - Same illumination throughout
- **Shadow movement** - Natural shadow changes as subject moves
- **Highlight maintained** - Key light direction steady
- **Warm light throughout** - Golden/warm tones preserved

## Complete Video Prompt Examples

### Example 1: Eye Contact Hold (Static)
```
<Video 1>
Direct eye contact, slow blink at halfway point, confident expression held throughout 4 seconds, golden warm lighting preserved, no body movement, fade to next segment
```

### Example 2: Slow Pan Down
```
<Video 2>
Smooth camera pan down from face to shoulders, 3-second duration revealing body, siena maintains confident eye contact as much as visible, warm golden lighting, end on shoulder/chest reveal, cut to next
```

### Example 3: Body Roll
```
<Video 3>
Slow body roll rotation from side to front to side over full 4 seconds, sensual fluid motion, camera fixed, emphasize curves through movement, maintain eye contact/expression where visible, continuous fade to next
```

### Example 4: Hair Movement
```
<Video 4>
Hair flip or toss over 2 seconds, then hold with eye contact and knowing smile for remaining 2 seconds, soft golden lighting catches hair movement, body mostly static, emotional intensity building, dissolve to next
```

### Example 5: Sitting to Recline
```
<Video 5>
Slow transition from sitting to reclining position over 4 seconds, graceful movement emphasizing body positioning, maintain sensual expression, golden bedroom light consistent, confident throughout, hard cut to next moment
```

### Example 6: Rotation/Spin
```
<Video 6>
Slow 180° rotation over 4 seconds, reveal back and sides before returning to front-facing, camera stays fixed, allow body movement to show silhouette, lighting catches curves during rotation, end facing camera, fade to next
```

### Example 7: Pose Hold
```
<Video 7>
Hold confident pose for 3 seconds with no motion, subtle natural breathing visible, direct eye contact with knowing smile, warm light, in final second add subtle head tilt or hair adjustment for engagement, cut to next
```

### Example 8: Clothing Adjustment
```
<Video 8>
Reach and adjust clothing/robe strap or hem slowly over 2 seconds, sensual deliberate motion, return to pose for final 2 seconds with intensified eye contact, lighting maintains warmth, smooth transition to next
```

## Moment-to-Moment Flow Strategy

For smooth multi-segment assembly:

1. **Opening segment** - Establish look/pose, confidence
2. **Reveal segments** - Gradually show more, transitions between locations/angles
3. **Peak moment** - Sensual peak, maximum impact
4. **Engagement segments** - Direct camera connection moments
5. **Transition segments** - Movement that connects to next key moment
6. **Build segments** - Increasing energy/intensity
7. **Climactic moment** - Highest sensual peak
8. **Closing segments** - Maintain energy, smooth finish

## i2v Model Optimization

### Effective Prompts for i2v
- ✅ Specific motion descriptions work better than vague
- ✅ Duration specification (4 seconds) is critical
- ✅ Direction descriptors (pan, rotate, zoom) help consistency
- ✅ Lighting maintenance notes help transitions
- ✅ Expression/engagement descriptors improve quality
- ✅ Transition cues help multi-segment assembly

### Avoid
- ❌ Overly complex motion (stick to primary action)
- ❌ Conflicting motions (don't say "hold still" AND "walk")
- ❌ Vague timing (be specific: 3 seconds, not "quickly")
- ❌ Extreme camera movements (smooth, controlled motions)
- ❌ Sudden lighting changes (consistency preferred)

## Quick Reference Templates

### Static Pose Segment
```
[Expression/engagement type] maintained throughout 4 seconds, [eye direction], confident/sensual/playful energy, [lighting preserved], [subtle expression detail if any], [transition cue]
```

### Movement Segment
```
Slow [motion type] over 4 seconds, [camera movement if any], [engagement type] maintained, [lighting note], end [final positioning], [transition]
```

### Transition Segment
```
[Movement connecting current pose to next position], fluid/deliberate motion, 4 seconds, [engagement quality], warm lighting consistent, [final state ready for next segment]
```

### Peak Moment
```
[Primary sensual motion/pose], [eye contact and expression], confident/mysterious energy, all elements aligned for maximum impact, 4 seconds, [transition]
```
