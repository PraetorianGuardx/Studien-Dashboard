from modelle import Pruefungsleistung, Modulstatus
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
        print(f"Regelstudienzeit: {fortschritt['regelstudienzeit']}")
        # Der Prozentwert macht den Fortschritt sofort einschätzbar, die reine ECTS-Zahl sagt ohne Bezugsgröße wenig aus
        prozent = 0.0
        if fortschritt["ects_gesamt"] > 0:
            prozent = fortschritt["ects_erreicht"] / fortschritt["ects_gesamt"] * 100
        print(f"Erreichte ECTS: {fortschritt['ects_erreicht']} von {fortschritt['ects_gesamt']} ({prozent:.1f} %)")
        # Ohne abgeschlossenes Modul liefert der Service None, statt "None" wird hier ein verständlicher Satz ausgegeben
        if fortschritt["notendurchschnitt"] is None:
            print("Notendurchschnitt: noch kein abgeschlossenes Modul bewertet")
        else:
            print(f"Notendurchschnitt: {fortschritt['notendurchschnitt']:.2f} (Ziel: {fortschritt['zielnote']})")

    def zeige_login_fehler(self):
        """Eine Fehlermeldung zur fehlgeschlagenen Anmeldung wird ausgegeben."""
        print("Login fehlgeschlagen. Bitte überprüfen Sie Ihren Benutzernamen und Ihr Passwort.")

    def frage_registrierungsdaten_ab(self):
        """Alle Registrierungsdaten werden abgefragt und als Tupel zurückgegeben."""
        # Die Abfrage ist in drei Blöcke gruppiert, damit der Benutzer nicht zwischen Konto- und Studiendaten hin und her springen muss
        print("\n--- Zugangsdaten ---")
        benutzername = input("Benutzername: ")
        # getpass statt input, damit das Passwort nicht sichtbar in der Konsole und im Verlauf stehen bleibt
        passwort = getpass.getpass("Passwort: ")
        sicherheitsfrage = input("Sicherheitsfrage: ")
        sicherheitsantwort = input("Sicherheitsantwort: ")

        print("\n--- Persönliche Daten ---")
        vorname = input("Vorname: ")
        nachname = input("Nachname: ")

        print("\n--- Studium ---")
        studiengang_name = input("Studiengang: ")
        ects_gesamt = self.frage_int_ab("Gesamt-ECTS: ")
        start_datum = input("Startdatum (DD.MM.YYYY): ")
        regelstudienzeit = self.frage_int_ab("Regelstudienzeit (Angabe in Semestern): ")
        zielnote = self.frage_float_ab("Zielnote: ")

        # Die Reihenfolge im Tupel bleibt unverändert, weil registrieren() im Controller die Werte genauso erwartet
        return benutzername, passwort, vorname, nachname, zielnote, regelstudienzeit, sicherheitsfrage, sicherheitsantwort, studiengang_name, ects_gesamt, start_datum

    def waehle_aus_liste(self, elemente, beschriftungen):
        """Eine nummerierte Liste wird angezeigt und das gewählte Element zurückgegeben."""
        # Die Beschriftung wird als zweite Liste übergeben, dadurch lässt sich dieselbe Auswahl für Semester, Module, Prüfungsleistungen und Noten verwenden
        for index, beschriftung in enumerate(beschriftungen, start=1):
            print(f"{index}. {beschriftung}")
        # Bei ungültiger Eingabe wird erneut gefragt statt abzubrechen, ein Tippfehler soll das Programm nicht beenden
        while True:
            auswahl = self.frage_int_ab("Bitte wählen Sie eine Option: ")
            if 1 <= auswahl <= len(elemente):
                # Zurückgegeben wird das Objekt selbst, damit der Aufrufer nicht mit Indizes weiterarbeiten muss
                return elemente[auswahl - 1]
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")

    def waehle_semester_aus(self, semester_liste):
        """Ein Semester wird aus der übergebenen Liste ausgewählt und zurückgegeben."""
        beschriftungen = []
        for semester in semester_liste:
            beschriftungen.append(f"Semester {semester.semester_nummer}")
        return self.waehle_aus_liste(semester_liste, beschriftungen)

    def waehle_modul_aus(self, modul_liste):
        """Ein Modul wird aus der übergebenen Liste ausgewählt und zurückgegeben."""
        beschriftungen = []
        for modul in modul_liste:
            beschriftungen.append(f"{modul.name} ({modul.ects} ECTS)")
        return self.waehle_aus_liste(modul_liste, beschriftungen)

    def waehle_pruefungsleistung_aus(self, pruefungsleistung_liste):
        """Eine Prüfungsleistung wird aus der übergebenen Liste ausgewählt und zurückgegeben."""
        beschriftungen = []
        for pruefungsleistung in pruefungsleistung_liste:
            beschriftungen.append(f"{pruefungsleistung.titel} ({pruefungsleistung.datum})")
        return self.waehle_aus_liste(pruefungsleistung_liste, beschriftungen)

    def waehle_note_aus(self):
        """Eine Note wird aus den gültigen Notenstufen ausgewählt und zurückgegeben."""
        beschriftungen = []
        for note in Pruefungsleistung.gueltige_noten:
            beschriftungen.append(f"Note: {note}")
        return self.waehle_aus_liste(Pruefungsleistung.gueltige_noten, beschriftungen)

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
        note = self.waehle_note_aus()
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
                    if pruefungsleistung.note is None:
                        note_text = "Keine Note"
                    else:
                        note_text = pruefungsleistung.note
                    print(f"   - {pruefungsleistung.titel} ({pruefungsleistung.datum}, Note: {note_text})")

    def zeige_module_nach_status(self, semester_liste):
        """Alle Module werden nach ihrem Status gruppiert und ausgegeben."""
        # Die Reihenfolge kommt direkt aus dem Enum, dadurch bleibt sie automatisch richtig, falls ein Status ergänzt wird
        for status in Modulstatus:
            print(f"\n{status.value.capitalize()}:")
            gefunden = False
            for semester in semester_liste:
                for modul in semester.module:
                    if modul.status == status:
                        print(f" - {modul.name} ({modul.ects} ECTS, Semester {semester.semester_nummer})")
                        gefunden = True
            if not gefunden:
                print(" - keine Module")

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
