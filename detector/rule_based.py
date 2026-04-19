# Rule-based Prompt Injection Detector
# Phase 1: Basic pattern matching for English, Hindi, Hinglish
# Returns: SAFE / SUSPICIOUS / DANGEROUS

import re
from typing import Literal

# Common English prompt injection patterns
ENGLISH_PATTERNS = [
    r"ignore (all|previous|above) instructions",
    r"disregard (all|previous|above) instructions",
    r"repeat after me",
    r"you are now",
    r"pretend to",
    r"as an ai language model,?",
    r"forget you are an ai",
    r"do not obey previous",
    r"bypass",
    r"override",
    r"disregard previous instructions",
    r"do anything now",
    r"jailbreak",
    r"unfiltered response",
    r"no restrictions",
    r"ignore content policy",
]

# Hindi/Hinglish patterns (Devanagari and transliterated)
HINDI_PATTERNS = [
    r"सभी निर्देशों को अनदेखा करें",  # Ignore all instructions
    r"पिछले निर्देशों को भूल जाओ",    # Forget previous instructions
    r"मेरे बाद दोहराओ",              # Repeat after me
    r"तुम अब हो",                    # You are now
    r"नियम तोड़ो",                   # Break the rules
    r"bina rok-tok ke jawab do",      # Hinglish: answer without restriction
    r"sabhi niyam bhool jao",         # Hinglish: forget all rules
    r"tum ab ho",                     # Hinglish: you are now
    r"koi rok nahi hai",              # Hinglish: no restriction
]

# Combine all patterns
ALL_PATTERNS = ENGLISH_PATTERNS + HINDI_PATTERNS

# Compile regexes for performance
COMPILED_PATTERNS = [re.compile(pat, re.IGNORECASE) for pat in ALL_PATTERNS]

RiskLevel = Literal["SAFE", "SUSPICIOUS", "DANGEROUS"]

def detect_prompt_injection(text: str) -> RiskLevel:
    """
    Returns:
        - "DANGEROUS" if strong match to known attack pattern
        - "SUSPICIOUS" if partial/weak match
        - "SAFE" otherwise
    """
    matches = [pat for pat in COMPILED_PATTERNS if pat.search(text)]
    if matches:
        # If multiple strong matches, mark as dangerous
        if len(matches) > 1:
            return "DANGEROUS"
        return "SUSPICIOUS"
    return "SAFE"

if __name__ == "__main__":
    import sys
    prompt = sys.argv[1] if len(sys.argv) > 1 else input("Enter prompt: ")
    result = detect_prompt_injection(prompt)
    print(f"Risk: {result}")
