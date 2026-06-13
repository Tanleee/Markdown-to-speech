# Markdown to Speech Converter (gTTS)

A simple and effective Python script that converts Markdown (`.md`) text files into audio files (`.mp3`) using Google Text-to-Speech (**gTTS**).

This tool automatically strips out complex Markdown formatting (such as code blocks, bold/italics, links, and special characters) to generate a natural, fluent, and uninterrupted voice output.

## Key Features

- **Automatic Markdown Cleaning:** Ignores code blocks, links, images, and formatting syntax. Converts heading tags into periods to ensure natural reading pauses.
- **Bypasses API Limits:** Automatically splits the text into smaller chunks based on sentence boundaries to prevent Google TTS character limit errors.
- **Auto-Merging:** Downloads the short audio chunks and seamlessly concatenates them into a single, complete `.mp3` file.
- **Multi-language Support:** Easily change the language (e.g., English, Vietnamese, etc.) and reading speed through simple configuration variables.

## Prerequisites

- Python 3.x
- `gTTS` (Google Text-to-Speech) library

## Installation & Usage

### 1. Install the Required Library

Open your terminal or command prompt and install the `gTTS` library via pip:

```bash
pip install gTTS
```
