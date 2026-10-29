# README de profil — Alexandre Bredillot

## Profil GitHub

Ce README est publié dans le dépôt public [McJack3d/McJack3d](https://github.com/McJack3d/McJack3d) et s'affiche sur le [profil McJack3d](https://github.com/McJack3d). Le visuel s'adapte au thème clair ou sombre de GitHub.

Pour relancer une actualisation, ouvre **Actions → Refresh profile stats → Run workflow**. Le dépôt `CFG_McJack3d` est conservé séparément.

Les exigences officielles sont décrites dans [la documentation GitHub](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).

## Personnalisation

- `data/profile.json` : poste, technologies, centres d'intérêt et coordonnées.
- `data/portrait.txt` : portrait en caractères ASCII, issu de la photo fournie.
- `data/stats.json` : photographie des statistiques publiques GitHub.
- `scripts/render_profile.py` : génération des deux SVG avec Python 3, sans dépendance.
- `scripts/update_stats.py` : actualisation des statistiques depuis l'API publique GitHub.

Après avoir modifié le profil ou le portrait, lance :

```sh
python3 scripts/render_profile.py
```

Pour actualiser les statistiques et les visuels localement :

```sh
python3 scripts/update_stats.py
python3 scripts/render_profile.py
```

Le workflow `.github/workflows/update-profile.yml` réalise ces deux opérations chaque jour à 05:23 UTC, ou manuellement. Il utilise le jeton fourni par GitHub Actions ; aucun jeton personnel à créer. Le dépôt doit autoriser le workflow à pousser son commit sur la branche par défaut. Les règles de protection de branche peuvent empêcher ce push.

Les SVG déjà livrés fonctionnent sans activer le workflow. Le poste et la biographie restent modifiables manuellement ; seules les statistiques sont actualisées automatiquement.

## Sens des statistiques

- **Repos.Public** : nombre de dépôts publics du compte, forks compris.
- **Stars** : somme des étoiles reçues par les dépôts publics possédés par le compte, hors forks.
- **Followers** : nombre d'abonnés au compte.
- **Since** : année de création du compte GitHub.
- **Updated.UTC** : date de la dernière collecte réussie, en UTC.

Les dépôts privés, les commits et les lignes de code ne sont pas comptabilisés dans cette version.

## Sources

Le style terminal et le principe des versions claire/sombre sont inspirés du [profil d'Andrew Grant](https://github.com/Andrew6rant/Andrew6rant). Le code de génération a été écrit pour ce profil.

Les informations personnelles ont été reprises du [portfolio public](https://mcjack3d.github.io/) et du [README public existant](https://github.com/McJack3d/CFG_McJack3d), consultés le 29 octobre 2026. Le portrait provient de `IMG_0580.heic` fourni pour cette demande. La photo originale n'est pas nécessaire au fonctionnement du README.
