from repositories import BenutzerkontoRepository

class FortschrittService:
    """Die Fortschrittsdaten eines Studenten, aufbereitet für die Anzeige."""
    # Die Service-Schicht liegt zwischen Controller und Repository, damit der Controller nicht wissen muss, wie ECTS und Notendurchschnitt berechnet werden
    def __init__(self, konto_repository: BenutzerkontoRepository):
        # Die Typangabe verweist bewusst auf die abstrakte Klasse und nicht auf JSONBenutzerkontoRepository, dadurch arbeitet der Service mit jeder Umsetzung des Repositories
        self.konto_repository = konto_repository

    def fortschritt_anzeigen(self, benutzername):
        """Die Fortschrittsdaten werden als Dictionary zurückgegeben, sonst None."""
        konto = self.konto_repository.laden(benutzername)
        # Ohne Konto gibt es nichts zu berechnen, die View gibt in diesem Fall dann eine Meldung aus
        if konto is None:
            return None
        student = konto.student

        ects_erreicht = 0
        for belegung in student.belegungen:
            ects_erreicht += belegung.ects_erreicht_berechnen()

        # Die Gesamt-ECTS kommen aus dem Studiengang der ersten Belegung, damit die View den Fortschritt ins Verhältnis setzen kann
        ects_gesamt = 0
        if len(student.belegungen) > 0:
            ects_gesamt = student.belegungen[0].studiengang.ects_gesamt

        # Der Notendurchschnitt stammt aus der ersten Belegung, weil die Anwendung pro Student genau eine anlegt
        # Mehrere Belegungen ließen sich nicht einfach zu einem Wert verrechnen, da jede intern bereits nach ECTS gewichtet rechnet und die Zwischensumme dafür nicht zugänglich ist
        notendurchschnitt = None
        if len(student.belegungen) > 0:
            notendurchschnitt = student.belegungen[0].notendurchschnitt_berechnen()

        # Bewusst als Dictionary gewählt statt des Studentenobjekts, damit die View die Domänenklassen nicht kennen muss und nur noch Werte ausliest
        fortschritt = {
            "vorname": student.vorname,
            "nachname": student.nachname,
            "zielnote": student.zielnote,
            "regelstudienzeit": student.regelstudienzeit,
            "ects_erreicht": ects_erreicht,
            "ects_gesamt": ects_gesamt,
            "notendurchschnitt": notendurchschnitt
        }
        return fortschritt
