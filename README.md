# Studien-Dashboard

Python-basiertes, mehrbenutzerfähiges Dashboard zur Verwaltung von Semestern, Modulen, Prüfungsleistungen 
sowie zur Berechnung von ECTS-Fortschritt und Notendurchschnitt.

## Installation

1. Repository klonen: "git clone https://github.com/PraetorianGuardx/Studien-Dashboard.git"
2. Abhängigkeiten installieren: "pip install -r requirements.txt"
3. Programm starten: "python application.py"

Alternativ steht "dist/application.exe" als eigenständig ausführbare Version zur Verfügung (kein Python nötig).

## Architektur

Das Projekt folgt einem Schichtenmodell: Domain -> Repository -> Service -> Controller -> View -> Application.
Details dazu im Reflexions- und Entwurfsdokument (Phase 2) des zugehörigen Projekts.
Verwendete Quellen befinden sich im "quellen.md".