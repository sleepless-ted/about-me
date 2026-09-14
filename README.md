# Ted Dousset — Vitrine Django publiée sur GitHub Pages

Vitrine française : présentation, offres, expérience, approche et contact via Malt. Django 5.2 LTS, templates Django, CSS et JavaScript natifs. Pas de frontend à compiler, de base de données, de traceur ni de formulaire factice. Django génère les pages et leurs fichiers statiques ; GitHub Pages héberge le résultat sans serveur Python. Le portrait et les ressources sont inclus dans le site.

## Lancer avec Pixi

```sh
pixi install
pixi run dev
```

Ouvrir http://127.0.0.1:8000. Python 3.12 et les dépendances sont isolés dans `.pixi/`, avec leurs versions verrouillées dans `pixi.lock`.

```sh
pixi run check
pixi run test
```

## Lancer avec un environnement Python classique

Avec Python 3.12 :

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DJANGO_DEBUG=1 python manage.py runserver
```

## Organisation

- `config/` : paramètres Django, URL et application WSGI.
- `templates/base.html` : métadonnées, navigation et pied de page.
- `templates/pages/home.html` : contenu de la vitrine.
- `static/vitrine/` : CSS, JavaScript et portrait.
- `pages/management/commands/export_site.py` : export HTML et fichiers statiques versionnés.
- `.github/workflows/pages.yml` : validation, génération et publication sur GitHub Pages.
- `pages/tests.py` : rendu, ressources, export à la racine ou dans un sous-répertoire et paramètres Django.

Le menu mobile est la seule interaction JavaScript nécessaire à la navigation compacte ; les liens restent disponibles si JavaScript est désactivé. Les mouvements respectent la préférence de réduction des animations.

## Dépôt et site public

Les sources de cette vitrine sont dans `sleepless-ted/about-me`. L’ancien dépôt de présentation est conservé dans [About-me-archive](https://github.com/sleepless-ted/About-me-archive), avec son historique.

Dépôt public : https://github.com/sleepless-ted/about-me

Site : https://sleepless-ted.github.io/about-me/

GitHub Pages est activé avec GitHub Actions. Chaque push sur `main` déclenche la publication.

## Générer et prévisualiser la version GitHub Pages

```sh
pixi run build
pixi run preview
```

L’export est dans `dist/`, ignoré par Git. L’aperçu statique est accessible sur http://127.0.0.1:8001. Refaire `pixi run build` après les modifications, puis recharger le navigateur. Les fichiers de `dist/` sont entièrement régénérés à chaque export.

Sans Pixi : `DJANGO_DEBUG=1 python manage.py export_site`, puis `python -m http.server 8001 --bind 127.0.0.1 --directory dist`.

Le HTML exporté utilise des ressources relatives et versionnées. Il fonctionne sous `/about-me/` comme à la racine d’un domaine personnalisé. Seuls le HTML et les fichiers statiques sont publiés, aucun serveur Django, paramètre privé ou fichier Python.

## Publier sur GitHub Pages

1. Ouvrir https://github.com/sleepless-ted/about-me/settings/pages.
2. Dans **Build and deployment → Source**, sélectionner **GitHub Actions**.
3. Ouvrir **Actions → Publish showcase to GitHub Pages → Run workflow**, sélectionner `main`, puis lancer le workflow.
4. Attendre que les étapes `build` et `deploy` soient vertes. Le lien du site apparaît dans le résultat du déploiement.

Le premier workflow déclenché par le push peut échouer à l’étape de configuration si Pages n’est pas encore activé : l’activer puis relancer le workflow suffit.

Le workflow vérifie le projet, lance les tests, exporte le site dans `dist/` et publie uniquement cet export. Il se relance ensuite à chaque push sur `main` et peut être déclenché manuellement.

Sans domaine personnalisé, l’adresse du site est `https://sleepless-ted.github.io/about-me/`. Un domaine acheté ensuite pourra être ajouté dans les paramètres Pages et les DNS du registrar. Aucun domaine n’est configuré d’avance.

Django reste l’outil de développement et de génération. Ses fonctionnalités serveur (base de données, admin, formulaire traité en Python) ne sont pas exécutées sur GitHub Pages ; le contact Malt fonctionne comme auparavant. Aucun service du VPS n’est modifié.

Références :
- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Sources et choix éditoriaux

- Informations, préférences et captures fournies par Ted, le 13 septembre 2026.
- Profil public : https://www.malt.fr/profile/tedd
- README consulté (dépôt renommé) : https://github.com/sleepless-ted/About-me-archive/blob/main/README.md
- Références graphiques : https://clad3815.dev/ et https://alfouille.blackshield-intel.fr/ ; aucun code repris.
- Portrait public Malt : https://dam.malt.com/2b22b8e1-dea5-4c79-a571-eaab8db6fa8d?face_margin=70&force_format=webp&func=face&gravity=face&h=360&w=360
- Django : https://www.djangoproject.com/download/

Les dates EDF suivent la capture fournie (avril–octobre 2021), car la page Malt indexée présentait des dates différentes. Le tarif de 550 €/jour reste indicatif. Les durées d’audit et de prototypage dépendent du périmètre. Aucune performance chiffrée de projet, recommandation client, adresse e-mail ou disponibilité immédiate n’a été inventée.
