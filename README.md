# ChatterieSync Backend

Prototype d'API FastAPI pour la gestion locale d'une chatterie de Maine Coons en Belgique.

## Fonctionnalités incluses

- Gestion des chats (profils complets, génétique, santé, mesures).
- Suivi des portées et chatons (journal de poids, statuts, mise à jour des informations).
- CRM familles adoptantes (leads, interactions, réservations, suivis post-adoption).
- Conformité & documents (rappels légaux paramétrables, pièces jointes).
- Export ZIP d'un chat ou d'une portée (métadonnées JSON + fichiers joints).

## Démarrage rapide

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

L'API est disponible sur `http://127.0.0.1:8000` et la documentation interactive sur `http://127.0.0.1:8000/docs`.

## Structure

```
backend/
  app/
    main.py            # Application FastAPI et exports ZIP
    database.py        # Initialisation SQLite locale
    models.py          # Modèles SQLModel couvrant l'élevage
    schemas.py         # Schémas Pydantic pour I/O
    routers/           # Routes modulaires (chats, portées, leads, conformité)
  requirements.txt     # Dépendances Python
```

La base de données SQLite est stockée dans `data/chatterie.db` (créée automatiquement).

## Étapes suivantes possibles

- Calcul automatique du COI via import de pedigree.
- Génération de PDF (contrats, fiches) depuis des modèles.
- Synchronisation Drive (Google/Nextcloud) pour les pièces jointes.
- Tableaux de bord (statistiques santé, reproduction, adoption).
- Interface front-end locale (Electron/Tauri ou PWA) alimentée par cette API.
