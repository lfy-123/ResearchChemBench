"""Regression checks for the read-only geometry audit, not chemistry validation."""
import tempfile
import unittest
from pathlib import Path

from scripts.audit_agent_geometry_leakage import audit, structure_markers, xyz_signature


class GeometryAuditTest(unittest.TestCase):
    def test_filename_markers(self):
        self.assertIn("transition_state", structure_markers("ts2_prime.xyz", ""))
        self.assertIn("optimized", structure_markers("compound_1_optimized.xyz", ""))
        self.assertIn("source_si", structure_markers("azotriazole_ts2_si.xyz", ""))
        self.assertIn("product", structure_markers("product_3a.xyz", ""))

    def test_silicon_is_not_si_provenance(self):
        self.assertEqual([], structure_markers("silicon.xyz", "Si starting geometry"))

    def test_coordinate_signature_ignores_labels_and_numeric_format(self):
        self.assertEqual(xyz_signature("1\nTS from SI\nH 0.0 -0.00 1.000\n"),
                         xyz_signature("1\nneutral label\nH 0 0 1e0\n"))
        self.assertNotEqual(xyz_signature("1\nx\nH 0 0 1\n"),
                            xyz_signature("1\nx\nH 0 0 2\n"))

    def test_malformed_or_multiframe_xyz_is_reported(self):
        for text in ("", "1\nx\nH NaN 0 0\n", "2\nx\nH 0 0 0\n",
                     "1\nx\nH 0 0 0\n1\ny\nH 0 0 1\n"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                xyz_signature(text)

    def test_renamed_files_are_matched_across_modes_without_modifying_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inputs = []
            for mode, name, comment in (("autonomous_research", "candidate.xyz", "model"),
                                        ("paper_reproduction", "ts2.xyz", "SI TS2")):
                package = root / mode / "paper_fixture"
                public = package / "agent_input/data/inputs"
                public.mkdir(parents=True)
                (package / "task_info.json").write_text("{}")
                path = public / name
                text = f"1\n{comment}\nH 0 0 0\n"
                path.write_text(text)
                inputs.append((path, text))
            result = audit(root)
            self.assertEqual(1, result["counts"]["equal_coordinate_papers"])
            self.assertEqual(1, len(result["findings"]))
            self.assertEqual(2, len(result["structure_inventory"]))
            self.assertEqual([], result["errors"])
            for path, content in inputs:
                self.assertEqual(content, path.read_text())

    def test_missing_roots_fail_instead_of_reporting_a_clean_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                audit(Path(directory))


if __name__ == "__main__":
    unittest.main()
