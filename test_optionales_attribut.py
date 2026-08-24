class Pruefungsleistung:                        # Bauplan für eine Prüfungsleistung
    def __init__(self, titel, datum):           # initialisiert eine Prüfungsleistung mit einem Modul und einer Note
        self.titel = titel                      # speichert den Titel der Prüfungsleistung
        self.datum = datum                      # speichert das Datum der Prüfungsleistung
        self.note = None                        # speichert die Note der Prüfungsleistung (initialisiert mit None, da die Note noch nicht bekannt ist)

    def bewerten(self, neue_note):              # bewertet die Prüfungsleistung mit einer Note
        self.note = neue_note                   # speichert die Note der Prüfungsleistung