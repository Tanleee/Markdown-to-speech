"""
Markdown to Speech (using gTTS - Google Text-to-Speech)
===============================================================
Install:  pip install gTTS
Run:      python md_to_speech.py

Output: .mp3 file in the same directory
"""

import re
import sys
import os
import tempfile
from pathlib import Path

try:
    from gtts import gTTS
except ImportError:
    print("gTTS is not installed. Run:  pip install gTTS")
    sys.exit(1)

# ── Configuration ─────────────────────────────────────────────────────────────
MD_FILE   = "united.md" # change this file name
LANG      = "en"        # change to 'vi' for Vietnamese, etc...
SLOW      = False       # True = slower speech rate
MAX_CHARS = 500         # Character limit per chunk sent to Google
# ──────────────────────────────────────────────────────────────────────────────


def strip_markdown(text: str) -> str:
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`]+`", "", text)
    # Convert headings to text + period for a natural speech pause
    text = re.sub(r"^#{1,6}\s+(.+)$", r"\1.", text, flags=re.MULTILINE)
    text = re.sub(r"\*{1,3}(.+?)\*{1,3}", r"\1", text)
    text = re.sub(r"_{1,3}(.+?)_{1,3}", r"\1", text)
    text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\|.*\|$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[|\s:-]+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^\)]+\)", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    # Remove leading em dashes, replace with commas for natural speech pauses
    text = re.sub(r"\s*—\s*", ", ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_chunks(text: str, max_chars: int = MAX_CHARS) -> list:
    """Split text into smaller chunks, breaking at sentence boundaries."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""

    for para in paragraphs:
        if len(para) > max_chars:
            # Paragraph is too long → split by sentence
            sentences = re.split(r"(?<=[.!?,])\s+", para)
            for sent in sentences:
                if len(current) + len(sent) + 1 <= max_chars:
                    current += (" " if current else "") + sent
                else:
                    if current:
                        chunks.append(current.strip())
                    current = sent
        else:
            if len(current) + len(para) + 2 <= max_chars:
                current += (" " if current else "") + para
            else:
                if current:
                    chunks.append(current.strip())
                current = para

    if current.strip():
        chunks.append(current.strip())

    return [c for c in chunks if c]


def convert(md_path: Path):
    raw   = md_path.read_text(encoding="utf-8")
    clean = strip_markdown(raw)

    # Save cleaned text for debugging
    txt_path = md_path.with_suffix(".txt")
    txt_path.write_text(clean, encoding="utf-8")
    print(f"✔ Cleaned text  → {txt_path.name}  ({len(clean)} characters)")

    chunks = split_chunks(clean)
    total  = len(chunks)
    print(f"✔ Split into {total} chunks\n")

    tmp_dir   = tempfile.mkdtemp()
    tmp_files = []

    for i, chunk in enumerate(chunks, 1):
        tmp_file = os.path.join(tmp_dir, f"part_{i:03d}.mp3")
        print(f"  [{i:2d}/{total}] {len(chunk):3d} characters → ", end="", flush=True)
        try:
            tts = gTTS(text=chunk, lang=LANG, slow=SLOW)
            tts.save(tmp_file)
            tmp_files.append(tmp_file)
            print("✔")
        except Exception as e:
            print(f"✗ ERROR: {e}")
            print("Check your internet connection and try again.")
            # Clean up temporary files and exit
            for f in tmp_files:
                os.remove(f)
            os.rmdir(tmp_dir)
            sys.exit(1)

    # Merge all chunks into a single MP3 file
    mp3_path = md_path.with_suffix(".mp3")
    print(f"\n⏳ Merging {len(tmp_files)} chunks...")
    with open(mp3_path, "wb") as out:
        for f in tmp_files:
            with open(f, "rb") as part:
                out.write(part.read())

    for f in tmp_files:
        os.remove(f)
    os.rmdir(tmp_dir)

    size_kb = mp3_path.stat().st_size // 1024
    print(f"\n✅ Done!  →  {mp3_path.name}  ({size_kb} KB)")
    print("Open with VLC or your preferred media player to listen.")


def main():
    md_path = Path(MD_FILE)
    if not md_path.exists():
        candidates = list(Path(".").glob("*.md"))
        if candidates:
            md_path = candidates[0]
            print(f"Using file: {md_path}\n")
        else:
            print(f"File not found: {MD_FILE}")
            print("Update the MD_FILE variable at the top of the script with the correct filename.")
            sys.exit(1)
    convert(md_path)


if __name__ == "__main__":
    main()