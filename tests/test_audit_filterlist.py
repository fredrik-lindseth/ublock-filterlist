import importlib.util
from pathlib import Path
import unittest


MODULE = Path(__file__).parents[1] / "scripts" / "audit_filterlist.py"
SPEC = importlib.util.spec_from_file_location("audit_filterlist", MODULE)
audit_filterlist = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(audit_filterlist)


class AuditFilterlistTests(unittest.TestCase):
    def test_accepts_grouped_domains(self):
        errors, _ = audit_filterlist.audit(["a.no,b.no##.banner\n"])
        self.assertEqual(errors, [])

    def test_rejects_path_in_cosmetic_hostname(self):
        errors, _ = audit_filterlist.audit(["klikk.no/index.html##.banner\n"])
        self.assertTrue(any("contains '/'" in error for error in errors))

    def test_rejects_body_scroll_typo(self):
        errors, _ = audit_filterlist.audit(["a.no###body,html:style(overflow:auto)\n"])
        self.assertTrue(any("not ###body" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
