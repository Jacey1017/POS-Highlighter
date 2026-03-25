# coding: utf-8
"""
This script processes a Markdown file and highlights words of a specific part of speech (POS) by underlining in Markdown.

Example Usage:
python pos_underliner.py example.md    # nouns (default)
python pos_underliner.py example.md [--pos VERB|ADJ|ADV|PRON]    # other POS tags, e.g. verbs, adjectives, ...
"""

import argparse
import re
import sys
import os
from pathlib import Path

import spacy
nlp = spacy.load("en_core_web_sm")

def underline_pos(line: str, pos_tag: str) -> str:
    """
    Italicizes words of a targeted pos with underscores.
    Args:
        line: a line of the input file
        pos_tag: Universal POS tags
    Returns:
        The new line with underlined words of matching pos tags.
    """

    # keep empty lines
    if not line.strip():
        return line

    # remove markdown symbols
    line_clean = re.sub(r"\*\*|#{1,6}\s*", "", line)

    doc = nlp(line_clean)

    # search for matching words
    pos_words = set()
    for token in doc:
        if token.pos_ == pos_tag:
            pos_words.add(token.text)

    # keep lines without matching words
    if not pos_words:
        return line

    # avoid double matches within a word
    sorted_words = sorted(pos_words, key=len, reverse=True)
    for w in sorted_words:
        # build pattern for all matching words
        pattern = r"\b(" + re.escape(w) + r")\b"
        # substitute matching words with _words_
        new_line = re.sub(pattern, r"_\1_", line)
        line = new_line

    return line

def process_file(input_file: Path, output_file: Path, pos_tag: str) -> None:
    """
    Reads input file line by line, generate output file with underlined words.
    Args:
        input_file: path to the Markdown file
        output_file: path to the output file
        pos_tag: Universal POS tags
    """

    with open (input_file, "r", encoding="utf-8") as f_in:
        with open(output_file, "w", encoding="utf-8") as f_out:
            for line in f_in:
                new_line = underline_pos(line, pos_tag)
                f_out.write(new_line)

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """

    parser = argparse.ArgumentParser(description="Highlights words of a specific POS in a Markdown file.")
    parser.add_argument("input_file", help="path to the Markdown file.")
    # extend default POS to Universal POS tags
    parser.add_argument("--pos", type=str, default="NOUN", help="Underlines the POS tag (default: NOUN).")

    # print help info when no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()

def main() -> None:
    args = parse_args()
    input_path = Path(args.input_file)

    if not input_path.exists():
        sys.exit(f"Error: Input file not found.")

    if input_path.suffix.lower() != ".md":
        sys.exit(f"Error: Please provide a Markdown file.")

    output_path = os.path.join(input_path.parent, "output.md")
    pos_tag = args.pos.upper()

    process_file(input_path, output_path, pos_tag)
    print(f"POS tag {pos_tag} highlighted.\nOutput file saved to {output_path}.")

if __name__ == "__main__":
    main()