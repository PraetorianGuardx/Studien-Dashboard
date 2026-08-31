from modelle import Student, Belegung, Semester, Modul, Modulstatus, Pruefungsleistung, Studiengang
from benutzerkonto import Benutzerkonto
from repositories import JSONBenutzerkontoRepository
from services import FortschrittService
from controller import StudentController
from view import KonsolenView

class Application:                                                              #Bauplan für die Anwendung
    def __init__(self):
        konto_repository = JSONBenutzerkontoRepository("benutzerkonto.json")    # Initialisiert das BenutzerkontoRepository mit dem Dateipfad
        service = FortschrittService(konto_repository)                          # Initialisiert den FortschrittService mit dem BenutzerkontoRepository
        self.controller = StudentController(service)                            # Initialisiert den StudentController mit dem FortschrittService
        self.view = KonsolenView()                                              # Initialisiert die KonsolenView für die Anzeige von Informationen in der Konsole

        # Vereinfachung: Ein Test-Student und -Konto werden beim Start fest angelegt, da eine Registrierung neuer Nutzer über die Konsole den Rahmen des Prototyps sprengen würde.

        self.student = Student("Hans", "Müller", 2.0, 3)                                                                            # Initialisiert einen Studenten mit den angegebenen Daten
        self.konto = Benutzerkonto("Hans", "passwort123", self.student, "In welcher Stadt bist du geboren?", "Frankfurt am Main")   # Initialisiert ein Benutzerkonto mit Benutzername, Passwort, Studentenobjekt, Sicherheitsfrage und -antwort
        konto_repository.speichern(self.konto)                                                                                      # Speichert das Benutzerkonto im BenutzerkontoRepository

        studiengang = Studiengang("Informatik", 180)                            # Initialisiert einen Studiengang mit dem Namen "Informatik" und 180 ECTS-Punkten
        belegung = Belegung("2024-10-01", studiengang)                          # Initialisiert eine Belegung mit dem Startdatum und dem Studiengang
        self.student.belegung_hinzufuegen(belegung)                             # Fügt die Belegung zur Liste der Belegungen des Studenten hinzu

    def starten(self):
        benutzername = input("Benutzername: ")                                  # Fragt den Benutzer nach dem Benutzernamen
        passwort = input("Passwort: ")                                          # Fragt den Benutzer nach dem Passwort

        login_erfolg = self.controller.login_versuchen(self.konto, benutzername, passwort)  # Überprüft, ob die Anmeldung erfolgreich war

        if login_erfolg:
            fortschritt = self.controller.fortschritt_abrufen(benutzername)                 # Ruft den Fortschritt des Studenten ab
            self.view.zeige_fortschritt(fortschritt)                                        # Zeigt den Fortschritt des Studenten an
        else:
            self.view.zeige_login_fehler()                                                  # Zeigt eine Fehlermeldung an, wenn die Anmeldung fehlschlägt

if __name__ == "__main__":
    app = Application()                                                                     # Initialisiert die Anwendung
    app.starten()                                                                           # Startet die Anwendung