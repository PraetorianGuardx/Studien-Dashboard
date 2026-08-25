from repositories import StudentRepository

class FortschrittService:
    def __init__(self, repository: StudentRepository):                              # Initialisiert den FortschrittService mit einem StudentRepository
        self.repository = repository

    def fortschritt_anzeigen(self, benutzername):                                   # Zeigt den Fortschritt eines Studenten an
        student = self.repository.laden(benutzername)                               # Lädt den Studenten aus dem Repository
        if student is None:                                                         # Überprüft, ob der Student existiert
            return None                                                             # Gibt None zurück, wenn der Student nicht existiert

        ects_erreicht = 0                                                           # Initialisiert die erreichten ECTS-Punkte mit 0
        for belegung in student.belegungen:                                         # Iteriert über alle Belegungen des Studenten
            ects_erreicht += belegung.ects_erreicht_berechnen()                     # Addiert die erreichten ECTS-Punkte der Belegung zu den erreichten ECTS-Punkten

        notendurchschnitt = None
        if len(student.belegungen) > 0:                                             # Überprüft, ob der Student Belegungen hat
            notendurchschnitt = student.belegungen[0].notendurchschnitt_berechnen() # Berechnet den Notendurchschnitt der letzten Belegung

        fortschritt = {
            "vorname": student.vorname,                                             # Speichert den Vornamen des Studenten
            "nachname": student.nachname,                                           # Speichert den Nachnamen des Studenten  
            "zielnote": student.zielnote,                                           # Speichert die Zielnote des Studenten
            "regelstudienzeit": student.regelstudienzeit,                           # Speichert die Regelstudienzeit des Studenten
            "ects_erreicht": ects_erreicht,                                         # Speichert die erreichten ECTS-Punkte des Studenten
            "notendurchschnitt": notendurchschnitt                                  # Speichert den Notendurchschnitt des Studenten
        }
        return fortschritt                                                          # Gibt den Fortschritt des Studenten zurück