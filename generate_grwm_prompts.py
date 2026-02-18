#!/usr/bin/env python3
"""
Generate I2V prompts for GRWM script
"""

images = [
    "Extreme close-up of siena's face, topless or minimal bikini top, direct INTENSE eye contact locked with camera, confident lip bite visible at 1-second moment, bare shoulders and collarbone fully exposed, warm golden bathroom vanity lighting (2700K), subtle breathing visible, peak confidence energy, professional intimate beauty photography, 9/10 intensity",
    
    "Siena in bathroom, bikini top strap pulled down partially, expose more upper chest and ribs visible, body at 20-degree angle showing side profile curves, hand trailing from collarbone downward sensually, confident eye contact maintained, warm golden lighting catching exposed skin and curves, professional body photography, 8.5/10 intensity",
    
    "Siena adjusting bikini bottom to show more hip and upper thigh exposure, standing power pose with confidence, minimal coverage bikini fully visible, direct camera engagement intensifying, hand positioned on hip showing ownership, lighting hits body definition and curves, breathing visible on chest, professional glamorous photography, 8.5/10 intensity",
    
    "Siena at 45-degree angle showing full side profile, back slightly arched emphasizing back curves and shoulder blades, minimal bikini coverage, hand on own hip, confident posture, warm golden lighting catching entire body silhouette and curves, direct eye contact from profile angle, professional photography, 9/10 intensity",
    
    "Siena mid-body-roll rotation visible, minimal bikini coverage throughout, hand tracing from collarbone sensually down toward hip, direct intense eye contact, confident expression at peak, breathing subtly visible on exposed chest, golden lighting emphasizing curves through body position, professional photography, 9/10 intensity",
    
    "Siena facing camera in power pose, minimal bikini/lingerie fully visible on body, hand positioned on own collarbone/hip area confident and unapologetic, INTENSE direct eye contact locked with camera, knowing confident smile, warm golden lighting on face and exposed skin, magnetic dominating energy, professional glamorous photography, 9/10 intensity",
    
    "Siena with hand pulling hair back to expose neck and collarbone fully, minimal bikini visible on body, bare neck and shoulders emphasized, eye contact intense and deepening, subtle breathing visible, expression showing peak confidence and sexuality, warm golden bathroom lighting throughout, professional beauty photography, 9/10 intensity",
    
    "Siena in strongest confident power stance, direct camera INTENSE eye contact, minimal coverage bikini frozen in place on body, breathing subtly visible on chest, expression peak confident and magnetic, bare shoulders and upper body fully exposed, warm golden lighting perfect on face and skin, ultimate sensual power moment, professional photography, 9/10 intensity"
]

videos = [
    "Extreme close-up camera on siena's face, INTENSE direct eye contact locked with camera throughout, lip bite visible at 1-second mark, hold intense stare for remaining 3 seconds, confident expression, warm golden bathroom lighting (2700K) on face, breathing subtly visible, magnetic commanding energy, hard cut to next",
    
    "Quick camera adjustment from face to shoulders, bikini strap pull motion visible, fast 2-second motion revealing more upper chest, warm golden lighting maintained, eye contact follows as body adjusts, breathing becomes visible on exposed chest, hard cut to next",
    
    "Fixed camera, fast bikini bottom adjustment over 2 seconds showing hip/thigh exposure, confident energy building, direct camera engagement, hand movement purposeful and sensual, minimal coverage visible, lighting hits new exposed areas, eye contact maintained, hard cut to next",
    
    "Fixed camera, smooth body rotation to 45-degree side profile over 3.5 seconds, back arch maintained emphasizing curves, warm golden lighting catches silhouette and body definition throughout motion, eye contact where visible from profile, confident expression, hard cut to next",
    
    "Fixed camera, slow confident body roll from side to front over 3.5 seconds, hand traces collarbone to hip with sensual intentional motion, direct intense eye contact when facing camera, minimal bikini throughout motion, breathing visible, golden light catches curves emphasized by rotation, hard cut to next",
    
    "Freeze on siena's face and upper body, INTENSE direct eye contact for full 4 seconds, confident power pose, hand near collarbone area, knowing confident smile building, minimal coverage visible, breathing visible on exposed chest, warm golden lighting perfect, magnetic dominating presence, hard cut to next",
    
    "Quick hand movement pulling hair back over 2 seconds, expose neck and collarbone fully, direct eye contact INTENSE throughout motion and hold, expression deepening in confidence, breathing visible on chest, bare shoulders emphasized, warm golden lighting highlights exposed areas, hard cut to next",
    
    "Freeze on strongest power pose facing camera, INTENSE direct eye contact held for 4 seconds, confident commanding expression, minimal bikini visible on body, breathing subtly visible on chest, expression shows peak sexuality and confidence, warm golden lighting perfect on face and exposed skin, magnetic presence, hard cut to black or fade"
]

print("IMAGE PROMPTS:\n")
for img in images:
    print(img)

print("\n---\n")
print("VIDEO PROMPTS:\n")
for vid in videos:
    print(vid)
