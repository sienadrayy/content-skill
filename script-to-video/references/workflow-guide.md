# Script-to-Video Workflow Guide

Complete reference for using the orchestrator skill and handling verification steps.

## Complete Workflow Flow

```
USER: "Generate complete reel content"
↓
SKILL: Calls sensual-reels
↓
sensual-reels: Generates 60-sec script + concept
↓
SKILL: Presents script + concept to user
↓
SCRIPT DISPLAY:
   [Timeline script with all moments]
   [Concept details]
   "Ready to proceed? (yes/modify/regenerate)"
↓
USER: Responds with one of:
   - "Yes, proceed"
   - "Modify: [request]"
   - "Regenerate: [new concept]"
↓
IF YES → SKILL: Calls i2v-prompt-generator
↓
i2v-generator: Creates 8-10 image + video prompts
↓
FINAL OUTPUT (in conversation):
   [Original script]
   [8-10 image prompts]
   [8-10 video prompts]
↓
AUTO-DELIVERY: SKILL sends to WhatsApp (4 organized messages)
↓
WhatsApp Messages:
   Message 1: "Image Prompts"
   Message 2: [All 10 image prompts - single line between each, no labels]
   Message 3: "Video Prompts"
   Message 4: [All 10 video prompts - single line between each, no labels]
↓
Instagram contact (+447876137368) receives: ✅
   - Clean, organized message structure
   - Easy to copy/use with i2v model
   - No formatting clutter
↓
STATUS: ✅ Ready for i2v model
   - Display in chat
   - 4 WhatsApp messages sent
   - Team has clean prompts ready
```

## Response Types & Handling

### Response 1: "Yes" / "Proceed" / "Approved"

User is satisfied with script.

**Action:**
1. Mark script as approved ✅
2. Immediately call i2v-prompt-generator with exact script
3. Generate 8-10 image + video prompt pairs
4. Return complete final output

**Output includes:**
- Original approved script
- 8-10 image prompts (with siena keyword)
- 8-10 video prompts (4-second each)
- Clear section: "READY FOR i2v MODEL"

---

### Response 2: "Modify" / "Change" + Specific Request

User wants script adjustments before AI generation.

**Examples:**
- "Modify: Make it more playful, less mysterious"
- "Modify: Add more outdoor moments"
- "Modify: Slower pacing, more sensual"
- "Modify: Different outfit focus"

**Action:**
1. Note the modification request
2. Call sensual-reels again with the modification context
3. Generate new script incorporating feedback
4. Present new script for re-approval
5. Return to verification step

**Output at this step:**
```
MODIFIED SCRIPT (Iteration 2)
[New timeline with requested changes]
[Updated concept]

> Still good? (yes/modify/regenerate)
```

**Loop:** Can modify 2-3 times if needed before approval

---

### Response 3: "Regenerate" / "Different" / "Try Again"

User wants a completely different script (different concept entirely).

**Examples:**
- "Regenerate: Totally different vibe"
- "Regenerate: Outdoor instead of bedroom"
- "Regenerate: More energetic"
- "Regenerate: Different styling theme"

**Action:**
1. Note it's a full regeneration (not modification)
2. Call sensual-reels to generate completely new script + concept
3. Present new concept for approval
4. Return to verification step

**Output:**
```
NEW CONCEPT (Regeneration)
[Completely different script]
[Different concept]

> How's this? (yes/modify/regenerate)
```

**Loop:** Can regenerate multiple times until happy

---

## Optimization Tips

### Batch Generation
**Multiple scripts at once:**
```
"Generate 3 complete reel contents"
```

**Workflow:**
1. Generate script #1 → Show → Get approval
2. Convert to prompts → Deliver
3. Generate script #2 → Show → Get approval
4. Convert to prompts → Deliver
5. Generate script #3 → Show → Get approval
6. Convert to prompts → Deliver

**Benefit:** Get 3 complete production pipelines in one session

---

### Concept-Specific Generation
**If you have a specific mood:**
```
"Generate complete reel for: Luxury bedroom confidence, slow movements, direct camera engagement"
```

**Workflow:**
1. sensual-reels generates with your concept context
2. Script comes out tailored to your brief
3. Higher chance of first-approval
4. Skip modifications, go straight to i2v prompts

---

### Script Reuse
**Use approved script multiple times:**
```
"I have this script: [paste approved script]
Generate i2v prompts for this"
```

**Benefit:** 
- Keeps script consistency
- Can regenerate different i2v prompt variations
- Useful if you want multiple AI video options from same script

---

## Decision Tree

```
START: "Generate complete reel content"
    ↓
    ├─ sensual-reels outputs script + concept
    ├─ Present to user
    ├─ Ask: "Ready?"
    │
    ├─ YES
    │  ├─ Call i2v-prompt-generator
    │  ├─ Generate 8-10 prompt pairs
    │  ├─ Deliver final output
    │  └─ END ✅
    │
    ├─ MODIFY
    │  ├─ Note requested changes
    │  ├─ Call sensual-reels with modifications
    │  ├─ Generate modified script
    │  ├─ Present new version
    │  └─ Ask again (may loop)
    │
    └─ REGENERATE
       ├─ Call sensual-reels fresh
       ├─ Generate totally new concept
       ├─ Present new version
       └─ Ask again (may loop)
```

## Time Estimates

| Step | Time |
|------|------|
| sensual-reels script generation | 30 seconds |
| User verification | 1-2 minutes |
| i2v-prompt-generator conversion | 30 seconds |
| WhatsApp auto-delivery | 5 seconds |
| **Total** | **2-3 minutes** |

**With modifications:** +1-2 minutes per iteration

**With regenerations:** +30 seconds per regeneration

**WhatsApp delivery:** Automatic, no extra time needed

---

## Quality Checkpoints

### At Script Verification:

Ask yourself:
- ✅ Does this feel hot/sensual enough?
- ✅ Do the angles make sense for my body/location?
- ✅ Is the pacing right (enough time for each movement)?
- ✅ Does the concept match my outfit/props available?
- ✅ Is the energy right for @desire.siena brand?

**If NO on any:** Request modification or regeneration

### At Final Output:

Check i2v prompts:
- ✅ Does "siena" appear in every image prompt?
- ✅ Are video prompts 4 seconds each?
- ✅ Do transitions make sense between moments?
- ✅ Is sensuality level consistent throughout (8-9/10)?
- ✅ Can you actually film this with your setup?

**If issues:** Either modify the script and regenerate prompts, or feed prompts to your i2v model and let it improve them.

---

## Common Workflows

### Morning Routine (Daily Content)
```
TIME: 7:00 AM
ACTION: "Generate complete reel content"
   ↓ 1 minute: Script appears
   ↓ 1 minute: You approve
   ↓ 30 sec: i2v prompts generated
   ↓ Auto: Prompts sent to Instagram on WhatsApp ✅
RESULT: Ready to brief team/start shooting by 7:05 AM
        Team already has prompts on WhatsApp!
```

### Weekly Batch
```
Monday: Generate 5 complete reels
   - Review all scripts (5 mins)
   - Approve best 3
   - Get i2v prompts for those 3
   - Plan shoot schedule for week
```

### Concept-Driven
```
"I want more outdoor content this week"
   ↓ Generate: "Outdoor golden hour concepts"
   ↓ Iterate: 2-3 regenerations until golden
   ↓ Approve: Get i2v prompts
   ↓ Shoot: All outdoor focused week
```

---

## Troubleshooting

### Script Doesn't Feel Hot Enough

**Response:** "Regenerate: Make it 9/10 intensity, more revealing"

sensual-reels will push the envelope more.

### Too Many Moments to Shoot

**Response:** "Modify: Fewer transitions, focus on key moments"

i2v-generator will select fewer, more impactful moments.

### Outfit Doesn't Match Concept

**Response:** "Modify: Use [your outfit] as styling"

sensual-reels will rewrite script to match what you're wearing.

### Don't Like i2v Prompts

**Option 1:** Go back to script approval, "Modify: [request]"  
**Option 2:** Feed script and prompts to i2v model, let it interpret creatively

---

## Pro Formula

**For maximum daily efficiency:**

1. **Morning (2 mins):** "Generate complete reel content"
2. **Approval (1 min):** Quick yes/modify decision
3. **Output (30 sec):** Get i2v prompts
4. **Result:** Shoot-ready script + prompts before coffee ☕

**Repeat daily or 3x/week for consistent content supply.**
