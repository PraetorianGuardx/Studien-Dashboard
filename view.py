from modelle import Pruefungsleistung
import getpass

class KonsolenView:
    """Die wiederverwendbaren Ein- und Ausgabebausteine für die Konsole."""
    def zeige_fortschritt(self, fortschritt):
        """Die Fortschrittsdaten werden ausgegeben, bei None wird eine Meldung angezeigt."""
        if fortschritt is None:
            print("Kein Fortschritt gefunden.")
            return

        # Gelesen wird nur aus dem Dictionary des FortschrittService, dadurch muss die View die Fachklassen nicht kennen
        print(f"Student: {fortschritt['vorname']} {fortschritt['nachname']}")
        print(f"Zielnote: {fortschritt['zielnote']}")
        print(f"Regelstudienzeit: {fortschritt['regelstudienzeit']}")
        print(f"Erreichte ECTS: {fortschritt['ects_erreicht']}")
        # Ohne abgeschlossenes Modul liefert der Service None, das wird hier unverändert ausgegeben
        # Die Ausgabe zeigt damit ehrlich an, dass noch kein Durchschnitt berechnet werden kann
        print(f"Notendurchschnitt: {fortschritt['notendurchschnitt']}")

    def zeige_login_fehler(self):
        """Eine Fehlermeldung zur fehlgeschlagenen Anmeldung wird ausgegeben."""
        print("Login fehlgeschlagen. Bitte überprüfen Sie Ihren Benutzernamen und Ihr Passwort.")

    def frage_registrierungsdaten_ab(self):
        """Alle Registrierungsdaten werden abgefragt und als Tupel zurückgegeben."""
        benutzername = input("Benutzername: ")
        # getpass statt input, damit das Passwort nicht sichtbar in der Konsole und im Verlauf stehen bleibt
        passwort = getpass.getpass("Passwort: ")
        vorname = input("Vorname: ")
        nachname = input("Nachname: ")
        zielnote = self.frage_float_ab("Zielnote: ")
        regelstudienzeit = self.frage_int_ab("Regelstudienzeit (Angabe in Semestern): ")
        sicherheitsfrage = input("Sicherheitsfrage: ")
        sicherheitsantwort = input("Sicherheitsantwort: ")
        studiengang_name = input("Studiengang: ")
        ects_gesamt = self.frage_int_ab("Gesamt-ECTS: ")
        start_datum = input("Startdatum (DD.MM.YYYY): ")

        return benutzername, passwort, vorname, nachname, zielnote, regelstudienzeit, sicherheitsfrage, sicherheitsantwort, studiengang_name, ects_gesamt, start_datum

    def waehle_aus_liste(self, elemente, anzeige_funktion):
        """Eine nummerierte Liste wird angezeigt und das gewählte Element zurückgegeben."""
        # Die Beschriftung wird als Funktion übergeben, dadurch lässt sich dieselbe Auswahl für Semester, Module, Prüfungsleistungen und Noten verwenden
        for index, element in enumerate(elemente, start=1):
            print(f"{index}. {anzeige_funktion(element)}")
        # Bei ungültiger Eingabe wird erneut gefragt statt abzubrechen, ein Tippfehler soll das Programm nicht beenden
        while True:
            auswahl = self.frage_int_ab("Bitte wählen Sie eine Option: ")
            if 1 <= auswahl <= len(elemente):
                # Zurückgegeben wird das Objekt selbst, damit der Aufrufer nicht mit Indizes weiterarbeiten muss
                return elemente[auswahl - 1]
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")

    def frage_semester_ab(self):
        """Die Semesternummer wird abgefragt und zurückgegeben."""
        semester_nummer = self.frage_int_ab("Semester (als Zahl): ")
        return semester_nummer

    def frage_modul_ab(self):
        """Name und ECTS-Punkte eines Moduls werden abgefragt."""
        name = input("Modulname: ")
        ects = self.frage_int_ab("ECTS-Punkte: ")
        return name, ects

    def frage_pruefungsleistung_ab(self):
        """Titel, Datum und Note einer Prüfungsleistung werden abgefragt."""
        titel = input("Prüfungsleistungstitel: ")
        datum = input("Datum (DD.MM.YYYY): ")
        # Die Auswahl kommt direkt aus Pruefungsleistung.gueltige_noten, dadurch können Anzeige und Validierung nicht auseinanderlaufen
        note = self.waehle_aus_liste(Pruefungsleistung.gueltige_noten, lambda n: f"Note: {n}")
        return titel, datum, note

    def frage_int_ab(self, prompt):
        """Es wird so lange gefragt, bis eine gültige Ganzzahl eingegeben wurde."""
        # Das wurde zentral gelöst, damit nicht an jeder Eingabestelle ein eigenes try/except steht und eine Fehleingabe nirgends das Programm beendet
        while True:
            eingabe = input(prompt)
            try:
                return int(eingabe)
            except ValueError:
                print("Ungültige Eingabe. Bitte geben Sie eine Ganzzahl ein.")

    def frage_float_ab(self, prompt):
        """Es wird so lange gefragt, bis eine gültige Gleitkommazahl eingegeben wurde."""
        while True:
            eingabe = input(prompt)
            try:
                return float(eingabe)
            except ValueError:
                print("Ungültige Eingabe. Bitte geben Sie eine Zahl ein.")

    def frage_sicherheitsantwort_ab(self, sicherheitsfrage):
        """Die Sicherheitsfrage wird angezeigt und die Antwort abgefragt."""
        print(f"Sicherheitsfrage: {sicherheitsfrage}")
        antwort = input("Antwort: ")
        return antwort

    def frage_neues_passwort_ab(self):
        """Das neue Passwort wird ohne sichtbare Eingabe abgefragt."""
        neues_passwort = getpass.getpass("Neues Passwort: ")
        return neues_passwort

    def zeige_gesamtuebersicht(self, semester_liste):
        """Alle Semester werden mit ihren Modulen und Prüfungsleistungen ausgegeben."""
        if not semester_liste:
            print("Keine Semesterinformationen verfügbar.")
            return
        for semester in semester_liste:
            print(f"\nSemester {semester.semester_nummer}:")
            for modul in semester.module:
                print(f" - {modul.name} ({modul.ects} ECTS, Status: {modul.status.value})")
                for pruefungsleistung in modul.pruefungsleistungen:
                    # Ohne Note wird ein Text angezeigt, damit in der Übersicht nicht "None" steht
                    note_text = pruefungsleistung.note if pruefungsleistung.note is not None else "Keine Note"
                    print(f"   - {pruefungsleistung.titel} ({pruefungsleistung.datum}, Note: {note_text})")

    def frage_anmeldedaten_ab(self):
        """Benutzername und Passwort werden abgefragt und als Tupel zurückgegeben."""
        # Die Abfrage liegt in der View und nicht in der Application, damit die Anmeldung denselben Weg nimmt wie die Registrierung und das Zurücksetzen des Passworts
        benutzername = input("Benutzername: ")
        passwort = getpass.getpass("Passwort: ")
        return benutzername, passwort

    def frage_benutzername_ab(self):
        """Der Benutzername wird abgefragt und zurückgegeben."""
        benutzername = input("Benutzername: ")
        return benutzername
