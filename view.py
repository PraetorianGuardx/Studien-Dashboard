from modelle import Pruefungsleistung
import getpass

class KonsolenView:                                                                                     # Bauplan für die Konsolenansicht
    def zeige_fortschritt(self, fortschritt):                                                           # Methode zur Anzeige des Fortschritts eines Studenten
        if fortschritt is None:                                                                         # Überprüft, ob der Fortschritt None ist
            print("Kein Fortschritt gefunden.")
            return                                                                                      # Gibt eine Meldung aus, wenn kein Fortschritt gefunden wurde und beendet die Methode

        print(f"Student: {fortschritt['vorname']} {fortschritt['nachname']}")                           # Gibt den Namen des Studenten aus
        print(f"Zielnote: {fortschritt['zielnote']}")                                                   # Gibt die Zielnote des Studenten aus
        print(f"Regelstudienzeit: {fortschritt['regelstudienzeit']}")                                   # Gibt die Regelstudienzeit des Studenten aus
        print(f"Erreichte ECTS: {fortschritt['ects_erreicht']}")                                        # Gibt die erreichten ECTS-Punkte des Studenten aus
        print(f"Notendurchschnitt: {fortschritt['notendurchschnitt']}")                                 # Gibt den Notendurchschnitt des Studenten aus

    def zeige_login_fehler(self):                                                                       # Methode zur Anzeige eines Login-Fehlers
        print("Login fehlgeschlagen. Bitte überprüfen Sie Ihren Benutzernamen und Ihr Passwort.")       # Gibt eine Fehlermeldung aus

    def frage_registrierungsdaten_ab(self):                                                             # Methode zur Abfrage von Registrierungsdaten
        benutzername = input("Benutzername: ")                                                          # Fragt den Benutzer nach dem Benutzernamen
        passwort = getpass.getpass("Passwort: ")                                                        # Fragt den Benutzer nach dem Passwort (ohne sichtbare Eingabe)
        vorname = input("Vorname: ")                                                                    # Fragt den Benutzer nach dem Vornamen
        nachname = input("Nachname: ")                                                                  # Fragt den Benutzer nach dem Nachnamen
        zielnote = self.frage_float_ab("Zielnote: ")                                                    # Fragt den Benutzer nach der Zielnote und konvertiert sie in eine Gleitkommazahl
        regelstudienzeit = self.frage_int_ab("Regelstudienzeit (in Semestern): ")                       # Fragt den Benutzer nach der Regelstudienzeit und konvertiert sie in einen Integer
        sicherheitsfrage = input("Sicherheitsfrage: ")                                                  # Fragt den Benutzer nach der Sicherheitsfrage
        sicherheitsantwort = input("Sicherheitsantwort: ")                                              # Fragt den Benutzer nach der Sicherheitsantwort
        studiengang_name = input("Studiengang: ")                                                       # Fragt den Benutzer nach dem Studiengang
        ects_gesamt = self.frage_int_ab("Gesamt-ECTS: ")                                                # Fragt den Benutzer nach den Gesamt-ECTS und konvertiert sie in einen Integer
        start_datum = input("Startdatum (DD.MM.YYYY): ")                                                # Fragt den Benutzer nach dem Startdatum

        return benutzername, passwort, vorname, nachname, zielnote, regelstudienzeit, sicherheitsfrage, sicherheitsantwort, studiengang_name, ects_gesamt, start_datum      # Gibt die abgefragten Daten zurück

    def waehle_aus_liste(self, elemente, anzeige_funktion):                                             # Methode zur Auswahl eines Elements aus einer Liste
        for index, element in enumerate(elemente, start=1):                                             # Iteriert über die Elemente der Liste und nummeriert sie
            print(f"{index}. {anzeige_funktion(element)}")                                              # Gibt jedes Element aus
        while True:                                                                                     # Endlosschleife zur wiederholten Abfrage, bis eine gültige Auswahl getroffen wird
            auswahl = self.frage_int_ab("Bitte wählen Sie eine Option: ")                               # Fragt den Benutzer nach einer Auswahl und konvertiert sie in einen Integer
            if 1 <= auswahl <= len(elemente):                                                           # Überprüft, ob die Auswahl innerhalb des gültigen Bereichs liegt
                return elemente[auswahl - 1]                                                            # Gibt das ausgewählte Element zurück (Index um 1 verringert, da die Liste bei 0 beginnt)
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")                                  # Gibt eine Fehlermeldung aus, wenn die Auswahl ungültig ist

    def frage_semester_ab(self):                                                                        # Methode zur Abfrage eines Semesters
        semester_nummer = self.frage_int_ab("Semester (als Zahl): ")                                    # Fragt den Benutzer nach der Semesternummer und konvertiert sie in einen Integer
        return semester_nummer                                                                          # Gibt die abgefragte Semesternummer zurück

    def frage_modul_ab(self):                                                                           # Methode zur Abfrage eines Moduls
        name = input("Modulname: ")                                                                     # Fragt den Benutzer nach dem Modulnamen
        ects = self.frage_int_ab("ECTS-Punkte: ")                                                       # Fragt den Benutzer nach den ECTS-Punkten und konvertiert sie in einen Integer
        return name, ects                                                                               # Gibt den abgefragten Modulnamen und die ECTS-Punkte zurück

    def frage_pruefungsleistung_ab(self):                                                               # Methode zur Abfrage einer Prüfungsleistung
        titel = input("Prüfungsleistungstitel: ")                                                       # Fragt den Benutzer nach dem Titel der Prüfungsleistung
        datum = input("Datum (DD.MM.YYYY): ")                                                           # Fragt den Benutzer nach dem Datum der Prüfungsleistung
        note = self.waehle_aus_liste(Pruefungsleistung.gueltige_noten, lambda n: f"Note: {n}")          # Fragt den Benutzer nach einer Note aus der Liste der gültigen Noten
        return titel, datum, note                                                                       # Gibt den abgefragten Titel, das Datum und die Note der Prüfungsleistung zurück

    def frage_int_ab(self, prompt):                                                                     # Methode zur Abfrage einer Ganzzahl
        while True:                                                                                     # Endlosschleife zur wiederholten Abfrage, bis eine gültige Ganzzahl eingegeben wird
            eingabe = input(prompt)                                                                     # Fragt den Benutzer nach einer Eingabe
            try:
                return int(eingabe)
            except ValueError:                                                                          # Fängt den Fehler ab, wenn die Eingabe keine gültige Ganzzahl ist
                print("Ungültige Eingabe. Bitte geben Sie eine Ganzzahl ein.")                          # Gibt eine Fehlermeldung aus und fordert den Benutzer auf, eine gültige Ganzzahl einzugeben

    def frage_float_ab(self, prompt):                                                                   # Methode zur Abfrage einer Gleitkommazahl
        while True:                                                                                     # Endlosschleife zur wiederholten Abfrage, bis eine gültige Gleitkommazahl eingegeben wird
            eingabe = input(prompt)                                                                     # Fragt den Benutzer nach einer Eingabe
            try:
                return float(eingabe)
            except ValueError:                                                                          # Fängt den Fehler ab, wenn die Eingabe keine gültige Gleitkommazahl ist
                print("Ungültige Eingabe. Bitte geben Sie eine Zahl ein.")                              # Gibt eine Fehlermeldung aus und fordert den Benutzer auf, eine gültige Gleitkommazahl einzugeben

    def frage_sicherheitsantwort_ab(self, sicherheitsfrage):                                            # Methode zur Abfrage der Sicherheitsantwort
        print(f"Sicherheitsfrage: {sicherheitsfrage}")                                                  # Gibt die Sicherheitsfrage aus
        antwort = input("Antwort: ")                                                                    # Fragt den Benutzer nach der Antwort auf die Sicherheitsfrage
        return antwort                                                                                  # Gibt die abgefragte Antwort zurück

    def frage_neues_passwort_ab(self):                                                                  # Methode zur Abfrage eines neuen Passworts
        neues_passwort = getpass.getpass("Neues Passwort: ")                                            # Fragt den Benutzer nach einem neuen Passwort (ohne sichtbare Eingabe)
        return neues_passwort                                                                           # Gibt das abgefragte neue Passwort zurück

    def zeige_gesamtuebersicht(self, semester_liste):                                                                    # Methode zur Anzeige der Gesamtübersicht der Semester
        if not semester_liste:                                                                                          # Überprüft, ob die Semesterliste leer ist
            print("Keine Semesterinformationen verfügbar.")                                                             # Gibt eine Meldung aus, wenn keine Semesterinformationen verfügbar sind
            return                                                                                                      # Beendet die Methode
        for semester in semester_liste:                                                                                 # Iteriert über die Semesterliste
            print(f"\nSemester {semester.semester_nummer}:")                                                            # Gibt die Semesternummer aus
            for modul in semester.module:                                                                               # Iteriert über die Module des Semesters                                                                                                                   
                print(f" - {modul.name} ({modul.ects} ECTS, Status: {modul.status.value})")                             # Gibt den Namen und die ECTS-Punkte des Moduls aus
                for pruefungsleistung in modul.pruefungsleistungen:                                                     # Iteriert über die Prüfungsleistungen des Moduls
                    note_text = pruefungsleistung.note if pruefungsleistung.note is not None else "Keine Note"          # Überprüft, ob eine Note vorhanden ist und gibt sie aus, ansonsten wird "Keine Note" angezeigt
                    print(f"   - {pruefungsleistung.titel} ({pruefungsleistung.datum}, Note: {note_text})")             # Gibt den Titel, das Datum und die Note der Prüfungsleistung aus

# Quelle: https://www.youtube.com/watch?v=M3EHqLw5w8I