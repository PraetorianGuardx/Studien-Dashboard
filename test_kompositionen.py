class Modul:                                    # Bauplan für ein Modul
    def __init__(self, name, status, ects):     # initialisiert ein Modul mit einem Namen, einem Status und einer Anzahl von ECTS-Punkten
        self.name = name                        # speichert den Namen des Moduls
        self.status = status                    # speichert den Status des Moduls (bestanden, nicht bestanden, in Bearbeitung)
        self.ects = ects                        # speichert die ECTS-Punkte des Moduls

class Semester:                                 # Bauplan für ein Semester
    def __init__(self, nummer):                 # initialisiert ein Semester mit einer Nummer und einer leeren Liste von Modulen
        self.semester_nummer = nummer           # speichert die Nummer des Semesters
        self.module = []                        # leere Liste, die die Module des Semesters speichert

    def add_modul(self, modul):                 # fügt ein Modul zur Liste der Module des Semesters hinzu
        self.module.append(modul)               # hängt das Modul an die Liste der Module des Semesters an


# Quelle: https://www.youtube.com/watch?v=yYALsys-P_w
# Quelle: https://www.youtube.com/watch?v=JeznW_7DlB0&t
# Quelle: https://www.youtube.com/watch?v=rLyYb7BFgQI