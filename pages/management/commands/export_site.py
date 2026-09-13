"""Render the Django showcase into a standalone GitHub Pages artifact."""

import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from django.conf import settings
from django.core.management import BaseCommand, CommandError, call_command
from django.template.loader import render_to_string
from django.test.utils import override_settings


class Command(BaseCommand):
    help = "Génère la vitrine statique dans dist/ pour GitHub Pages."

    def handle(self, *args, **options):
        output = settings.BASE_DIR / "dist"
        if output.is_symlink():
            raise CommandError("dist/ doit être un dossier local, pas un lien symbolique.")

        # Build completely before replacing the previous generated artifact.
        with TemporaryDirectory(prefix="site-vitrine-export-") as temporary:
            staging = Path(temporary)
            with override_settings(
                DEBUG=False,
                STATIC_URL="/static/",
                STATIC_ROOT=staging / "static",
                STORAGES={
                    "staticfiles": {
                        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
                    }
                },
            ):
                call_command("collectstatic", interactive=False, verbosity=0)
                html = render_to_string("pages/home.html")

            # Relative URLs work at /site-vitrine/ and at a custom domain root.
            html = html.replace('"/static/', '"./static/')
            (staging / "index.html").write_text(html, encoding="utf-8")
            (staging / ".nojekyll").touch()
            if output.exists():
                shutil.rmtree(output)
            shutil.copytree(staging, output)

        self.stdout.write(self.style.SUCCESS(f"Site statique prêt : {output}"))
