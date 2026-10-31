import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from openfx.docling_adapter import ExtractionError, extract_local_document


class FakeDocument:
    def export_to_markdown(self):
        return "# عنوان\nحد ضرر ۴۵ پوینت است؛ نیست."

    def export_to_dict(self):
        return {"texts": [{"text": "حد ضرر ۴۵ پوینت است؛ نیست.", "prov": [{"page_no": 1}]}]}


class FakeConverter:
    def __init__(self):
        self.kwargs = None

    def convert(self, path, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(document=FakeDocument(), status="success", errors=[])


class DoclingAdapterTests(unittest.TestCase):
    def test_extracts_local_file_with_provenance_and_limits(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sample.html"
            source.write_text("<p>fixture</p>", encoding="utf-8")
            converter = FakeConverter()
            artifact = extract_local_document(
                source, rights_review_state="synthetic_fixture",
                max_file_bytes=4096, max_pages=3,
                converter_factory=lambda: converter,
            )
        self.assertEqual(artifact["verification_state"], "unverified_extraction")
        self.assertEqual(artifact["rights_review_state"], "synthetic_fixture")
        self.assertEqual(len(artifact["source"]["sha256"]), 64)
        self.assertEqual(len(artifact["artifact_sha256"]), 64)
        self.assertEqual(converter.kwargs["max_num_pages"], 3)
        self.assertEqual(converter.kwargs["max_file_size"], 4096)
        self.assertIn("page_no", str(artifact["structured_document"]))

    def test_rejects_unsupported_extension(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sample.exe"
            source.write_bytes(b"not executable")
            with self.assertRaises(ExtractionError):
                extract_local_document(source, converter_factory=FakeConverter)

    def test_rejects_oversized_file_before_converter(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sample.html"
            source.write_bytes(b"12345")
            with self.assertRaises(ExtractionError):
                extract_local_document(source, max_file_bytes=4,
                                       converter_factory=FakeConverter)

    def test_resource_limits_must_be_positive(self):
        with self.assertRaises(ValueError):
            extract_local_document("does-not-need-to-exist.html", max_pages=0)

    def test_no_document_is_failure_not_empty_success(self):
        class EmptyConverter:
            def convert(self, *args, **kwargs):
                return SimpleNamespace(document=None, errors=["parse failed"])
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sample.html"
            source.write_text("fixture", encoding="utf-8")
            with self.assertRaisesRegex(ExtractionError, "parse failed"):
                extract_local_document(source, converter_factory=EmptyConverter)


if __name__ == "__main__":
    unittest.main()
