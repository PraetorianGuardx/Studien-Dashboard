import hashlib                                                                                                              # Import der hashlib-Bibliothek, die Funktionen für kryptografische Hashes bereitstellt

class Benutzer:                                                                                                             # Bauplan für einen Benutzer
    def __init__(self, vorname, nachname, benutzername, passwort, sicherheitsfrage, sicherheitsantwort):                    # initialisiert einen Benutzer mit einem Vornamen, Nachnamen, Benutzernamen, Passwort, Sicherheitsfrage und Sicherheitsantwort
        self.vorname = vorname                                                                                              # speichert den Vornamen des Benutzers
        self.nachname = nachname                                                                                            # speichert den Nachnamen des Benutzers
        self.benutzername = benutzername                                                                                    # speichert den Benutzernamen des Benutzers                  
        self.passwort_hash = hashlib.sha256(passwort.encode()).hexdigest()                                                  # speichert den Hash des Passworts des Benutzers, um die Sicherheit zu erhöhen
        self.sicherheitsfrage = sicherheitsfrage                                                                            # speichert die Sicherheitsfrage des Benutzers
        self.sicherheitsantwort_hash = hashlib.sha256(sicherheitsantwort.encode()).hexdigest()                              # speichert den Hash der Sicherheitsantwort des Benutzers, um die Sicherheit zu erhöhen

    def melde_an(self, benutzername, passwort):                                                                             # überprüft, ob der eingegebene Benutzername und das Passwort mit den gespeicherten Werten übereinstimmen
        if self.benutzername == benutzername and self.passwort_hash == hashlib.sha256(passwort.encode()).hexdigest():       # wenn der Benutzername und das Passwort übereinstimmen, wird True zurückgegeben
            return True                                                                                                     # Return True, wenn die Anmeldedaten korrekt sind
        else:
            return False                                                                                                    # Return False, wenn die Anmeldedaten nicht korrekt sind

# Quelle: https://www.youtube.com/watch?v=YFn0iwU-Jz8
# Quelle: https://docs.python.org/3/library/hashlib.html