from enum import Enum

class Modulstatus(Enum):
    """Der Lebenszyklus eines Moduls, von bevorstehend bis zum bestandenen Abschluss."""
    # Damit Tippfehler nicht unbemerkt durchgehen, wird ein Enum anstatt eines Strings genutzt
    # Dadurch kann der Setter in Modul den Wert per isinstance prüfen
    BEVORSTEHEND = "bevorstehend"
    AKTUELL = "aktuell"
    ABGESCHLOSSEN = "abgeschlossen"

class Pruefungsleistung:
    """Eine Prüfung innerhalb eines Moduls, zum Beispiel eine Klausur, ein Test oder eine Hausarbeit."""
    # Damit Zwischenwerte wie 2.1 oder 4.5 nicht angenommen werden, wurden feste Notenstufen implementiert
    # Es handelt sich bewusst um ein Klassenattribut, da die Liste für alle Prüfungsleistungen gleich ist und die View sie direkt als Auswahlmenü verwendet
    gueltige_noten = [1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0, 5.0]

    def __init__(self, titel, datum):
        self.titel = titel
        self.datum = datum
        # Die Zuweisung der Note läuft über den Setter, deshalb muss None dort ausdrücklich erlaubt sein
        self.note = None

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, wert):
        # Die Prüfung der Noten ist im Setter und nicht im Controller, damit keine ungültigen Noten in das Objekt gelangen können
        if wert is not None and wert not in self.gueltige_noten:
            raise ValueError(f"Ungültige Note. Bitte geben Sie eine der gültigen Noten {self.gueltige_noten} ein.")
        self._note = wert

class Modul:
    """Ein Modul eines Semesters mit ECTS-Punkten und den zugehörigen Prüfungsleistungen."""
    def __init__(self, name, status, ects):
        self.name = name
        self.status = status
        self.ects = ects
        self.pruefungsleistungen = []

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, wert):
        # Ein Enum alleine schützt in Python nicht vor falschen Werten, ohne diese Prüfung wäre self.status = "abgeschlossen" als String möglich
        if not isinstance(wert, Modulstatus):
            raise ValueError("Status muss ein Modulstatus sein.")
        self._status = wert

    def pruefungsleistung_hinzufuegen(self, pruefungsleistung):
        """Eine Prüfungsleistung wird an die Liste des Moduls angehängt."""
        self.pruefungsleistungen.append(pruefungsleistung)

    def modulnote_berechnen(self):
        """Die Note der zuletzt bewerteten Prüfungsleistung wird zurückgegeben, sonst None."""
        # Es wurde bewusst kein Durchschnitt gewählt, da eine Prüfung mit 5.0 als nicht bestanden gilt und wiederholt werden muss, erst dann zählt die bestandene Note
        # Die Liste steht in Eintragungsreihenfolge, reversed() durchläuft sie deshalb von hinten und liefert den neuesten Versuch zuerst
        for pruefungsleistung in reversed(self.pruefungsleistungen):
            if pruefungsleistung.note is not None:
                return pruefungsleistung.note
        return None

    def pruefungsleistung_entfernen(self, pruefungsleistung):
        """Die übergebene Prüfungsleistung wird aus dem Modul entfernt."""
        self.pruefungsleistungen.remove(pruefungsleistung)

class Semester:
    """Ein Semester, das die in diesem Zeitraum belegten Module bündelt."""
    def __init__(self, nummer):
        self.semester_nummer = nummer
        self.module = []

    def modul_hinzufuegen(self, modul):
        """Ein Modul wird dem Semester hinzugefügt."""
        self.module.append(modul)

    def modul_entfernen(self, modul):
        """Das übergebene Modul wird aus dem Semester entfernt."""
        self.module.remove(modul)

class Studiengang:
    """Der allgemeine Studienaufbau, unabhängig von einer konkreten Person."""
    def __init__(self, name, ects_gesamt):
        self.name = name
        self.ects_gesamt = ects_gesamt

class Belegung:
    """Die persönlichen Studiendaten eines Studenten, die mit einem Studiengang verbunden werden."""
    def __init__(self, startdatum, studiengang):
        self.startdatum = startdatum
        self.studiengang = studiengang
        self.semester = []

    def semester_hinzufuegen(self, semester):
        """Ein Semester wird der Belegung hinzugefügt."""
        self.semester.append(semester)

    def ects_erreicht_berechnen(self):
        """Die Summe der ECTS-Punkte aller abgeschlossenen Module wird zurückgegeben."""
        # Nur ABGESCHLOSSEN zählt, weil ECTS erst mit dem Bestehen gutgeschrieben werden
        # Ein nicht bestandenes Modul behält den Status AKTUELL und fällt somit automatisch heraus
        ects_erreicht = 0
        for semester in self.semester:
            for modul in semester.module:
                if modul.status == Modulstatus.ABGESCHLOSSEN:
                    ects_erreicht += modul.ects
        return ects_erreicht

    def notendurchschnitt_berechnen(self):
        """Der nach ECTS gewichtete Notendurchschnitt aller abgeschlossenen Module wird zurückgegeben, sonst None."""
        # Die Gewichtung wird nach ECTS gemacht, weil ein Modul mit 10 ECTS stärker in den Abschluss eingeht als eines mit 5 ECTS
        summe_noten = 0
        summe_ects = 0
        for semester in self.semester:
            for modul in semester.module:
                if modul.status == Modulstatus.ABGESCHLOSSEN:
                    modulnote = modul.modulnote_berechnen()
                    if modulnote is not None:
                        summe_noten += modulnote * modul.ects
                        summe_ects += modul.ects
        if summe_ects > 0:
            return summe_noten / summe_ects
        else:
            return None

    def semester_entfernen(self, semester):
        """Das übergebene Semester wird aus der Belegung entfernt."""
        self.semester.remove(semester)

class Student:
    """Die fachlichen Stammdaten eines Studenten, die Zugangsdaten liegen getrennt im Benutzerkonto."""
    def __init__(self, vorname, nachname, zielnote, regelstudienzeit):
        self.vorname = vorname
        self.nachname = nachname
        self.zielnote = zielnote
        self.regelstudienzeit = regelstudienzeit
        # Als Liste angelegt, obwohl die Anwendung nur eine Belegung erzeugt und überall belegungen[0] verwendet, so bliebe ein Studienwechsel ergänzbar
        self.belegungen = []

    def belegung_hinzufuegen(self, belegung):
        """Eine Belegung wird dem Studenten hinzugefügt."""
        self.belegungen.append(belegung)
