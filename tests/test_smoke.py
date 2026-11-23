"""Smoke tests: every module imports and each entry point answers --help, --version or exits clearly."""

import importlib
import subprocess
import sys
import unittest

MODULES = ["schema", "canonical", "limits", "engine", "scheduler", "verify", "workload", "server"]


def run(*args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, timeout=30)


class ImportSmoke(unittest.TestCase):
    def test_each_module_imports_and_has_a_docstring(self):
        for name in MODULES:
            with self.subTest(module=name):
                module = importlib.import_module(f"warehouse_sim.{name}")
                self.assertTrue(module.__doc__)


class EntryPointSmoke(unittest.TestCase):
    def test_version(self):
        result = run("-m", "warehouse_sim", "--version")
        self.assertEqual(result.returncode, 0)
        self.assertIn("warehouse_sim", result.stdout)

    def test_help_names_the_commands(self):
        result = run("-m", "warehouse_sim", "--help")
        self.assertEqual(result.returncode, 0)
        for command in ("run", "serve", "validate", "compare", "scale"):
            self.assertIn(command, result.stdout)

    def test_unbuilt_command_exits_non_zero_with_ticket(self):
        result = run("-m", "warehouse_sim", "run", "x.json", "--out", "y.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not implemented yet: see", result.stderr)

    def test_verify_help_and_unbuilt(self):
        self.assertEqual(run("-m", "warehouse_sim.verify", "--help").returncode, 0)
        result = run("-m", "warehouse_sim.verify", "r.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not implemented yet: see #3", result.stderr)


if __name__ == "__main__":
    unittest.main()
