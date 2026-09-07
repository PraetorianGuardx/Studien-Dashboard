from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError

# Ursprünglich war SHA-256 ohne Salt für das Projekt geplant, das ist jedoch für Passwörter ungeeignet
# SHA-256 ist auf Tempo ausgelegt, ein Angreifer könnte viele Passwörter pro Sekunde durchprobieren
# Ohne Salt ergeben die gleichen Passwörter immer denselben Hashwert
# Argon2 ist gezielt für Passwörter konzipiert und absichtlich langsam und speicherintensiv
# Durch die eigenständige Verwaltung der Parameter und des Salts durch den PasswordHasher war die Implementierung leichter als bei SHA-256
ph = PasswordHasher()

class Benutzerkonto:
    """Die technischen Zugangsdaten zu einem Studenten, bewusst getrennt von dessen fachlichen Daten in Student."""
    def __init__(self, benutzername, passwort, student, sicherheitsfrage, sicherheitsantwort):
        self.benutzername = benutzername
        # Das Passwort wird nie im Klartext gespeichert
        self.passwort_hash = ph.hash(passwort)
        # Verweist auf die fachlichen Daten, das Benutzerkonto selbst kennt nur Zugangsinformationen
        self.student = student
        self.sicherheitsfrage = sicherheitsfrage
        # Vor dem Hashen wird die Sicherheitsantwort normalisiert, damit die spätere Prüfung nicht an Groß-/Kleinschreibung oder einem versehentlichen Leerzeichen scheitert
        # Beim Passwort wäre das falsch, da dort die Groß-/Kleinschreibung Teil der Sicherheit ist
        self.sicherheitsantwort_hash = ph.hash(self._normalisieren(sicherheitsantwort))

    def _normalisieren(self, text):
        """Führende und folgende Leerzeichen werden entfernt und der Text wird kleingeschrieben."""
        return text.strip().lower()

    def melde_an(self, benutzername, passwort):
        """Der Benutzername und das Passwort werden geprüft, bei erfolgreicher Anmeldung wird True zurückgegeben."""
        # Der Name wird erneut geprüft, obwohl das Repository das Konto bereits darüber gefunden hat
        # So liegt die vollständige Prüfung im Benutzerkonto selbst und verlässt sich nicht darauf, dass der Aufrufer das passende Objekt geladen hat
        if self.benutzername.strip().lower() != benutzername.strip().lower():
            return False
        try:
            ph.verify(self.passwort_hash, passwort)
            return True
        # Der InvalidHashError wird mitaufgefangen, damit eine beschädigte konten.json zu einem fehlgeschlagenen Login führt anstatt zu einem Programmabsturz
        except (VerifyMismatchError, InvalidHashError):
            return False

    def antwort_pruefen(self, antwort):
        """Die Antwort auf die Sicherheitsfrage wird gegen den gespeicherten Hash geprüft."""
        try:
            # Hier wird dieselbe Normalisierung wie beim Anlegen genutzt, sonst passt der Hash nicht
            ph.verify(self.sicherheitsantwort_hash, self._normalisieren(antwort))
            return True
        except (VerifyMismatchError, InvalidHashError):
            return False

    def passwort_aendern(self, neues_passwort):
        """Der Passwort-Hash wird ersetzt, nachdem der Aufrufer den Benutzer authentifiziert hat."""
        self.passwort_hash = ph.hash(neues_passwort)
