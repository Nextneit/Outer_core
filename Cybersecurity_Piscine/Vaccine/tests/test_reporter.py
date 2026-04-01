import unittest

from core.extractor import ExtractionResult
from core.reporter import format_results


class TestReporter(unittest.TestCase):
    def test_format_results_includes_extraction(self):
        extraction = ExtractionResult(
            vulnerable_parameters=["id"],
            payloads_used=["Boolean probes per parameter", "UNION SELECT"],
            engine="mysql",
            current_db="dvwa",
            databases=["dvwa"],
            tables={"dvwa": ["users"]},
            columns={"users": ["user", "password"]},
            dump={"users": [{"user": "admin", "password": "hash"}]},
        )

        output = format_results(
            "http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit",
            ["Error-based", "Boolean-based"],
            extraction=extraction,
        )

        self.assertIn("Parámetros vulnerables: id", output)
        self.assertIn("Motor detectado: mysql", output)
        self.assertIn("users", output)
        self.assertIn("admin", output)


if __name__ == "__main__":
    unittest.main()
