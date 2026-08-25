from benutzerkonto import Benutzerkonto
from services import FortschrittService

class StudentController:
    def __init__(self, fortschritt_service: FortschrittService):                        # Initialisiert den StudentController mit einem FortschrittService
        self.fortschritt_service = fortschritt_service

    def login_versuchen(self, benutzerkonto: Benutzerkonto, benutzername, passwort):    # Versucht, einen Benutzer anzumelden
        erfolgreich = benutzerkonto.melde_an(benutzername, passwort)                    # Überprüft die Anmeldedaten des Benutzerkontos
        return erfolgreich                                                              # Gibt True zurück, wenn die Anmeldung erfolgreich war, sonst False

    def fortschritt_abrufen(self, benutzername):                                        # Ruft den Fortschritt eines Studenten ab
        return self.fortschritt_service.fortschritt_anzeigen(benutzername)              # Ruft den Fortschritt des Studenten über den FortschrittService ab