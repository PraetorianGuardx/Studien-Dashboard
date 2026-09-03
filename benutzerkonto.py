from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from modelle import Student

ph = PasswordHasher()                                                                               # Initialisiert den PasswordHasher für die Passwort-Hashing-Funktionalität

class Benutzerkonto:                                                                                # Bauplan für ein Benutzerkonto
    def __init__(self, benutzername, passwort, student, sicherheitsfrage, sicherheitsantwort):      # Initialisiert ein Benutzerkonto mit einem Benutzernamen, Passwort, Studentenobjekt, Sicherheitsfrage und Sicherheitsantwort
        self.benutzername = benutzername                                                            # Speichert den Benutzernamen des Benutzerkontos
        self.passwort_hash = ph.hash(passwort)                                                      # Speichert den gehashten Wert des Passworts des Benutzerkontos
        self.student = student                                                                      # Speichert das Studentenobjekt, das mit dem Benutzerkonto verknüpft ist
        self.sicherheitsfrage = sicherheitsfrage                                                    # Speichert die Sicherheitsfrage des Benutzerkontos
        self.sicherheitsantwort_hash = ph.hash(self._normalisieren(sicherheitsantwort))             # Speichert die gehashte und normalisierte Sicherheitsantwort

    def _normalisieren(self, text):
        return text.strip().lower()

    def melde_an(self, benutzername, passwort):                                                     # Methode zur Anmeldung eines Benutzers
        if self.benutzername.strip().lower() != benutzername.strip().lower():                       # Überprüft, ob der eingegebene Benutzername mit dem gespeicherten Benutzernamen übereinstimmt
            return False                                                                            # Gibt False zurück, wenn der Benutzername nicht übereinstimmt
        try:
            ph.verify(self.passwort_hash, passwort)                                                 # Überprüft, ob das eingegebene Passwort mit dem gespeicherten Passwort-Hash übereinstimmt
            return True                                                                             # Gibt True zurück, wenn die Anmeldung erfolgreich ist
        except VerifyMismatchError:                                                                 # Fängt den Fehler ab, wenn das Passwort nicht übereinstimmt
            return False                                                                            # Gibt False zurück, wenn die Anmeldung fehlschlägt

    def antwort_pruefen(self, antwort):                                                             # Methode zur Überprüfung der Sicherheitsantwort
        try:
            ph.verify(self.sicherheitsantwort_hash, self._normalisieren(antwort))                   # Überprüft die normalisierte und eingegebene Antwort gegen den gespeicherten Hash
            return True                                                                             # Gibt True zurück, wenn die Sicherheitsantwort korrekt ist
        except VerifyMismatchError:                                                                 # Fängt den Fehler ab, wenn die Sicherheitsantwort nicht übereinstimmt
            return False                                                                            # Gibt False zurück, wenn die Sicherheitsantwort falsch ist

    def passwort_aendern(self, neues_passwort):                                                     # Methode zur Änderung des Passworts
        self.passwort_hash = ph.hash(neues_passwort)                                                # Aktualisiert den Passwort-Hash mit dem neuen Passwort