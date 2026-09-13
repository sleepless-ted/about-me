from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urljoin, urlparse

from django.contrib.staticfiles import finders
from django.core.management import call_command
from django.test import SimpleTestCase, override_settings
from django.urls import reverse


@override_settings(
    SECURE_SSL_REDIRECT=False,
    STORAGES={
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}
    },
)
class ShowcaseTests(SimpleTestCase):
    def test_homepage_renders_without_database_and_static_assets_exist(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Ted Dousset")
        self.assertContains(response, 'lang="fr"')
        self.assertContains(response, 'href="https://www.malt.fr/profile/tedd"')
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "pages/home.html")
        for asset in ["styles.css", "main.js", "assets/ted-dousset.png", "assets/favicon.svg"]:
            with self.subTest(asset=asset):
                self.assertIsNotNone(finders.find(f"vitrine/{asset}"))
                self.assertContains(response, f"/static/vitrine/{asset}")

    def test_unknown_route_is_not_a_fake_homepage(self):
        self.assertEqual(self.client.get("/missing-page/").status_code, 404)

    @override_settings(SECURE_SSL_REDIRECT=True)
    def test_production_redirects_http_to_https(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "https://testserver/")


class StaticExportTests(SimpleTestCase):
    def test_export_has_resolvable_assets_at_root_and_repository_subpath(self):
        class Resources(HTMLParser):
            def __init__(self):
                super().__init__()
                self.urls = []

            def handle_starttag(self, tag, attrs):
                if tag in {"link", "script", "img"}:
                    self.urls.extend(value for key, value in attrs if key in {"src", "href"})

        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            with override_settings(BASE_DIR=root):
                call_command("export_site", verbosity=0)
                # Rebuilding must remove stale generated files.
                (root / "dist" / "obsolete.txt").write_text("old output")
                call_command("export_site", verbosity=0)
            output = root / "dist"
            html = (output / "index.html").read_text()
            self.assertIn("Ted Dousset", html)
            self.assertNotIn("{%", html)
            self.assertTrue((output / ".nojekyll").exists())
            self.assertFalse((output / "obsolete.txt").exists())
            self.assertFalse(list(output.rglob("*.py")))
            parser = Resources()
            parser.feed(html)
            self.assertEqual(len(parser.urls), 4)
            for base in ("https://example.com/", "https://example.com/site-vitrine/"):
                for resource in parser.urls:
                    with self.subTest(base=base, resource=resource):
                        self.assertTrue(resource.startswith("./static/"))
                        resolved = urlparse(urljoin(base, resource)).path
                        prefix = urlparse(base).path
                        self.assertTrue(resolved.startswith(prefix))
                        self.assertTrue((output / resolved[len(prefix):]).is_file())
