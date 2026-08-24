class Studiengang:                              # Bauplan für einen Studiengang
    def __init__(self, name, ects_gesamt):      # initialisiert einen Studiengang mit einem Namen und einer leeren Liste von Semestern
        self.name = name                        # speichert den Namen des Studiengangs
        self.ects_gesamt = ects_gesamt          # speichert die Gesamtzahl der ECTS-Punkte des Studiengangs
        self.semester = []                      # leere Liste, die die Semester des Studiengangs speichert

    def add_semester(self, semester):           # fügt ein Semester zur Liste der Semester des Studiengangs hinzu
        self.semester.append(semester)          # hängt das Semester an die Liste der Semester des Studiengangs an

    def berechne_fortschritt(self):                                                             # berechnet den Fortschritt des Studiengangs in Prozent
        ects_erreicht = 0                                                                       # initialisiert die erreichten ECTS-Punkte mit 0
        for semester in self.semester:                                                          # iteriert über alle Semester des Studiengangs
            for modul in semester.module:                                                       # iteriert über alle Module des Semesters
                if modul.status == "bestanden":                                                 # prüft, ob das Modul bestanden wurde
                    ects_erreicht += modul.ects                                                 # addiert die ECTS-Punkte des Moduls zu den erreichten ECTS-Punkten
        if self.ects_gesamt > 0:                                                                # prüft, ob die Gesamtzahl der ECTS-Punkte größer als 0 ist
            fortschritt = (ects_erreicht / self.ects_gesamt) * 100                              # berechnet den Fortschritt in Prozent
        else:
            fortschritt = 0                                                                     # setzt den Fortschritt auf 0, wenn die Gesamtzahl der ECTS-Punkte 0 ist

        return round(fortschritt, 1)                                                            # gibt den Fortschritt in Prozent zurück