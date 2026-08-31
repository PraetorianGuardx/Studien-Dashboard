from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from modelle import Student

ph = PasswordHasher()                                                                           # Initialisiert den PasswordHasher für die Passwort-Hashing-Funktionalität

class Benutzerkonto:                                                                            # Bauplan für ein Benutzerkonto
    def __init__(self, benutzername, passwort, student, sicherheitsfrage, sicherheitsantwort):   # initialisiert ein Benutzerkonto mit einem Benutzernamen, Passwort, Studentenobjekt, Sicherheitsfrage und Sicherheitsantwort
        self.benutzername = benutzername                                                        # speichert den Benutzernamen des Benutzerkontos
        self.passwort_hash = ph.hash(passwort)                                                  # speichert den gehashten Wert des Passworts des Benutzerkontos
        self.student = student                                                                  # speichert das Studentenobjekt, das mit dem Benutzerkonto verknüpft ist
        self.sicherheitsfrage = sicherheitsfrage                                                # speichert die Sicherheitsfrage des Benutzerkontos
        self.sicherheitsanwort_hash = ph.hash(self._normalisieren(sicherheitsantwort))

    def _normalisieren(self, text):
        return text.strip().lower()

    def melde_an(self, benutzername, passwort):                             # Methode zur Anmeldung eines Benutzers
        if self.benutzername != benutzername:                               # überprüft, ob der eingegebene Benutzername mit dem gespeicherten Benutzernamen übereinstimmt
            return False                                                    # gibt False zurück, wenn die Benutzernamen nicht übereinstimmen
        try:
            ph.verify(self.passwort_hash, passwort)                         # überprüft, ob das eingegebene Passwort mit dem gespeicherten Passwort-Hash übereinstimmt
            return True                                                     # gibt True zurück, wenn die Anmeldung erfolgreich ist
        except VerifyMismatchError:                                         # fängt den Fehler ab, wenn das Passwort nicht übereinstimmt
            return False                                                    # gibt False zurück, wenn die Anmeldung fehlschlägt

    def antwort_pruefen(self, antwort):                                     # Methode zur Überprüfung der Sicherheitsantwort
        try:
            ph.verify(self.sicherheitsanwort_hash, self._normalisieren(antwort))
            return True                                                     # gibt True zurück, wenn die Sicherheitsantwort korrekt ist
        except VerifyMismatchError:                                         # fängt den Fehler ab, wenn die Sicherheitsantwort nicht übereinstimmt
            return False                                                    # gibt False zurück, wenn die Sicherheitsantwort falsch ist