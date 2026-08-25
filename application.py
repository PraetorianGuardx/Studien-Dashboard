from modelle import Student, Belegung, Semester, Modul, Modulstatus, Pruefungsleistung
from benutzerkonto import Benutzerkonto
from repositories import JSONStudentRepository
from services import FortschrittService
from controller import StudentController
from view import KonsolenView

class Application:                                                          #Bauplan für die Anwendung
    def __init__(self):
        repository = JSONStudentRepository("student_application.json")      # Initialisiert das StudentRepository mit der JSON-Datei
        service = FortschrittService(repository)                            # Initialisiert den FortschrittService mit dem StudentRepository
        self.controller = StudentController(service)                        # Initialisiert den StudentController mit dem FortschrittService
        self.view = KonsolenView()                                          # Initialisiert die KonsolenView für die Anzeige von Informationen in der Konsole

        # Vereinfachung: Ein Test-Student und -Konto werden beim Start fest angelegt, da ein vollständiges BenutzerkontoRepository den Rahmen des Prototyps sprengen würde.

        self.student = Student("Hans", "Müller", 2.0, 3)               # Initialisiert einen Studenten mit den angegebenen Daten
        self.konto = Benutzerkonto("Hans", "passwort123", self.student)    # Initialisiert ein Benutzerkonto mit dem Benutzernamen, Passwort und dem Studentenobjekt
        repository.speichern(self.student)                                  # Speichert den Studenten im StudentRepository

    def starten(self):
        benutzername = input("Benutzername: ")                              # Fragt den Benutzer nach dem Benutzernamen
        passwort = input("Passwort: ")                                      # Fragt den Benutzer nach dem Passwort

        login_erfolg = self.controller.login_versuchen(self.konto, benutzername, passwort)  # Überprüft, ob die Anmeldung erfolgreich war

        if login_erfolg:
            fortschritt = self.controller.fortschritt_abrufen(benutzername)                 # Ruft den Fortschritt des Studenten ab
            self.view.zeige_fortschritt(fortschritt)                                        # Zeigt den Fortschritt des Studenten an
        else:
            self.view.zeige_login_fehler()                                                  # Zeigt eine Fehlermeldung an, wenn die Anmeldung fehlschlägt

if __name__ == "__main__":
    app = Application()                                                                     # Initialisiert die Anwendung
    app.starten()                                                                           # Startet die Anwendung