from repositories import BenutzerkontoRepository

class FortschrittService:
    def __init__(self, konto_repository: BenutzerkontoRepository):                          # Initialisiert den FortschrittService mit einem BenutzerkontoRepository
        self.konto_repository = konto_repository                                            # Speichert das BenutzerkontoRepository als Attribut des FortschrittService

    def fortschritt_anzeigen(self, benutzername):                                           # Zeigt den Fortschritt eines Studenten an
        konto = self.konto_repository.laden(benutzername)                                   # Lädt das Benutzerkonto des Studenten anhand des Benutzernamens
        if konto is None:                                                                   # Überprüft, ob das Benutzerkonto existiert
            return None                                                                     # Gibt None zurück, wenn das Benutzerkonto nicht existiert
        student = konto.student                                                             # Holt das Studentenobjekt aus dem Benutzerkonto

        ects_erreicht = 0                                                                   # Initialisiert die erreichten ECTS-Punkte mit 0
        for belegung in student.belegungen:                                                 # Iteriert über alle Belegungen des Studenten
            ects_erreicht += belegung.ects_erreicht_berechnen()                             # Addiert die erreichten ECTS-Punkte der Belegung zu den erreichten ECTS-Punkten

        notendurchschnitt = None
        if len(student.belegungen) > 0:                                                     # Überprüft, ob der Student Belegungen hat
            notendurchschnitt = student.belegungen[0].notendurchschnitt_berechnen()         # Berechnet den Notendurchschnitt der ersten Belegung des Studenten

        fortschritt = {
            "vorname": student.vorname,                                                     # Speichert den Vornamen des Studenten
            "nachname": student.nachname,                                                   # Speichert den Nachnamen des Studenten  
            "zielnote": student.zielnote,                                                   # Speichert die Zielnote des Studenten
            "regelstudienzeit": student.regelstudienzeit,                                   # Speichert die Regelstudienzeit des Studenten
            "ects_erreicht": ects_erreicht,                                                 # Speichert die erreichten ECTS-Punkte des Studenten
            "notendurchschnitt": notendurchschnitt                                          # Speichert den Notendurchschnitt des Studenten
        }
        return fortschritt                                                                  # Gibt den Fortschritt des Studenten zurück