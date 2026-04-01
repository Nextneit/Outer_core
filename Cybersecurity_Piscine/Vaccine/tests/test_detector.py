import unittest
from unittest.mock import patch

from core import detector


class DummyResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code


class TestDetector(unittest.TestCase):
    def test_error_based_detection(self):
        responses = [
            DummyResponse("ok"),
            DummyResponse("You have an error in your SQL syntax near ..."),
        ]

        with patch("core.detector.inject_payload", side_effect=responses):
            found = detector.detect_error_based(None, "http://x/?id=1", "GET")

        self.assertTrue(found)

    def test_boolean_based_detection(self):
        responses = [
            DummyResponse("A" * 200),
            DummyResponse("B" * 120),
        ]

        with patch("core.detector.inject_payload", side_effect=responses):
            found = detector.detect_boolean_based(None, "http://x/?id=1", "GET")

        self.assertTrue(found)

    def test_time_based_detection(self):
        # inject_payload is called once, but elapsed time is simulated.
        with patch("core.detector.inject_payload", return_value=DummyResponse("ok")):
            with patch("core.detector.time.time", side_effect=[10.0, 14.2]):
                found = detector.detect_time_based(None, "http://x/?id=1", "GET")

        self.assertTrue(found)


if __name__ == "__main__":
    unittest.main()
