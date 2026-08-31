from enum import Enum

class Modulstatus(Enum):                        # Enum-Klasse für den Status eines Moduls
    BEVORSTEHEND = "bevorstehend"               # Status: Modul bevorstehend
    AKTUELL = "aktuell"                         # Status: Modul aktuell
    ABGESCHLOSSEN = "abgeschlossen"             # Status: Modul abgeschlossen

class Pruefungsleistung:                        # Bauplan für eine Prüfungsleistung
    def __init__(self, titel, datum):           # initialisiert eine Prüfungsleistung mit einem Titel, einem Datum und einer Note (initialisiert mit None)
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

class Semester:                                     # Bauplan für ein Semester
    def __init__(self, nummer):                     # initialisiert ein Semester mit einer Nummer und einer leeren Liste von Modulen
        self.semester_nummer = nummer               # speichert die Nummer des Semesters
        self.module = []                            # leere Liste, die die Module des Semesters speichert

    def modul_hinzufuegen(self, modul):             # fügt ein Modul zur Liste der Module des Semesters hinzu
        self.module.append(modul)                   # hängt das Modul an die Liste der Module des Semesters an

class Studiengang:                                  # Bauplan für einen Studiengang
    def __init__(self, name, ects_gesamt):          # initialisiert einen Studiengang mit einem Namen
        self.name = name                            # speichert den Namen des Studiengangs
        self.ects_gesamt = ects_gesamt              # speichert die Gesamtzahl der ECTS-Punkte des Studiengangs

class Belegung:                                     # Bauplan für eine Belegung
    def __init__(self, startdatum, studiengang):    # initialisiert eine Belegung mit einem Startdatum und einer leeren Liste von Semestern
        self.startdatum = startdatum                # speichert das Startdatum der Belegung
        self.studiengang = studiengang              # speichert den Studiengang der Belegung
        self.semester = []                          # leere Liste, die die Semester der Belegung speichert

    def semester_hinzufuegen(self, semester):       # fügt ein Semester zur Liste der Semester der Belegung hinzu
        self.semester.append(semester)              # hängt das Semester an die Liste der Semester der Belegung an

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

class Student:                                                          # Bauplan für einen Studenten
    def __init__(self, vorname, nachname, zielnote, regelstudienzeit):  # initialisiert einen Studenten mit einem Vornamen, Nachnamen, Zielnote und Regelstudienzeit
        self.vorname = vorname                                          # speichert den Vornamen des Studenten
        self.nachname = nachname                                        # speichert den Nachnamen des Studenten
        self.zielnote = zielnote                                        # speichert die Zielnote des Studenten
        self.regelstudienzeit = regelstudienzeit                        # speichert die Regelstudienzeit des Studenten
        self.belegungen = []                                            # leere Liste, die die Belegungen des Studenten speichert

    def belegung_hinzufuegen(self, belegung):                           # fügt eine Belegung zur Liste der Belegungen des Studenten hinzu
        self.belegungen.append(belegung)                                # hängt die Belegung an die Liste der Belegungen des Studenten an

# Quelle: https://www.youtube.com/watch?v=yYALsys-P_w
# Quelle: https://www.youtube.com/watch?v=JeznW_7DlB0&t
# Quelle: https://www.youtube.com/watch?v=rLyYb7BFgQI
# Quelle: https://www.youtube.com/watch?v=TAMbq0iRUsA
# Quelle: https://www.youtube.com/watch?v=HkbQ_NaH0Lc
# Quelle: https://www.youtube.com/watch?v=0l0ygSCT_q8
# Quelle: https://www.youtube.com/watch?v=0rHGnpH2_h8