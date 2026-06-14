import re

# Patterns that indicate a request needs a doctor, not a coach
MEDICAL_PATTERNS = [
    r"\bdiagnos(e|is|ed|ing)\b",
    r"\bmedication(s)?\b",
    r"\bprescri(ption|be|bed|bing)\b",
    r"\bdosage?\b",
    r"\binsulin\b",
    r"\bblood sugar\b",
    r"\bdiabet(es|ic)\b",
    r"\bhypertension\b",
    r"\bcholesterol\b",
    r"\bthyroid\b",
    r"\bantidepressant\b",
    r"\bantibiotics?\b",
    r"\bchemotherapy\b",
    r"\bcancer\b",
    r"\btumor\b",
    r"\bsurgery\b",
    r"\bsymptom(s)?\b",
    r"\btreat(ment|ing|ed)?\b",
    r"\bcure\b",
    r"\bsick\b",
    r"\bill(ness)?\b",
    r"\bdisease\b",
    r"\binfection\b",
    r"\bvirus\b",
    r"\bbacteria\b",
    r"\bfever\b",
    r"\bpain\b",
    r"\bhurt(s|ing)?\b",
    r"\bsore\b",
    r"\bache\b",
    r"\bnausea\b",
    r"\bdizziness\b",
    r"\bvomit(ing)?\b",
    r"\bdiarrhea\b",
    r"\bbleeding\b",
    r"\brash\b",
    r"\ballergy|allergic\b",
    r"\bsupplement dosage\b",
    r"\bvitamin dosage\b",
]

# Patterns that require an immediate emergency redirect
EMERGENCY_PATTERNS = [
    r"\bchest pain\b",
    r"\bcan'?t breathe\b",
    r"\bdifficulty breathing\b",
    r"\bshortness of breath\b",
    r"\bheart attack\b",
    r"\bstroke\b",
    r"\bseizure\b",
    r"\bunconscious\b",
    r"\bpassing out\b",
    r"\bsuicid(e|al)\b",
    r"\bkill myself\b",
    r"\bend my life\b",
    r"\bself.harm\b",
    r"\boverdose\b",
    r"\bsevere bleeding\b",
    r"\bcan'?t stop bleeding\b",
    r"\bbroken bone\b",
    r"\bspinal\b",
    r"\bemergency\b",
    r"\b911\b",
    r"\bambulance\b",
    r"\bparalysi(s|zed)\b",
    r"\bsevere allergic reaction\b",
    r"\banaphylaxis\b",
]

EMERGENCY_RESPONSE = """**This sounds like it may be a medical emergency.**

Please take action immediately:
- **Call emergency services** (911 in the US, 999 in the UK, 112 in Europe)
- Or go to your nearest emergency room
- Or call a trusted person who can help you right now

If you are in emotional distress, please contact:
- **988 Suicide & Crisis Lifeline:** Call or text **988** (US)
- **Crisis Text Line:** Text HOME to **741741**

I'm a wellness coach and am not equipped to help with emergencies. Please reach out to the people above — you matter.
"""

MEDICAL_REDIRECT_RESPONSE = """That's an important question, and I want to make sure you get the right support.

As a wellness coach, I'm not qualified to advise on medical symptoms, diagnoses, medications, or treatment plans. For what you're describing, the right person to speak to is:

- **Your primary care doctor** or GP
- **A registered dietitian** for medically specific diet needs
- **A licensed pharmacist** for medication questions
- **A mental health professional** for emotional health concerns

What I *can* help with is general wellness — building better sleep habits, stress management techniques, gentle movement ideas, and nourishing eating patterns for someone without specific medical conditions.

Is there a general wellness topic I can support you with today?
"""


def check_safety(message: str) -> tuple[bool, str]:
    """
    Check if a message requires a safety redirect.

    Returns (is_unsafe, response_message).
    If safe, returns (False, "").
    """
    lowered = message.lower()

    for pattern in EMERGENCY_PATTERNS:
        if re.search(pattern, lowered):
            return True, EMERGENCY_RESPONSE

    for pattern in MEDICAL_PATTERNS:
        if re.search(pattern, lowered):
            return True, MEDICAL_REDIRECT_RESPONSE

    return False, ""
