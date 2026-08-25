class Studiengang:                              # Bauplan für einen Studiengang
    def __init__(self, name, ects_gesamt):      # initialisiert einen Studiengang mit einem Namen
        self.name = name                        # speichert den Namen des Studiengangs
        self.ects_gesamt = ects_gesamt          # speichert die Gesamtzahl der ECTS-Punkte des Studiengangs

class Belegung:                                 # Bauplan für eine Belegung
    def __init__(self, startdatum):             # initialisiert eine Belegung mit einem Startdatum und einer leeren Liste von Semestern
        self.startdatum = startdatum            # speichert das Startdatum der Belegung
        self.semester = []                      # leere Liste, die die Semester der Belegung speichert

    def semester_hinzufuegen(self, semester):   # fügt ein Semester zur Liste der Semester der Belegung hinzu
        self.semester.append(semester)          # hängt das Semester an die Liste der Semester der Belegung an

    def ects_erreicht_berechnen(self):                          # berechnet die erreichten ECTS-Punkte der Belegung
        ects_erreicht = 0                                       # initialisiert die erreichten ECTS-Punkte mit 0
        for semester in self.semester:                          # iteriert über alle Semester der Belegung
            for modul in semester.module:                       # iteriert über alle Module des Semesters
                if modul.status == Modulstatus.ABGESCHLOSSEN:   # überprüft, ob das Modul abgeschlossen ist
                    ects_erreicht += modul.ects                 # addiert die ECTS-Punkte des Moduls zu den erreichten ECTS-Punkten
        return ects_erreicht                                    # gibt die erreichten ECTS-Punkte zurück

    def notendurchschnitt_berechnen(self):                      # berechnet den Notendurchschnitt der Belegung
        summe_noten = 0                                         # initialisiert die Summe der Noten mit 0
        summe_ects = 0                                          # initialisiert die Summe der ECTS-Punkte mit 0
        for semester in self.semester:                          # iteriert über alle Semester der Belegung
            for modul in semester.module:                       # iteriert über alle Module des Semesters
                if modul.status == Modulstatus.ABGESCHLOSSEN:   # überprüft, ob das Modul abgeschlossen ist
                    modulnote = modul.modulnote_berechnen()     # berechnet die Modulnote des Moduls
                    if modulnote is not None:                   # überprüft, ob die Modulnote nicht None ist
                        summe_noten += modulnote * modul.ects   # addiert die Modulnote multipliziert mit den ECTS-Punkten des Moduls zur Summe der Noten
                        summe_ects += modul.ects                # addiert die ECTS-Punkte des Moduls zur Summe der ECTS-Punkte
        if summe_ects > 0:                                      # überprüft, ob die Summe der ECTS-Punkte größer als 0 ist
            return summe_noten / summe_ects                     # gibt den gewichteten Notendurchschnitt zurück
        else:
            return None                                         # gibt None zurück, wenn keine bewerteten Module vorhanden sind

class Modul:
    def __init__(self, name, status, ects):     # initialisiert ein Modul mit einem Namen, einem Status und einer Anzahl von ECTS-Punkten
        self.name = name                        # speichert den Namen des Moduls
        self.status = status                    # speichert den Status des Moduls (bestanden, nicht bestanden, in Bearbeitung)
        self.ects = ects                        # speichert die ECTS-Punkte des Moduls
        self.pruefungsleistungen = []           # leere Liste, die die Prüfungsleistungen des Moduls speichert

    def pruefungsleistung_hinzufuegen(self, pruefungsleistung): # fügt eine Prüfungsleistung zum Modul hinzu
        self.pruefungsleistungen.append(pruefungsleistung)      # hängt die Prüfungsleistungen an die Liste der Prüfungsleistungen des Moduls an

    def modulnote_berechnen(self):                              # berechnet die Modulnote des Moduls
        summe_noten = 0                                         # initialisiert die Summe der Noten mit 0
        anzahl_bewertet = 0                                     # initialisiert die Anzahl der bewerteten Prüfungsleistungen mit 0
        for pruefungsleistung in self.pruefungsleistungen:      # iteriert über alle Prüfungsleistungen des Moduls
            if pruefungsleistung.note is not None:              # überprüft, ob die Prüfungsleistung eine Note hat
                summe_noten += pruefungsleistung.note           # addiert die Note der Prüfungsleistung zur Summe der Noten
                anzahl_bewertet += 1                            # erhöht die Anzahl der bewerteten Prüfungsleistungen um 1
        if anzahl_bewertet > 0:
            return summe_noten / anzahl_bewertet                # gibt die durchschnittliche Modulnote zurück
        else:
            return None                                         # gibt None zurück, wenn keine bewerteten Prüfungsleistungen vorhanden sind

mathe = Modul("Mathematik", Modulstatus.ABGESCHLOSSEN, 5)
klausur_mathe = Pruefungsleistung("Klausur Mathe", "01.06.2024")
klausur_mathe.note = 1.0
mathe.pruefungsleistung_hinzufuegen(klausur_mathe)

security = Modul("Security", Modulstatus.ABGESCHLOSSEN, 10)
klausur_security = Pruefungsleistung("Klausur Security", "15.06.2024")
klausur_security.note = 3.0
security.pruefungsleistung_hinzufuegen(klausur_security)

sem1 = Semester(1)
sem1.modul_hinzufuegen(mathe)
sem1.modul_hinzufuegen(security)

belegung = Belegung("01.10.2024")
belegung.semester_hinzufuegen(sem1)

print(belegung.notendurchschnitt_berechnen())