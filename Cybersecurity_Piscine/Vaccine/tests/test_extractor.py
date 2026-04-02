import unittest
from unittest.mock import patch

from core import extractor


class DummyResponse:
    def __init__(self, text):
        self.text = text


class TestExtractor(unittest.TestCase):
    def test_fingerprint_mysql(self):
        with patch(
            "core.extractor.inject_payload",
            return_value=DummyResponse("mysql information_schema"),
        ):
            engine = extractor.fingerprint_engine(
                None,
                "http://localhost/?id=1",
                "GET",
                "id",
            )
        self.assertEqual(engine, "mysql")

    def test_discover_vulnerable_parameter(self):
        def fake_inject_payload(_session, _url, _method, payload, target_param=None, verbose=False):
            del _session, _url, _method, verbose
            if target_param == "id" and "1=2" in payload:
                return DummyResponse("F" * 50)
            return DummyResponse("T" * 100)

        with patch("core.extractor.inject_payload", side_effect=fake_inject_payload):
            vulnerable, payloads = extractor.discover_vulnerable_parameters_with_payloads(
                None,
                "http://localhost/?id=1&Submit=Submit",
                "GET",
            )

        self.assertIn("id", vulnerable)
        self.assertTrue(any("TRUE=" in p for p in payloads))

    def test_sqlite_extraction_ignores_reflected_query(self):
        reflected = (
            "<b>Consulta ejecutada:</b><code>SELECT '"
            + extractor.START_MARK
            + "'||IFNULL((SELECT 'main'),'')||'"
            + extractor.END_MARK
            + "'</code>"
            "<b>Resultados:</b>[('"
            + extractor.START_MARK
            + "main"
            + extractor.END_MARK
            + "',)]"
        )

        with patch("core.extractor.inject_payload", return_value=DummyResponse(reflected)):
            value = extractor._extract_single_value(
                None,
                "http://localhost:5001/?user=admin",
                "GET",
                "user",
                "sqlite",
                1,
                0,
                "SELECT 'main'",
            )

        self.assertEqual(value, "main")


if __name__ == "__main__":
    unittest.main()
