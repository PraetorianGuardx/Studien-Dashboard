from benutzerkonto import Benutzerkonto
from services import FortschrittService
from modelle import Modul, Modulstatus, Student, Belegung, Studiengang, Semester, Pruefungsleistung

class StudentController:
    """Die Vermittlung zwischen der Bedienoberfläche und den Fach- und Repository-Klassen."""
    # View und Application arbeiten ausschließlich über diese Methoden und greifen nie direkt auf die Fachklasse zu
    # Jede Änderung wird sofort über das Repository gespeichert, ein extra Speicherbefehl in der Bedienung wird somit vermieden
    def __init__(self, fortschritt_service: FortschrittService):
        self.fortschritt_service = fortschritt_service

    def login_versuchen(self, benutzerkonto: Benutzerkonto, benutzername, passwort):
        """Die Anmeldedaten werden geprüft, bei Erfolg wird True zurückgegeben."""
        # Die eigentliche Prüfung liegt im Benutzerkonto, der Controller reicht sie nur weiter, damit die Application die Fachklasse nicht selbst aufrufen muss
        erfolgreich = benutzerkonto.melde_an(benutzername, passwort)
        return erfolgreich

    def fortschritt_abrufen(self, benutzername):
        """Die Fortschrittsdaten werden über den FortschrittService abgerufen."""
        return self.fortschritt_service.fortschritt_anzeigen(benutzername)

    def registrieren(self, konto_repository, benutzername, passwort, vorname, nachname, zielnote, regelstudienzeit, sicherheitsfrage, sicherheitsantwort, studiengang_name, ects_gesamt, start_datum):
        """Ein neues Benutzerkonto wird angelegt, bei bereits vergebenem Benutzernamen wird None zurückgegeben."""
        bestehendes_konto = konto_repository.laden(benutzername)
        if bestehendes_konto is not None:
            return None

        # Hier wird der gesamte Objektbaum aufgebaut: der Studiengang beschreibt den allgemeinen Aufbau, die Belegung verbindet ihn mit dem Studenten
        # Das Benutzerkonto erhält den Studenten und nicht umgekehrt, damit die fachlichen Daten nichts von den Zugangsdaten wissen müssen
        student = Student(vorname, nachname, zielnote, regelstudienzeit)
        studiengang = Studiengang(studiengang_name, ects_gesamt)
        belegung = Belegung(start_datum, studiengang)
        student.belegung_hinzufuegen(belegung)
        konto = Benutzerkonto(benutzername, passwort, student, sicherheitsfrage, sicherheitsantwort)
        konto_repository.speichern(konto)
        return konto

    def semester_hinzufuegen(self, benutzername, konto_repository, semester_nummer):
        """Ein Semester wird angelegt, bei bereits vorhandener Semesternummer wird False zurückgegeben."""
        konto = konto_repository.laden(benutzername)
        # Es wird immer die erste Belegung verwendet, weil die Anwendung pro Student genau eine anlegt
        belegung = konto.student.belegungen[0]
        # Doppelte Semesternummern werden verhindert, damit die Auswahlliste in der View eindeutig bleibt
        for vorhandenes_semester in belegung.semester:
            if vorhandenes_semester.semester_nummer == semester_nummer:
                return False
        neues_semester = Semester(semester_nummer)
        belegung.semester_hinzufuegen(neues_semester)
        konto_repository.speichern(konto)
        return True

    def semester_auflisten(self, benutzername, konto_repository):
        """Das Benutzerkonto und die Liste seiner Semester werden zurückgegeben."""
        # Das Konto wird mit zurückgegeben, weil die Application es anschließend zum Speicher der Änderung braucht und es sonst ein zweites Mal laden müsste
        konto = konto_repository.laden(benutzername)
        belegung = konto.student.belegungen[0]
        return konto, belegung.semester

    def semester_entfernen(self, konto_repository, konto, semester):
        """Ein Semester wird samt seiner Module aus der Belegung entfernt."""
        belegung = konto.student.belegungen[0]
        belegung.semester_entfernen(semester)
        konto_repository.speichern(konto)

    def modul_hinzufuegen(self, konto_repository, konto, semester, modul_daten):
        """Ein Modul wird dem Semester hinzugefügt, bei bereits vorhandenem Namen wird False zurückgegeben."""
        name, ects = modul_daten
        # Der Vergleich ignoriert Groß-/Kleinschreibung und Leerzeichen, damit "Python" und "python" nicht als zwei Module angelegt werden
        for vorhandenes_modul in semester.module:
            if vorhandenes_modul.name.strip().lower() == name.strip().lower():
                return False
        # Ein neues Modul startet immer als BEVORSTEHEND, den Status ändert erst das Eintragen der Note
        modul = Modul(name, Modulstatus.BEVORSTEHEND, ects)
        semester.modul_hinzufuegen(modul)
        konto_repository.speichern(konto)
        return True

    def modul_auflisten(self, semester):
        """Die Module des Semesters werden zurückgegeben."""
        return semester.module

    def modul_entfernen(self, konto_repository, konto, semester, modul):
        """Ein Modul wird samt Prüfungsleistungen aus dem Semester entfernt."""
        semester.modul_entfernen(modul)
        konto_repository.speichern(konto)

    def pruefungsleistung_eintragen(self, konto_repository, konto, modul, daten):
        """Eine Prüfungsleistung wird eingetragen und der Modulstatus entsprechend gesetzt."""
        titel, datum, note = daten
        pruefungsleistung = Pruefungsleistung(titel, datum)
        pruefungsleistung.note = note
        modul.pruefungsleistung_hinzufuegen(pruefungsleistung)
        # Bei 5.0 bleibt das Modul auf AKTUELL statt ABGESCHLOSSEN, sonst würden ECTS für eine nicht bestandene Prüfung gutgeschrieben werden
        if note == 5.0:
            modul.status = Modulstatus.AKTUELL
        else:
            modul.status = Modulstatus.ABGESCHLOSSEN
        konto_repository.speichern(konto)

    def pruefungsleistung_entfernen(self, konto_repository, konto, modul, pruefungsleistung):
        """Eine Prüfungsleistung wird entfernt und der Modulstatus neu bestimmt."""
        modul.pruefungsleistung_entfernen(pruefungsleistung)
        # Der Status muss neu bestimmt werden, sonst bliebe ein Modul ohne verbleibende Note weiterhin ABGESCHLOSSEN und würde seine ECTS mitzählen, obwohl keine Bewertung mehr vorliegt
        letzte_note = modul.modulnote_berechnen()
        if letzte_note is None:
            modul.status = Modulstatus.BEVORSTEHEND
        elif letzte_note == 5.0:
            modul.status = Modulstatus.AKTUELL
        else:
            modul.status = Modulstatus.ABGESCHLOSSEN
        konto_repository.speichern(konto)

    def konto_loeschen(self, benutzername, konto_repository):
        """Das Benutzerkonto wird gelöscht und True wird zurückgegeben, falls es vorhanden ist."""
        return konto_repository.loeschen(benutzername)

    # Das Prüfen der Sicherheitsantwort und das Setzen des Passworts sind bewusst zwei Methoden, damit die Application das neue Passwort erst abfragt, nachdem die Antwort bestätigt wurde
    def sicherheitsantwort_pruefen(self, konto_repository, benutzername, antwort):
        """Die Sicherheitsantwort wird geprüft, bei fehlendem Konto wird False zurückgegeben."""
        konto = konto_repository.laden(benutzername)
        if konto is None:
            return False
        return konto.antwort_pruefen(antwort)

    def passwort_setzen(self, konto_repository, benutzername, neues_passwort):
        """Das Passwort wird gesetzt, bei fehlendem Konto wird False zurückgegeben."""
        # Hier wird nicht selber geprüft, ob der Aufrufer berechtigt ist, das muss vorher über sicherheitsantwort_pruefen passieren
        konto = konto_repository.laden(benutzername)
        if konto is None:
            return False
        konto.passwort_aendern(neues_passwort)
        konto_repository.speichern(konto)
        return True