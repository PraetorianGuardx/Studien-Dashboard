from enum import Enum

class Modulstatus(Enum):                                                        # Enum-Klasse für den Status eines Moduls
    BEVORSTEHEND = "bevorstehend"                                               # Status: Modul bevorstehend
    AKTUELL = "aktuell"                                                         # Status: Modul aktuell
    ABGESCHLOSSEN = "abgeschlossen"                                             # Status: Modul abgeschlossen

class Pruefungsleistung:                                                        # Bauplan für eine Prüfungsleistung

    gueltige_noten = [1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0, 5.0]    # Liste der gültigen Noten für eine Prüfungsleistung

    def __init__(self, titel, datum):                                           # Initialisiert eine Prüfungsleistung mit einem Titel, einem Datum und einer Note (initialisiert mit None)
        self.titel = titel                                                      # Speichert den Titel der Prüfungsleistung
        self.datum = datum                                                      # Speichert das Datum der Prüfungsleistung
        self.note = None                                                        # Speichert die Note der Prüfungsleistung (initialisiert mit None, da die Note noch nicht bekannt ist)

    @property
    def note(self):                                                             # Getter-Methode für die Note der Prüfungsleistung
        return self._note                                                       # Gibt die Note der Prüfungsleistung zurück

    @note.setter
    def note(self, wert):                                                                                               # Setter-Methode für die Note der Prüfungsleistung
        if wert is not None and wert not in self.gueltige_noten:                                                        # Überprüft, ob die Note gültig ist (entweder None oder in der Liste der gültigen Noten)
            raise ValueError(f"Ungültige Note. Bitte geben Sie eine der gültigen Noten {self.gueltige_noten} ein.")
        self._note = wert                                                                                               # Speichert die Note der Prüfungsleistung

class Modul:
    def __init__(self, name, status, ects):                                     # Initialisiert ein Modul mit einem Namen, einem Status und einer Anzahl von ECTS-Punkten
        self.name = name                                                        # Speichert den Namen des Moduls
        self.status = status                                                    # Speichert den Status des Moduls (bestanden, nicht bestanden, in Bearbeitung)
        self.ects = ects                                                        # Speichert die ECTS-Punkte des Moduls
        self.pruefungsleistungen = []                                           # Leere Liste, die die Prüfungsleistungen des Moduls speichert

    @property
    def status(self):                                                           # Getter-Methode für den Status des Moduls
        return self._status                                                     # Gibt den Status des Moduls zurück

    @status.setter
    def status(self, wert):                                                     # Setter-Methode für den Status des Moduls
        if not isinstance(wert, Modulstatus):                                   # Überprüft, ob der Wert eine Instanz von Modulstatus ist
            raise ValueError("Status muss ein Modulstatus sein.")               # Wirft eine Fehlermeldung, wenn der Wert kein Modulstatus ist
        self._status = wert                                                     # Speichert den Status des Moduls

    def pruefungsleistung_hinzufuegen(self, pruefungsleistung):                 # Fügt eine Prüfungsleistung zum Modul hinzu
        self.pruefungsleistungen.append(pruefungsleistung)                      # Hängt die Prüfungsleistungen an die Liste der Prüfungsleistungen des Moduls an

    def modulnote_berechnen(self):                                              # Berechnet die Modulnote des Moduls
        for pruefungsleistung in reversed(self.pruefungsleistungen):            # Iteriert über alle Prüfungsleistungen des Moduls in umgekehrter Reihenfolge
            if pruefungsleistung.note is not None:                              # Überprüft, ob die Prüfungsleistung eine Note hat
                return pruefungsleistung.note                                   # Gibt die Note der letzten bewerteten Prüfungsleistung zurück
        return None                                                             # Gibt None zurück, wenn keine bewerteten Prüfungsleistungen vorhanden sind

    def pruefungsleistung_entfernen(self, pruefungsleistung):                   # Entfernt eine Prüfungsleistung aus dem Modul
        self.pruefungsleistungen.remove(pruefungsleistung)                      # Entfernt die angegebene Prüfungsleistung aus der Liste der Prüfungsleistungen des Moduls

class Semester:                                                                 # Bauplan für ein Semester
    def __init__(self, nummer):                                                 # Initialisiert ein Semester mit einer Nummer und einer leeren Liste von Modulen
        self.semester_nummer = nummer                                           # Speichert die Nummer des Semesters
        self.module = []                                                        # Leere Liste, die die Module des Semesters speichert

    def modul_hinzufuegen(self, modul):                                         # Fügt ein Modul zur Liste der Module des Semesters hinzu
        self.module.append(modul)                                               # Hängt das Modul an die Liste der Module des Semesters an

    def modul_entfernen(self, modul):                                           # Entfernt ein Modul aus der Liste der Module des Semesters
        self.module.remove(modul)                                               # Entfernt das angegebene Modul aus der Liste der Module des Semesters

class Studiengang:                                                              # Bauplan für einen Studiengang
    def __init__(self, name, ects_gesamt):                                      # Initialisiert einen Studiengang mit einem Namen
        self.name = name                                                        # Speichert den Namen des Studiengangs
        self.ects_gesamt = ects_gesamt                                          # Speichert die Gesamtzahl der ECTS-Punkte des Studiengangs

class Belegung:                                                                 # Bauplan für eine Belegung
    def __init__(self, startdatum, studiengang):                                # Initialisiert eine Belegung mit einem Startdatum und einer leeren Liste von Semestern
        self.startdatum = startdatum                                            # Speichert das Startdatum der Belegung
        self.studiengang = studiengang                                          # Speichert den Studiengang der Belegung
        self.semester = []                                                      # Leere Liste, die die Semester der Belegung speichert

    def semester_hinzufuegen(self, semester):                                   # Fügt ein Semester zur Liste der Semester der Belegung hinzu
        self.semester.append(semester)                                          # Hängt das Semester an die Liste der Semester der Belegung an

    def ects_erreicht_berechnen(self):                                          # Berechnet die erreichten ECTS-Punkte der Belegung
        ects_erreicht = 0                                                       # Initialisiert die erreichten ECTS-Punkte mit 0
        for semester in self.semester:                                          # Iteriert über alle Semester der Belegung
            for modul in semester.module:                                       # Iteriert über alle Module des Semesters
                if modul.status == Modulstatus.ABGESCHLOSSEN:                   # Überprüft, ob das Modul abgeschlossen ist
                    ects_erreicht += modul.ects                                 # Addiert die ECTS-Punkte des Moduls zu den erreichten ECTS-Punkten
        return ects_erreicht                                                    # Gibt die erreichten ECTS-Punkte zurück

    def notendurchschnitt_berechnen(self):                                      # Berechnet den Notendurchschnitt der Belegung
        summe_noten = 0                                                         # Initialisiert die Summe der Noten mit 0
        summe_ects = 0                                                          # Initialisiert die Summe der ECTS-Punkte mit 0
        for semester in self.semester:                                          # Iteriert über alle Semester der Belegung
            for modul in semester.module:                                       # Iteriert über alle Module des Semesters
                if modul.status == Modulstatus.ABGESCHLOSSEN:                   # Überprüft, ob das Modul abgeschlossen ist
                    modulnote = modul.modulnote_berechnen()                     # Berechnet die Modulnote des Moduls
                    if modulnote is not None:                                   # Überprüft, ob die Modulnote nicht None ist
                        summe_noten += modulnote * modul.ects                   # Addiert die Modulnote multipliziert mit den ECTS-Punkten des Moduls zur Summe der Noten
                        summe_ects += modul.ects                                # Addiert die ECTS-Punkte des Moduls zur Summe der ECTS-Punkte
        if summe_ects > 0:                                                      # Überprüft, ob die Summe der ECTS-Punkte größer als 0 ist
            return summe_noten / summe_ects                                     # Gibt den gewichteten Notendurchschnitt zurück
        else:
            return None                                                         # Gibt None zurück, wenn keine bewerteten Module vorhanden sind

    def semester_entfernen(self, semester):                                     # Entfernt ein Semester aus der Liste der Semester der Belegung anhand der Semesternummer
        self.semester.remove(semester)                                          # Entfernt das angegebene Semester aus der Liste der Semester der Belegung

class Student:                                                                  # Bauplan für einen Studenten
    def __init__(self, vorname, nachname, zielnote, regelstudienzeit):          # Initialisiert einen Studenten mit einem Vornamen, Nachnamen, Zielnote und Regelstudienzeit
        self.vorname = vorname                                                  # Speichert den Vornamen des Studenten
        self.nachname = nachname                                                # Speichert den Nachnamen des Studenten
        self.zielnote = zielnote                                                # Speichert die Zielnote des Studenten
        self.regelstudienzeit = regelstudienzeit                                # Speichert die Regelstudienzeit des Studenten
        self.belegungen = []                                                    # Leere Liste, die die Belegungen des Studenten speichert

    def belegung_hinzufuegen(self, belegung):                                   # Fügt eine Belegung zur Liste der Belegungen des Studenten hinzu
        self.belegungen.append(belegung)                                        # Hängt die Belegung an die Liste der Belegungen des Studenten an

# Quelle: https://www.youtube.com/watch?v=yYALsys-P_w
# Quelle: https://www.youtube.com/watch?v=JeznW_7DlB0&t
# Quelle: https://www.youtube.com/watch?v=rLyYb7BFgQI
# Quelle: https://www.youtube.com/watch?v=TAMbq0iRUsA
# Quelle: https://www.youtube.com/watch?v=HkbQ_NaH0Lc
# Quelle: https://www.youtube.com/watch?v=0l0ygSCT_q8
# Quelle: https://www.youtube.com/watch?v=0rHGnpH2_h8