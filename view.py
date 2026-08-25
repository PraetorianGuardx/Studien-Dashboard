class KonsolenView:                             # Bauplan für die Konsolenansicht
    def zeige_fortschritt(self, fortschritt):   # Methode zur Anzeige des Fortschritts eines Studenten
        if fortschritt is None:                 # Überprüft, ob der Fortschritt None ist
            print("Kein Fortschritt gefunden.")
            return

        print(f"Student: {fortschritt['vorname']} {fortschritt['nachname']}")                       # Gibt den Namen des Studenten aus
        print(f"Zielnote: {fortschritt['zielnote']}")                                               # Gibt die Zielnote des Studenten aus
        print(f"Regelstudienzeit: {fortschritt['regelstudienzeit']}")                               # Gibt die Regelstudienzeit des Studenten aus
        print(f"Erreichte ECTS: {fortschritt['ects_erreicht']}")                                    # Gibt die erreichten ECTS-Punkte des Studenten aus
        print(f"Notendurchschnitt: {fortschritt['notendurchschnitt']}")                             # Gibt den Notendurchschnitt des Studenten aus

    def zeige_login_fehler(self):                                                                   # Methode zur Anzeige eines Login-Fehlers
        print("Login fehlgeschlagen. Bitte überprüfen Sie Ihren Benutzernamen und Ihr Passwort.")   # Gibt eine Fehlermeldung aus