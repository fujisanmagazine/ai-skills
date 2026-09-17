import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location(
    "fetch_apidoc",
    pathlib.Path(__file__).resolve().parent.parent / "skill" / "scripts" / "fetch_apidoc.py",
)
fetch_apidoc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetch_apidoc)
canonical_path = fetch_apidoc.canonical_path

ACCEPTED = {
    "/": "/",
    "/api-index.json": "/api-index.json",
    "/apis/catalog-api": "/apis/catalog-api/",
    "/apis/catalog-api/": "/apis/catalog-api/",
    "/apis/mccp-payment-api/backend-api": "/apis/mccp-payment-api/backend-api/",
    "/docs/product-graphql-api": "/docs/product-graphql-api/",
    "/redocusaurus/catalog-api.yaml": "/redocusaurus/catalog-api.yaml",
}

REJECTED = [
    "/apis/../secret",
    "/apis/..",
    "/apis/.",
    "/../etc/passwd",
    "//apis//x",
    "apis/catalog-api",
    "/not-allowed",
    "/apis",
    "/docs",
    "/redocusaurus/x",
    "/redocusaurus/a/b.yaml",
    "/apis/name with spaces",
    "",
]


class CanonicalPath(unittest.TestCase):
    def test_accepted_paths_map_to_the_path_the_host_actually_serves(self):
        for given, expected in ACCEPTED.items():
            with self.subTest(given):
                self.assertEqual(canonical_path(given), expected)

    def test_rejected_paths_return_none(self):
        for given in REJECTED:
            with self.subTest(given):
                self.assertIsNone(canonical_path(given))

    def test_canonicalising_an_already_canonical_path_changes_nothing(self):
        for expected in ACCEPTED.values():
            with self.subTest(expected):
                self.assertEqual(canonical_path(expected), expected)


if __name__ == "__main__":
    unittest.main()
