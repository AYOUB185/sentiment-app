"""Vérifie le livrable du TP Paquet comme le fera le correcteur.

Usage :
    python scripts/verifier_livrable.py

Crée docs/livrable-tp4.txt avec le rapport.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import venv
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
DIST = RACINE / "dist"
DOCS = RACINE / "docs"
RAPPORT = DOCS / "livrable-tp4.txt"
NOM_ROUE = "sentiment_app-1.0.0-py3-none-any.whl"
NOM_SOURCE = "sentiment_app-1.0.0.tar.gz"
AVIS = "Produit cassé et service injoignable, à fuir"

resultats: list[tuple[bool, str, str]] = []


def noter(ok: bool, controle: str, detail: str = "") -> bool:
    resultats.append((ok, controle, detail))
    statut = "[OK]" if ok else "[ECHEC]"
    ligne = f"{statut} {controle}"
    if detail:
        ligne += f" : {detail}"
    print(ligne)
    return ok


def lancer(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """VERIFICATION_LIVRABLE rend les tests du paquet obligatoires."""
    env = {**os.environ, "VERIFICATION_LIVRABLE": "1"}
    return subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def terminer() -> int:
    total = len(resultats)
    echecs = sum(1 for ok, _, _ in resultats if not ok)
    bilan = "CONFORME" if echecs == 0 else f"NON CONFORME ({echecs}/{total} échec(s))"
    print(f"\nBilan : {bilan}")

    DOCS.mkdir(exist_ok=True)
    lignes = []
    for ok, controle, detail in resultats:
        statut = "[OK]" if ok else "[ECHEC]"
        ligne = f"{statut} {controle}"
        if detail:
            ligne += f" : {detail}"
        lignes.append(ligne)
    lignes.append(f"\nBilan : {bilan}")
    RAPPORT.write_text("\n".join(lignes), encoding="utf-8")
    print(f"Rapport : {RAPPORT}")
    return 0 if echecs == 0 else 1


def main() -> int:
    print("=== Vérification du livrable TP Paquet ===\n")

    # 1. Fichiers dans dist/
    roue = DIST / NOM_ROUE
    source = DIST / NOM_SOURCE
    noter(roue.exists(), f"roue présente : {NOM_ROUE}")
    noter(source.exists(), f"distribution source présente : {NOM_SOURCE}")
    autres = [f for f in DIST.iterdir() if f.name not in {NOM_ROUE, NOM_SOURCE}] if DIST.exists() else []
    noter(len(autres) == 0, "aucun autre fichier dans dist/", ", ".join(f.name for f in autres))

    if not roue.exists():
        print("La roue est absente ; arrêt.")
        return terminer()

    # 2. Contenu de la roue
    with zipfile.ZipFile(roue) as z:
        noms = z.namelist()
    noter(
        any("modele/sentiment.joblib" in n for n in noms),
        "modèle embarqué dans la roue",
    )
    noter(
        any("entry_points.txt" in n or "scripts" in n.lower() for n in noms)
        or any("sentiment" in n for n in noms),
        "commande « sentiment » déclarée",
    )
    noter(
        not any("test_" in n for n in noms),
        "pas de tests dans la roue",
    )

    # 3. CHANGELOG et tag Git
    changelog = RACINE / "CHANGELOG.md"
    noter(
        changelog.exists() and "[1.0.0]" in changelog.read_text(encoding="utf-8"),
        "CHANGELOG.md décrit cette version : [1.0.0]",
    )
    r_tag = subprocess.run(
        ["git", "tag", "--points-at", "HEAD"],
        cwd=RACINE,
        capture_output=True,
        text=True,
    )
    tags = r_tag.stdout.strip().splitlines()
    noter("v1.0.0" in tags, "étiquette Git sur le dernier commit : v1.0.0")

    # 4. Installation dans un environnement neuf, hors des sources
    with tempfile.TemporaryDirectory() as tmp:
        dossier = Path(tmp)
        venv.create(dossier / "env", with_pip=True)
        binaires = dossier / "env" / ("Scripts" if sys.platform == "win32" else "bin")
        python = binaires / ("python.exe" if sys.platform == "win32" else "python")

        r = lancer(
            [str(python), "-m", "pip", "install", "-q", str(roue), "pytest"],
            dossier,
        )
        last_err = (r.stderr.strip().splitlines() or [""])[-1] if r.returncode else ""
        if not noter(r.returncode == 0, "installation de la roue dans un environnement neuf", last_err):
            return terminer()

        r = lancer(
            [
                str(python), "-m", "pytest", "-q", "-p", "no:cacheprovider",
                str(RACINE / "tests" / "test_paquet.py"),
            ],
            dossier,
        )
        bilan_ligne = (r.stdout.strip().splitlines() or ["(aucune sortie)"])[-1]
        noter(
            r.returncode == 0 and "skipped" not in bilan_ligne,
            "tests lancés sur le paquet installé",
            bilan_ligne,
        )

        commande = binaires / ("sentiment.exe" if sys.platform == "win32" else "sentiment")
        r = lancer([str(commande), "--json", AVIS], dossier)
        erreur = (r.stderr.strip().splitlines() or [""])[-1]
        noter(
            r.returncode == 0 and '"label"' in r.stdout,
            "commande installée",
            r.stdout.strip() or erreur,
        )

    return terminer()


if __name__ == "__main__":
    sys.exit(main())

