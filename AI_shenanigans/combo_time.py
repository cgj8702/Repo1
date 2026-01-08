import re
import pdfplumber
import os
import json
from tqdm import tqdm

# --- CONFIGURATION ---
SCRIPTS_FOLDER = "C:/Users/carly/Documents/Coding/episode_scripts/"
OUTPUT_FOLDER = "C:/Users/carly/Documents/Coding/Hannibal_chunks/"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

UNIT = r"(?=.*\d)[A-Z0-9]+(?:-[A-Z0-9]+)?"
STRICT_BLACKLIST = [
    "TEASER",
    "ACT ONE",
    "ACT TWO",
    "ACT THREE",
    "ACT FOUR",
    "ACT FIVE",
    "CONTINUED",
    "OMITTED",
    "SHOW",
    "END OF SHOW",
    "END OF TEASER",
    "ACT ",
]


def is_junk_line(text):
    """Vaporizes zombie metadata and technical jargon."""
    clean = text.strip()
    if not clean:
        return True

    # 1. THE ZOMBIE LIST (If these appear ANYWHERE, line dies)
    DESTROY_LIST = [
        "CONTINUED",
        "OMITTED",
        "ACT ONE",
        "ACT TWO",
        "ACT THREE",
        "ACT FOUR",
        "ACT FIVE",
        "END OF SHOW",
        "END OF ACT",
        "END OF TEASER",
        "CUT TO",
        "BACK TO",
        "POP TO",
        "AIR #",
        "PROD #",
        "MORE",
        "CHYRON",
        "We are--",
        "We are --",
        "SMASH BACK TO",
        "QUICK POP TO",
    ]
    if any(junk in clean for junk in DESTROY_LIST):
        return True

    # 2. HANNIBAL PRODUCTION FOOTER
    if re.search(r"HANNIBAL\s*-\s*(?:AIR|PROD).*?#\d+", clean, re.I):
        return True

    # 3. DIRECTORIAL JARGON
    tech_regex = r"^\s*(?:WIDENING|REVERSING|REVEALS|PUSH|POP|FOLLOWS|CLOSE ON|ON WILL|ON HANNIBAL|ON JACK|ON CAMERA|OFF WILL|OFF HANNIBAL|OFF JACK|OFF CAMERA|INCLUDE|STOCK FOOTAGE).*$"
    if re.match(tech_regex, clean, re.I):
        return True

    # 4. MARGIN CODES / EPISODE TITLES
    if clean == '"Amuse-Bouche"':
        return True
    if re.match(rf"^\s*{UNIT}\.?\s*$", clean):
        return True

    return False


def get_line_type(raw_line):
    """
    STRICT Gutters for Shooting Scripts:
    - Action/Sluglines: Left (0-15 spaces)
    - Dialogue: Middle (16-32 spaces) + NARROW width
    - Character Names: Deep (33+ spaces) + ALL CAPS
    """
    clean = raw_line.strip()
    if not clean:
        return "EMPTY", ""

    leading = len(raw_line) - len(raw_line.lstrip())
    line_width = len(clean)

    # 1. CHARACTER NAMES (Deep centered indent)
    if leading >= 32 and clean.isupper() and clean not in STRICT_BLACKLIST:
        # Filter parentheticals that slip into character gutter
        if not clean.startswith("("):
            return "CHARACTER", re.sub(r"\(.*?\)", "", clean).strip()

    # 2. DIALOGUE (Centered column + Narrow line width)
    # Dialogue in scripts is rarely wider than 45 chars.
    if 16 <= leading < 32 and line_width < 50:
        if clean.startswith("(") and clean.endswith(")"):
            return "EMPTY", ""
        return "DIALOGUE", clean

    # 3. SLUGLINES (Left margin keywords)
    if leading < 16 and any(x in clean for x in ["INT.", "EXT.", "I/E", "INT/EXT"]):
        return "SLUGLINE", clean

    # 4. ACTION (Descriptions)
    # If it's at the left OR if it's too wide to be dialogue
    if leading < 16 or line_width >= 50:
        return "ACTION", clean

    return "ACTION", clean


def process_script(pdf_path):
    chunks = []
    current_scene_content = []
    current_scene_title = "START"

    active_speaker = None
    speech_buffer = []

    def flush_dialogue():
        """Saves current buffer and clears speaker state."""
        nonlocal active_speaker, speech_buffer
        if active_speaker and speech_buffer:
            speech = " ".join(speech_buffer).strip()
            if speech:
                current_scene_content.append(f'{active_speaker}: "{speech}"')
        active_speaker = None
        speech_buffer = []

    tqdm.write(f"Processing: {os.path.basename(pdf_path)}...")

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[1:]:
            text = page.extract_text(layout=True)
            if not text:
                continue

            for line in text.split("\n"):
                # Revision markers check (The very edge of the page)
                if "Final Shooting Script" in line or "Collated" in line:
                    continue

                # 1. Kill Junk immediately
                if is_junk_line(line):
                    # Junk lines between dialogue paragraphs act as a reset
                    if "CONTINUED" not in line.upper():
                        flush_dialogue()
                    continue

                l_type, content = get_line_type(line)

                # 2. SCENE BREAK
                if l_type == "SLUGLINE":
                    flush_dialogue()
                    if current_scene_content:
                        chunks.append(
                            {
                                "heading": current_scene_title,
                                "content": "\n".join(current_scene_content).strip(),
                            }
                        )
                        current_scene_content = []
                    current_scene_title = re.sub(
                        rf"^{UNIT}\s+|\s+{UNIT}$", "", content
                    ).strip()

                # 3. SPEAKER BREAK
                elif l_type == "CHARACTER":
                    flush_dialogue()
                    active_speaker = content

                # 4. SPEECH COLLECTION
                elif l_type == "DIALOGUE":
                    speech_buffer.append(content)

                # 5. ACTION / NARRATION
                elif l_type == "ACTION":
                    # THE RESET: The character is done talking when prose starts
                    flush_dialogue()

                    # Clean margin numbers off narration
                    cleaned_action = re.sub(
                        rf"^{UNIT}\s+|\s+{UNIT}$", "", content
                    ).strip()
                    if cleaned_action and cleaned_action not in STRICT_BLACKLIST:
                        current_scene_content.append(cleaned_action)

    flush_dialogue()  # Last catch
    if current_scene_content:
        chunks.append(
            {
                "heading": current_scene_title,
                "content": "\n".join(current_scene_content).strip(),
            }
        )

    return chunks


# --- EXECUTION ---
pdf_files = [f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".pdf")]
for filename in tqdm(pdf_files, desc="Parsing Chunks"):
    data = process_script(os.path.join(SCRIPTS_FOLDER, filename))
    base = os.path.splitext(filename)[0]

    with open(
        os.path.join(OUTPUT_FOLDER, f"{base}_data.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(data, f, indent=4)

    with open(
        os.path.join(OUTPUT_FOLDER, f"{base}_debug.txt"), "w", encoding="utf-8"
    ) as f:
        for scene in data:
            f.write(f"=== {scene['heading']} ===\n{scene['content']}\n\n")

print(f"\nVictory! Chunks are clean and novelized. 🦌🍷")
