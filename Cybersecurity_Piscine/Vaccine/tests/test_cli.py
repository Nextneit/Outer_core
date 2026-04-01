import sys
import unittest
from unittest.mock import patch

from core.cli import parse_args


class TestCLI(unittest.TestCase):
    def test_defaults(self):
        with patch.object(sys, "argv", ["vaccine.py", "http://example.local/?id=1"]):
            args = parse_args()
        self.assertEqual(args.method, "GET")
        self.assertEqual(args.output, "output/results.txt")
        self.assertFalse(args.verbose)

    def test_custom_flags(self):
        with patch.object(
            sys,
            "argv",
            [
                "vaccine.py",
                "-X",
                "POST",
                "-o",
                "report.txt",
                "-v",
                "http://example.local/?id=1",
            ],
        ):
            args = parse_args()
        self.assertEqual(args.method, "POST")
        self.assertEqual(args.output, "report.txt")
        self.assertTrue(args.verbose)


if __name__ == "__main__":
    unittest.main()
