# Part of Speech (POS) Underlining

This script reads a Markdown file and italicises words of a specific part of speech (POS) using spaCy.

## Requirements

- Python 3.9 or higher must be installed on your system.
- This script is designed for macOS, but it should also work on Linux and Windows.

## Installation

1. Create and activate a virtual environment:

    `python3 -m venv venv`

    `source venv/bin/activate`


2. Install dependencies:

    `pip install spacy pytest` OR `pip install -r requirements.txt`


3. Download the spaCy English language model

    `python -m spacy download en_core_web_sm`


## Usage

Run the script with a Markdown file as input:

- for nouns (default)

    `python pos_highlighter.py example.md`

    
- for other [Universal POS tags](https://universaldependencies.org/u/pos/) (e.g. verbs, adjectives, adverbs, pronouns)

    `python pos_highlighter.py example.md [--pos VERB|ADJ|ADV|PRON]`

  The output.md is saved to the same directory as the input file.


## Tests

Run unit tests:

`python -m pytest test_pos_highlighter.py -v`