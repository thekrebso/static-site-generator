import unittest
from blocktype import (
    BlockType,
    block_to_blocktype
)


class Test_block_to_blocktype(unittest.TestCase):
    def test_paragraph_single_line(self):
        text = "This is a single-line paragraph"
        expected = BlockType.PARAGRAPH
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected)

    def test_paragraph_multi_line(self):
        text = "This is a multi-\nline paragraph"
        expected = BlockType.PARAGRAPH
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected)

    def test_code_single_line(self):
        text = "```This is single-line code```"
        expected = BlockType.CODE
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected)

    def test_code_multi_line(self):
        text = "```\nThis is multi-line code\n```"
        expected = BlockType.CODE
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected)

    def test_heading_h1(self):
        text = "# This is h1"
        expected = BlockType.HEADING
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected)

    def test_heading_h2(self):
        text = "## This is h2"
        expected = BlockType.HEADING
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected)

    def test_heading_h3(self):
        text = "### This is h3"
        expected = BlockType.HEADING
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected)

    def test_heading_h4(self):
        text = "#### This is h4"
        expected = BlockType.HEADING
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected)

    def test_heading_h5(self):
        text = "##### This is h5"
        expected = BlockType.HEADING
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected)

    def test_heading_h6(self):
        text = "###### This is h6"
        expected = BlockType.HEADING
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected)

    def test_quote_single_line(self):
        text = "> This is single line quote"
        expected = BlockType.QUOTE
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected) 

    def test_quote_multi_line(self):
        text = "> This is\n> Multi-line\n> quote"
        expected = BlockType.QUOTE
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected) 

    def test_unordered_list_single_line(self):
        text = "- first"
        expected = BlockType.UNORDERED_LIST
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected) 

    def test_unordered_list_multi_line(self):
        text = "- first\n- second\n- third"
        expected = BlockType.UNORDERED_LIST
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected) 

    def test_ordered_list_single_line(self):
        text = "1. first"
        expected = BlockType.ORDERED_LIST
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected) 

    def test_ordered_list_multi_line(self):
        text = "1. first\n2. second\n3. third"
        expected = BlockType.ORDERED_LIST
        actual = block_to_blocktype(text)
        self.assertEqual(actual, expected) 



if __name__ == "__main__":
    unittest.main()
