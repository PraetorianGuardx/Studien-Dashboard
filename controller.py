from benutzerkonto import Benutzerkonto
from services import FortschrittService
from modelle import Modul, Modulstatus, Student, Belegung, Studiengang, Semester, Pruefungsleistung

class StudentController:
    def __init__(self, fortschritt_service: FortschrittService):                                        # Initialisiert den StudentController mit einem FortschrittService
        self.fortschritt_service = fortschritt_service

    def login_versuchen(self, benutzerkonto: Benutzerkonto, benutzername, passwort):                    # Versucht, einen Benutzer anzumelden
        erfolgreich = benutzerkonto.melde_an(benutzername, passwort)                                    # Überprüft die Anmeldedaten des Benutzerkontos
        return erfolgreich                                                                              # Gibt True zurück, wenn die Anmeldung erfolgreich war, sonst False

    def fortschritt_abrufen(self, benutzername):                                                        # Ruft den Fortschritt eines Studenten ab
        return self.fortschritt_service.fortschritt_anzeigen(benutzername)                              # Ruft den Fortschritt des Studenten über den FortschrittService ab

    def registrieren(self, konto_repository, benutzername, passwort, vorname, nachname, zielnote, regelstudienzeit, sicherheitsfrage, sicherheitsantwort, studiengang_name, ects_gesamt, start_datum):      # Registriert einen neuen Benutzer
        bestehnendes_konto = konto_repository.laden(benutzername)                                                                                                                                           # Überprüft, ob ein Konto mit dem angegebenen Benutzernamen bereits existiert
        if bestehnendes_konto is not None:                                                                                                                                                                  # Wenn ein Konto mit dem angegebenen Benutzernamen existiert
            return None                                                                                                                                                                                     # Gibt None zurück, wenn der Benutzername bereits existiert

        student = Student(vorname, nachname, zielnote, regelstudienzeit)                                # Erstellt ein neues Studentenobjekt
        studiengang = Studiengang(studiengang_name, ects_gesamt)                                        # Erstellt ein neues Studiengang-Objekt
        belegung = Belegung(start_datum, studiengang)                                                   # Erstellt ein neues Belegungsobjekt mit dem Startdatum und dem Studiengang
        student.belegung_hinzufuegen(belegung)                                                          # Fügt die Belegung dem Studentenobjekt hinzu
        konto = Benutzerkonto(benutzername, passwort, student, sicherheitsfrage, sicherheitsantwort)    # Erstellt ein neues Benutzerkonto mit dem Studentenobjekt
        konto_repository.speichern(konto)                                                               # Speichert das neue Benutzerkonto im Repository
        return konto                                                                                    # Gibt das neu erstellte Benutzerkonto zurück

    def semester_hinzufuegen(self, benutzername, konto_repository, semester_nummer):                    # Fügt ein neues Semester zu einem Studenten hinzu
        konto = konto_repository.laden(benutzername)                                                    # Lädt das Benutzerkonto aus dem Repository
        belegung = konto.student.belegungen[0]                                                          # Greift auf die erste Belegung des Studenten zu (angenommen, es gibt nur eine Belegung)
        for vorhandenes_semester in belegung.semester:                                                  # Überprüft, ob das Semester bereits in der Belegung existiert
            if vorhandenes_semester.semester_nummer == semester_nummer:                                 # Wenn ein Semester mit der gleichen Semesternummer gefunden wird
                return False                                                                            # Gibt False zurück, um anzuzeigen, dass das Semester bereits existiert
        neues_semester = Semester(semester_nummer)                                                      # Erstellt ein neues Semesterobjekt mit der angegebenen Semesternummer
        belegung.semester_hinzufuegen(neues_semester)                                                   # Fügt das neue Semester der Belegung hinzu
        konto_repository.speichern(konto)                                                               # Speichert das aktualisierte Benutzerkonto im Repository
        return True                                                                                     # Gibt True zurück, um anzuzeigen, dass das Semester erfolgreich hinzugefügt wurde

    def semester_auflisten(self, benutzername, konto_repository):                                       # Fügt ein neues Semester zu einem Studenten hinzu
        konto = konto_repository.laden(benutzername)                                                    # Lädt das Benutzerkonto aus dem Repository
        belegung = konto.student.belegungen[0]                                                          # Greift auf die erste Belegung des Studenten zu (angenommen, es gibt nur eine Belegung)
        return konto, belegung.semester                                                                 # Gibt das Benutzerkonto und die Liste der Semester zurück

    def semester_entfernen(self, konto_repository, konto, semester):                                    # Entfernt ein Semester aus der Belegung eines Studenten
        belegung = konto.student.belegungen[0]                                                          # Greift auf die erste Belegung des Studenten zu (angenommen, es gibt nur eine Belegung)
        belegung.semester_entfernen(semester)                                                           # Entfernt das angegebene Semester aus der Belegung
        konto_repository.speichern(konto)                                                               # Speichert das aktualisierte Benutzerkonto im Repository

    def modul_hinzufuegen(self, konto_repository, konto, semester, modul_daten):                        # Fügt ein neues Modul zu einem Semester eines Studenten hinzu
        name, ects = modul_daten                                                                        # Entpackt die Modul-Daten (Name und ECTS-Punkte)
        for vorhandenes_modul in semester.module:                                                       # Überprüft, ob das Modul bereits im Semester existiert
            if vorhandenes_modul.name == name:                                                          # Wenn ein Modul mit dem gleichen Namen gefunden wird
                return False                                                                            # Gibt False zurück, um anzuzeigen, dass das Modul bereits existiert
        modul = Modul(name, Modulstatus.BEVORSTEHEND, ects)                                             # Erstellt ein neues Modulobjekt mit dem Status "BEVORSTEHEND"
        semester.modul_hinzufuegen(modul)                                                               # Fügt das Modul dem Semester hinzu
        konto_repository.speichern(konto)                                                               # Speichert das aktualisierte Benutzerkonto im Repository
        return True                                                                                     # Gibt True zurück, um anzuzeigen, dass das Modul erfolgreich hinzugefügt wurde

    def modul_auflisten(self, semester):                                                                # Listet alle Module eines Semesters eines Studenten auf
        return semester.module                                                                          # Gibt die Liste der Module des Semesters zurück

    def modul_entfernen(self, konto_repository, konto, semester, modul):                                # Entfernt ein Modul aus einem Semester eines Studenten
        semester.modul_entfernen(modul)                                                                 # Entfernt das angegebene Modul aus dem Semester
        konto_repository.speichern(konto)                                                               # Speichert das aktualisierte Benutzerkonto im Repository

    def pruefungsleistung_eintragen(self, konto_repository, konto, modul, daten):                       # Trägt eine Prüfungsleistung in ein Modul eines Studenten ein
        titel, datum, note = daten                                                                      # Entpackt die Daten der Prüfungsleistung (Titel, Datum und Note)
        pruefungsleistung = Pruefungsleistung(titel, datum)                                             # Erstellt ein neues Prüfungsleistungsobjekt
        pruefungsleistung.note = note                                                                   # Setzt die Note der Prüfungsleistung
        modul.pruefungsleistung_hinzufuegen(pruefungsleistung)                                          # Fügt die Prüfungsleistung dem Modul hinzu
        if note == 5.0:                                                                                 # Überprüft, ob die Note der Prüfungsleistung 5.0 ist (nicht bestanden)
            modul.status = Modulstatus.AKTUELL                                                          # Setzt den Status des Moduls auf "AKTUELL", wenn die Note 5.0 ist (nicht bestanden)
        else:                                                                                           # Überprüft, ob die Note der Prüfungsleistung nicht 5.0 ist (bestanden)
            modul.status = Modulstatus.ABGESCHLOSSEN                                                    # Setzt den Status des Moduls auf "ABGESCHLOSSEN"
        konto_repository.speichern(konto)                                                               # Speichert das aktualisierte Benutzerkonto im Repository

    def pruefungsleistung_entfernen(self, konto_repository, konto, modul, pruefungsleistung):           # Entfernt eine Prüfungsleistung aus einem Modul eines Studenten
        modul.pruefungsleistung_entfernen(pruefungsleistung)                                            # Entfernt die angegebene Prüfungsleistung aus dem Modul
        konto_repository.speichern(konto)                                                               # Speichert das aktualisierte Benutzerkonto im Repository

    def konto_loeschen(self, benutzername, konto_repository):                                           # Löscht ein Benutzerkonto eines Studenten
        return konto_repository.loeschen(benutzername)                                                  # Löscht das Benutzerkonto aus dem Repository

    def passwort_zuruecksetzen(self, konto_repository, benutzername, antwort, neues_passwort):          # Methode zur Abfrage von Daten zum Zurücksetzen des Passworts
        konto = konto_repository.laden(benutzername)                                                    # Lädt das Benutzerkonto anhand des Benutzernamens
        if konto is None:                                                                               # Überprüft, ob das Benutzerkonto existiert
            return False                                                                                # Gibt False zurück, wenn das Benutzerkonto nicht existiert
        if not konto.antwort_pruefen(antwort):                                                          # Überprüft die Sicherheitsantwort des Benutzerkontos
            return False                                                                                # Gibt False zurück, wenn die Sicherheitsantwort nicht korrekt ist
        konto.passwort_aendern(neues_passwort)                                                          # Ändert das Passwort des Benutzerkontos
        konto_repository.speichern(konto)                                                               # Speichert das aktualisierte Benutzerkonto im Repository
        return True                                                                                     # Gibt True zurück, wenn das Passwort erfolgreich zurückgesetzt wurde