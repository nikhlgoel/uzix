# preprocessor.py
# Cleans and normalizes input text before pattern matching.
# Handles: unicode look-alikes, zero-width chars, leet speak,
# obfuscated spacing, base64 encoded payloads, HTML entities.

import re
import unicodedata
import base64
import html

# Zero-width and invisible unicode chars attackers insert to break pattern matching
ZERO_WIDTH_CHARS = re.compile(
    r"[\u200b\u200c\u200d\u200e\u200f\ufeff\u00ad\u2060\u2061\u2062\u2063]"
)

# Common Cyrillic/Greek homoglyphs mapped to their ASCII equivalents
# Attackers use these look-alike chars to slip past pattern matchers
HOMOGLYPH_MAP = str.maketrans({
    # Cyrillic
    "\u0430": "a",  # а → a
    "\u0435": "e",  # е → e
    "\u043e": "o",  # о → o
    "\u0440": "r",  # р → r
    "\u0441": "c",  # с → c
    "\u0445": "x",  # х → x
    "\u0443": "y",  # у → y
    "\u0410": "A",  # А → A
    "\u0415": "E",  # Е → E
    "\u041e": "O",  # О → O
    "\u0420": "R",  # Р → R
    "\u0421": "C",  # С → C
    "\u0425": "X",  # Х → X
    # Greek
    "\u03b1": "a",  # α → a
    "\u03b5": "e",  # ε → e
    "\u03bf": "o",  # ο → o
    "\u03c1": "p",  # ρ → p
    "\u0391": "A",  # Α → A
    "\u0395": "E",  # Ε → E
    "\u039f": "O",  # Ο → O
})

# Leet speak substitution map (covers common number/symbol replacements)
LEET_MAP = str.maketrans({
    "0": "o",
    "1": "i",
    "3": "e",
    "4": "a",
    "5": "s",
    "6": "g",
    "7": "t",
    "@": "a",
    "$": "s",
    "!": "i",
    "|": "i",
})


def normalize_unicode(text: str) -> str:
    """
    NFKC normalization: maps look-alike Unicode chars to their ASCII equivalents.
    e.g. Cyrillic 'а' → ASCII 'a', fullwidth letters → normal ASCII
    """
    return unicodedata.normalize("NFKC", text)


def strip_zero_width(text: str) -> str:
    """Remove invisible/zero-width chars used to break up words."""
    return ZERO_WIDTH_CHARS.sub("", text)


def decode_base64_fragments(text: str) -> str:
    """
    Finds base64-looking chunks in the text (>=8 chars, valid base64 alphabet),
    tries to decode them, and appends decoded content after the original.
    This way both the original and decoded form get checked.
    """
    # rough base64 pattern: at least 8 base64 chars followed by optional padding
    b64_pattern = re.compile(r"[A-Za-z0-9+/]{8,}={0,2}")
    decoded_parts = []
    for match in b64_pattern.finditer(text):
        chunk = match.group(0)
        # pad to multiple of 4
        padded = chunk + "=" * (-len(chunk) % 4)
        try:
            decoded = base64.b64decode(padded).decode("utf-8", errors="ignore")
            # only keep it if it decoded to readable ASCII-ish text
            if decoded and decoded.isprintable() and len(decoded) >= 4:
                decoded_parts.append(decoded)
        except Exception:
            pass
    if decoded_parts:
        text = text + " " + " ".join(decoded_parts)
    return text


def normalize_leet(text: str) -> str:
    """Replace common leet-speak substitutions with normal letters."""
    return text.translate(LEET_MAP)


def collapse_whitespace(text: str) -> str:
    """Collapse multiple spaces, tabs, newlines into a single space."""
    return re.sub(r"\s+", " ", text).strip()


def strip_html_entities(text: str) -> str:
    """Decode HTML entities like &lt; &#105;gnore → <ignore."""
    return html.unescape(text)


def strip_punctuation_obfuscation(text: str) -> str:
    """
    Remove dots, dashes, underscores used to split individual letters.
    e.g. 'i.g.n.o.r.e' → 'ignore', 'b-y-p-a-s-s' → 'bypass'
    Only strips when the pattern is clearly single chars in sequence (3+ chars).
    Leaves real hyphenated words like 'rok-tok' intact.
    """
    # Match: single char + (separator + single char) x2 or more
    # Catches i.g.n.o.r.e but not rok-tok (multi-char words)
    def remove_separators(m):
        return re.sub(r"[.\-_]", "", m.group(0))

    text = re.sub(
        r"\b[a-zA-Z]([.\-_][a-zA-Z]){2,}\b",
        remove_separators,
        text
    )
    return text


def normalize_homoglyphs(text: str) -> str:
    """Map common Cyrillic/Greek look-alike characters to their ASCII equivalents."""
    return text.translate(HOMOGLYPH_MAP)


def preprocess(text: str) -> str:
    """
    Full preprocessing pipeline. Run this on input before pattern matching.
    Returns a cleaned, normalized version of the text.
    """
    text = strip_html_entities(text)
    text = normalize_unicode(text)
    text = normalize_homoglyphs(text)
    text = strip_zero_width(text)
    text = decode_base64_fragments(text)
    text = strip_punctuation_obfuscation(text)
    text = normalize_leet(text)
    text = collapse_whitespace(text)
    return text
