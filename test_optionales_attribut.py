class Pruefungsleistung:                        # Bauplan für eine Prüfungsleistung
    def __init__(self, titel, datum):           # initialisiert eine Prüfungsleistung mit einem Modul und einer Note
        self.titel = titel                      # speichert den Titel der Prüfungsleistung
        self.datum = datum                      # speichert das Datum der Prüfungsleistung
        self.note = None                        # speichert die Note der Prüfungsleistung (initialisiert mit None, da die Note noch nicht bekannt ist)

    @property
    def note(self):                             # Getter-Methode für die Note der Prüfungsleistung
        return self._note                       # gibt die Note der Prüfungsleistung zurück

    @note.setter
    def note(self, wert):                                                   # Setter-Methode für die Note der Prüfungsleistung
        if wert is not None and (wert < 1.0 or wert > 5.0):                 # überprüft, ob die Note im gültigen Bereich liegt (1.0 bis 5.0)
            raise ValueError("Die Note muss zwischen 1.0 und 5.0 liegen.")  # wirft eine Fehlermeldung, wenn die Note ungültig ist
        self._note = wert                                                   # speichert die Note der Prüfungsleistung

# Quelle: https://www.youtube.com/watch?v=HkbQ_NaH0Lc