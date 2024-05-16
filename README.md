# Outil de Conversion de PDF en TIFF

## Vue d'ensemble

Ce projet fournit une application avec une interface graphique (GUI) pour convertir des fichiers PDF en format TIFF. L'application est construite en utilisant Python et plusieurs bibliothèques telles que `tkinter` pour l'interface utilisateur, `PyMuPDF` (aussi connu sous le nom de `fitz`) pour la gestion des fichiers PDF, et `Pillow` pour le traitement d'images.

## Fonctionnalités

- Sélectionner un dossier contenant des fichiers PDF.
- Afficher le nombre de fichiers PDF dans le dossier sélectionné.
- Convertir tous les fichiers PDF ou des fichiers PDF sélectionnés du dossier en format TIFF.
- Afficher les détails des fichiers PDF (nom, date de modification, taille).
- Sélectionner tous les fichiers PDF ou les désélectionner d'un seul clic.
- Afficher des messages d'information ou d'erreur après la conversion.

## Prérequis

- Python 3.x
- Bibliothèques Python: `tkinter`, `PyMuPDF`, `Pillow`

## Installation

1. Clonez ce dépôt Git sur votre machine locale:
    ```bash
    git clone https://github.com/votre-utilisateur/pdf-to-tiff.git
    ```

2. Accédez au répertoire du projet:
    ```bash
    cd pdf-to-tiff
    ```

3. Installez les dépendances requises:
    ```bash
    pip install pymupdf Pillow
    ```

## Utilisation

1. Exécutez le script principal:
    ```bash
    python main.py
    ```

2. Utilisez l'application pour sélectionner un dossier contenant des fichiers PDF.

3. Cliquez sur "Sélectionner les fichiers PDF" pour choisir les fichiers PDF à convertir.

4. Cliquez sur "Lancer la conversion" pour convertir les fichiers sélectionnés en format TIFF.

## Structure du Projet

- `main.py`: Contient le code principal de l'application.
- `logo.png`: Image du logo affichée dans l'interface utilisateur.
- `README.md`: Ce fichier, qui fournit des informations sur le projet.

## Auteurs

- Nicolas (https://github.dev/NVA-1986)