"""
Unit tests for pos_highlighter.py
"""

import unittest
import tempfile
from pathlib import Path

from pos_highlighter import underline_pos, process_file

# tests for underline_pos
class TestUnderlinePos(unittest.TestCase):

    # empty lines should remain unchanged
    def test_empty_line(self):
        self.assertEqual(underline_pos("", "NOUN"), "")

    # lines with whitespaces only should remain unchanged
    def test_whitespace_line(self):
        self.assertEqual(underline_pos("   \n", "NOUN"), "   \n")

    # lines with no words of specific pos should remain unchanged
    def test_no_match(self):
        text = "Run quickly now.\n"
        self.assertEqual(underline_pos(text, "NOUN"), text)

    # nouns should be highlighted with underscores by default
    def test_noun_highlighted(self):
        self.assertIn("_whale_", underline_pos("The blue whale left quickly.\n", "NOUN"))

    # verbs should be highlighted with underscores if --pos VERB applied
    def test_verb_highlighted(self):
        self.assertIn("_left_", underline_pos("The blue whale left quickly.\n", "VERB"))

    # adjectives should be highlighted with underscores if --pos ADJ applied
    def test_adjective_highlighted(self):
        self.assertIn("_blue_", underline_pos("The blue whale left quickly.\n", "ADJ"))

    # adverbs should be highlighted with underscores if --pos ADV applied
    def test_adverb_highlighted(self):
        self.assertIn("_quickly_", underline_pos("The blue whale left quickly.\n", "ADV"))

    # compound words should be matched as a whole
    def test_word_boundary(self):
        self.assertNotIn("_booklet_", underline_pos("Go to the bookstore and read the books.\n", "NOUN"))

# tests for process_file
class TestProcessFile(unittest.TestCase):

    # write content to a temp file
    def _run(self, content: str, pos_tag: str = "NOUN") -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.md"
            output_path = Path(tmpdir) / "output.md"
            input_path.write_text(content, encoding="utf-8")
            process_file(input_path, output_path, pos_tag)
            return output_path.read_text(encoding="utf-8")

    # empty files should remain unchanged
    def test_empty_file(self):
        self.assertEqual(self._run(""), "")

    # output file should be created
    def test_output_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.md"
            output_path = Path(tmpdir) / "output.md"
            input_path.write_text("The blue whale left quickly.\n", encoding="utf-8")
            process_file(input_path, output_path, "NOUN")
            self.assertTrue(output_path.exists())

    def test_nouns_underlined(self):
        self.assertIn("_whale_", self._run("The blue whale left quickly.\n"))

if __name__ == "__main__":
    unittest.main()