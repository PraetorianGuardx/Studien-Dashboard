from repositories import JSONBenutzerkontoRepository
from services import FortschrittService
from controller import StudentController
from view import KonsolenView

class Application:                                                                      # Bauplan für die Anwendung
    def __init__(self):
        self.konto_repository = JSONBenutzerkontoRepository("konten.json")              # Initialisiert das Benutzerkonto-Repository mit dem Dateipfad "konten.json"
        service = FortschrittService(self.konto_repository)                             # Initialisiert den FortschrittService mit dem Benutzerkonto-Repository
        self.controller = StudentController(service)                                    # Initialisiert den StudentController mit dem Fortschritt
        self.view = KonsolenView()                                                      # Initialisiert die Konsolenansicht

    def starten(self):
        while True:                                                                     # Endlosschleife für die Anwendung
            print("\n--- Hauptmenü ---")                                                # Gibt das Hauptmenü aus
            print("1. Anmelden")                                                        # Gibt die Option "Anmelden" aus
            print("2. Registrieren")                                                    # Gibt die Option "Registrieren" aus
            print("3. Passwort vergessen")                                              # Gibt die Option "Passwort vergessen" aus
            print("4. Beenden")                                                         # Gibt die Option "Beenden" aus
            wahl = input("Auswahl: ")                                                   # Fragt den Benutzer nach einer Auswahl

            if wahl == "1":                                                             # Wenn der Benutzer "1" wählt, wird der Login-Prozess gestartet
                self._anmelden()                                                        # Aufruf der Methode _anmelden, um den Anmeldeprozess zu starten
            elif wahl == "2":                                                           # Wenn der Benutzer "2" wählt, wird der Registrierungsprozess gestartet
                self._registrieren()                                                    # Aufruf der Methode _registrieren, um den Registrierungsprozess zu starten
            elif wahl == "3":                                                           # Wenn der Benutzer "3" wählt, wird der Passwort-Zurücksetzen-Prozess gestartet
                self._passwort_zuruecksetzen()                                          # Aufruf der Methode _passwort_zuruecksetzen, um den Passwort-Zurücksetzen-Prozess zu starten
            elif wahl == "4":                                                           # Wenn der Benutzer "4" wählt, wird die Anwendung beendet
                print("Beenden der Anwendung.")
                break                                                                   # Beendet die Endlosschleife und somit die Anwendung
            else:                                                                       # Wenn der Benutzer eine ungültige Auswahl trifft, wird eine Fehlermeldung ausgegeben
                print("Ungültige Auswahl. Bitte erneut versuchen.")

    def _anmelden(self):
        benutzername = input("Benutzername: ")                                          # Fragt den Benutzer nach dem Benutzernamen
        passwort = input("Passwort: ")                                                  # Fragt den Benutzer nach dem Passwort
        konto = self.konto_repository.laden(benutzername)                               # Lädt das Benutzerkonto aus dem Repository
        if konto is None:                                                               # Wenn das Konto nicht existiert, wird eine Fehlermeldung ausgegeben
            self.view.zeige_login_fehler()                                              # Wenn das Konto nicht existiert, wird eine Fehlermeldung ausgegeben
            return
        login_erfolg = self.controller.login_versuchen(konto, benutzername, passwort)   # Versucht, den Benutzer anzumelden
        if login_erfolg:                                                                # Wenn die Anmeldung erfolgreich war, wird der Fortschritt des Benutzers angezeigt
            self._hauptmenue(benutzername)                                              # Aufruf der Methode _hauptmenue, um das Hauptmenü anzuzeigen
        else:                                                                           # Wenn die Anmeldung fehlschlägt, wird eine Fehlermeldung ausgegeben
            self.view.zeige_login_fehler()                                              # Wenn die Anmeldung fehlschlägt, wird eine Fehlermeldung ausgegeben

    def _passwort_vergessen(self):                                                      # Methode für den Passwort-Vergessen-Prozess
        benutzername = input("Benutzername: ")                                          # Fragt den Benutzer nach dem Benutzernamen
        konto = self.konto_repository.laden(benutzername)                               # Lädt das Benutzerkonto aus dem Repository
        if konto is None:                                                               # Wenn das Konto nicht existiert, wird eine Fehlermeldung ausgegeben
            print("Benutzerkonto existiert nicht.")                                     # Gibt eine Fehlermeldung aus, wenn das Benutzerkonto nicht existiert
            return
        antwort = self.view.frage_sicherheitsantwort_ab(konto.sicherheitsfrage)                                                                         # Fragt den Benutzer nach der Antwort auf die Sicherheitsfrage
        neues_passwort = self.view.frage_neues_passwort_ab()                                                                                            # Fragt den Benutzer nach einem neuen Passwort
        erfolg = self.controller.passwort_zuruecksetzen(self.konto_repository, benutzername, antwort, neues_passwort)                                   # Versucht, das Passwort zurückzusetzen
        if erfolg:                                                                                                                                      # Wenn das Passwort erfolgreich zurückgesetzt wurde, wird eine Erfolgsmeldung ausgegeben
            print("Passwort erfolgreich zurückgesetzt.")                                                                                                # Gibt eine Erfolgsmeldung aus, wenn das Passwort erfolgreich zurückgesetzt wurde
        else:                                                                                                                                           # Wenn das Zurücksetzen des Passworts fehlschlägt, wird eine Fehlermeldung ausgegeben
            print("Fehler beim Zurücksetzen des Passworts. Bitte überprüfen Sie Ihre Eingaben.")                                                        # Gibt eine Fehlermeldung aus, wenn das Zurücksetzen des Passworts fehlschlägt

    def _hauptmenue(self, benutzername):                                                # Methode für das Hauptmenü nach erfolgreicher Anmeldung
        while True:                                                                     # Endlosschleife für das Hauptmenü
            print("\n--- Menü ---")                                                     # Gibt das Hauptmenü aus
            print("1. Fortschritt anzeigen")                                            # Gibt die Option "Fortschritt anzeigen" aus
            print("2. Semester hinzufügen")                                             # Gibt die Option "Semester hinzufügen" aus
            print("3. Modul zu Semester hinzufügen")                                    # Gibt die Option "Modul zu Semester hinzufügen" aus
            print("4. Note eintragen")                                                  # Gibt die Option "Note eintragen" aus
            print("5. Semester entfernen")                                              # Gibt die Option "Semester entfernen" aus
            print("6. Modul entfernen")                                                 # Gibt die Option "Modul entfernen" aus
            print("7. Prüfungsleistung entfernen")                                      # Gibt die Option "Prüfungsleistung entfernen" aus
            print("8. Abmelden")                                                        # Gibt die Option "Abmelden" aus
            print("9. Konto löschen")                                                   # Gibt die Option "Konto löschen" aus
            wahl = input("Auswahl: ")                                                   # Fragt den Benutzer nach einer Auswahl

            if wahl == "1":                                                                                                                             # Wenn der Benutzer "1" wählt, wird der Fortschritt angezeigt
                fortschritt = self.controller.fortschritt_abrufen(benutzername)                                                                         # Ruft den Fortschritt des Benutzers ab
                self.view.zeige_fortschritt(fortschritt)                                                                                                # Zeigt den Fortschritt des Benutzers an
                input("\nDrücken Sie die Eingabetaste, um fortzufahren...")                                                                             # Wartet auf die Eingabe des Benutzers, bevor das Menü erneut angezeigt wird
            elif wahl == "2":                                                                                                                           # Wenn der Benutzer "2" wählt, wird das Semester hinzugefügt
                semester = self.view.frage_semester_ab()                                                                                                # Fragt nach dem neuen Semester
                self.controller.semester_hinzufuegen(benutzername, self.konto_repository, semester)                                                     # Fügt das Semester hinzu
            elif wahl == "3":                                                                                                                           # Wenn der Benutzer "3" wählt, wird das Modul hinzugefügt
                modul_daten = self.view.frage_modul_ab()                                                                                                # Fragt nach dem neuen Modul
                konto, semester_liste = self.controller.semester_auflisten(benutzername, self.konto_repository)                                         # Ruft die Liste der Semester des Benutzers ab
                if not semester_liste:                                                                                                                  # Wenn keine Semester vorhanden sind, wird eine Fehlermeldung ausgegeben
                    print("Keine Semester vorhanden. Bitte zuerst ein Semester hinzufügen.")
                else:                                                                                                                                   # Wenn Semester vorhanden sind, wird das Modul hinzugefügt
                    gewaehltes_semester = self.view.waehle_aus_liste(semester_liste, lambda s: f"Semester {s.semester_nummer}")                         # Fragt den Benutzer, in welches Semester das Modul hinzugefügt werden soll
                    erfolg = self.controller.modul_hinzufuegen(self.konto_repository, konto, gewaehltes_semester, modul_daten)                          # Fügt das Modul hinzu und gibt den Erfolg zurück
                    if erfolg:                                                                                                                          # Wenn das Modul erfolgreich hinzugefügt wurde, wird eine Erfolgsmeldung ausgegeben
                        print("Modul erfolgreich hinzugefügt.")
                    else:                                                                                                                               # Wenn das Modul nicht hinzugefügt werden konnte, wird eine Fehlermeldung ausgegeben
                        print("Modul konnte nicht hinzugefügt werden. Modul existiert bereits.")
            elif wahl == "4":                                                                                                                           # Wenn der Benutzer "4" wählt, wird die Note eingetragen
                pruefungsleistung_daten = self.view.frage_pruefungsleistung_ab()                                                                        # Fragt nach den Daten der Prüfungsleistung
                konto, semester_liste = self.controller.semester_auflisten(benutzername, self.konto_repository)                                         # Ruft die Liste der Semester des Benutzers ab
                if not semester_liste:                                                                                                                  # Wenn keine Semester vorhanden sind, wird eine Fehlermeldung ausgegeben
                    print("Keine Semester vorhanden. Bitte zuerst ein Semester hinzufügen.")
                else:                                                                                                                                   # Wenn Semester vorhanden sind, wird die Note eingetragen
                    gewaehltes_semester = self.view.waehle_aus_liste(semester_liste, lambda s: f"Semester {s.semester_nummer}")                         # Fragt den Benutzer, in welches Semester die Note eingetragen werden soll
                    modul_liste = self.controller.modul_auflisten(gewaehltes_semester)                                                                  # Ruft die Liste der Module des gewählten Semesters ab
                    if not modul_liste:                                                                                                                 # Wenn keine Module vorhanden sind, wird eine Fehlermeldung ausgegeben
                        print("Keine Module vorhanden. Bitte zuerst ein Modul hinzufügen.")
                    else:                                                                                                                               # Wenn Module vorhanden sind, wird die Note eingetragen
                        gewaehltes_modul = self.view.waehle_aus_liste(modul_liste, lambda m: f"{m.name} ({m.ects} ECTS)")                               # Fragt den Benutzer, in welches Modul die Note eingetragen werden soll
                        try:                                                                                                                            # Fängt mögliche ValueError ab, die beim Eintragen der Prüfungsleistung auftreten können
                            self.controller.pruefungsleistung_eintragen(self.konto_repository, konto, gewaehltes_modul, pruefungsleistung_daten)        # Trägt die Note in das gewählte Modul ein
                        except ValueError as e:                                                                                                         # Fängt ValueError ab, die beim Eintragen der Prüfungsleistung auftreten können
                            print(f"Fehler beim Eintragen der Prüfungsleistung: {e}")                                                                   # Gibt eine Fehlermeldung aus, wenn ein Fehler beim Eintragen der Prüfungsleistung auftritt
            elif wahl == "5":                                                                                                                           # Wenn der Benutzer "5" wählt, wird das Semester entfernt
                konto, semester_liste = self.controller.semester_auflisten(benutzername, self.konto_repository)                                         # Ruft die Liste der Semester des Benutzers ab
                if not semester_liste:                                                                                                                  # Wenn keine Semester vorhanden sind, wird eine Fehlermeldung ausgegeben
                    print("Keine Semester vorhanden. Bitte zuerst ein Semester hinzufügen.")
                else:                                                                                                                                   # Wenn Semester vorhanden sind, wird das gewählte Semester entfernt
                    gewaehltes_semester = self.view.waehle_aus_liste(semester_liste, lambda s: f"Semester {s.semester_nummer}")                         # Fragt den Benutzer, welches Semester entfernt werden soll
                    self.controller.semester_entfernen(self.konto_repository, konto, gewaehltes_semester)                                               # Entfernt das gewählte Semester
                    print("Semester erfolgreich entfernt.")
            elif wahl == "6":                                                                                                                           # Wenn der Benutzer "6" wählt, wird das Modul entfernt
                konto, semester_liste = self.controller.semester_auflisten(benutzername, self.konto_repository)                                         # Ruft die Liste der Semester des Benutzers ab
                if not semester_liste:                                                                                                                  # Wenn keine Semester vorhanden sind, wird eine Fehlermeldung ausgegeben
                    print("Keine Semester vorhanden. Bitte zuerst ein Semester hinzufügen.")
                else:                                                                                                                                   # Wenn Semester vorhanden sind, wird das gewählte Modul entfernt
                    gewaehltes_semester = self.view.waehle_aus_liste(semester_liste, lambda s: f"Semester {s.semester_nummer}")                         # Fragt den Benutzer, aus welchem Semester das Modul entfernt werden soll
                    modul_liste = self.controller.modul_auflisten(gewaehltes_semester)                                                                  # Ruft die Liste der Module des gewählten Semesters ab
                    if not modul_liste:                                                                                                                 # Wenn keine Module vorhanden sind, wird eine Fehlermeldung ausgegeben
                        print("Keine Module vorhanden. Bitte zuerst ein Modul hinzufügen.")
                    else:                                                                                                                               # Wenn Module vorhanden sind, wird das gewählte Modul entfernt
                        gewaehltes_modul = self.view.waehle_aus_liste(modul_liste, lambda m: f"{m.name} ({m.ects} ECTS)")                               # Fragt den Benutzer, welches Modul entfernt werden soll
                        self.controller.modul_entfernen(self.konto_repository, konto, gewaehltes_semester, gewaehltes_modul)                            # Entfernt das gewählte Modul
                        print("Modul erfolgreich entfernt.")
            elif wahl == "7":                                                                                                                           # Wenn der Benutzer "7" wählt, wird die Prüfungsleistung entfernt
                konto, semester_liste = self.controller.semester_auflisten(benutzername, self.konto_repository)                                         # Ruft die Liste der Semester des Benutzers ab
                if not semester_liste:                                                                                                                  # Wenn keine Semester vorhanden sind, wird eine Fehlermeldung ausgegeben
                    print("Keine Semester vorhanden. Bitte zuerst ein Semester hinzufügen.")
                else:                                                                                                                                   # Wenn Semester vorhanden sind, wird die gewählte Prüfungsleistung entfernt
                    gewaehltes_semester = self.view.waehle_aus_liste(semester_liste, lambda s: f"Semester {s.semester_nummer}")                         # Fragt den Benutzer, aus welchem Semester die Prüfungsleistung entfernt werden soll
                    modul_liste = self.controller.modul_auflisten(gewaehltes_semester)                                                                  # Ruft die Liste der Module des gewählten Semesters ab
                    if not modul_liste:                                                                                                                 # Wenn keine Module vorhanden sind, wird eine Fehlermeldung ausgegeben
                        print("Keine Module vorhanden. Bitte zuerst ein Modul hinzufügen.")
                    else:                                                                                                                               # Wenn Module vorhanden sind, wird die gewählte Prüfungsleistung entfernt
                        gewaehltes_modul = self.view.waehle_aus_liste(modul_liste, lambda m: f"{m.name} ({m.ects} ECTS)")                               # Fragt den Benutzer, aus welchem Modul die Prüfungsleistung entfernt werden soll
                        pruefungsleistung_liste = gewaehltes_modul.pruefungsleistungen                                                                  # Ruft die Liste der Prüfungsleistungen des gewählten Moduls ab
                        if not pruefungsleistung_liste:                                                                                                 # Wenn keine Prüfungsleistungen vorhanden sind, wird eine Fehlermeldung ausgegeben
                            print("Keine Prüfungsleistungen vorhanden. Bitte zuerst eine Prüfungsleistung eintragen.")
                        else:                                                                                                                           # Wenn Prüfungsleistungen vorhanden sind, wird die gewählte Prüfungsleistung entfernt
                            gewaehlte_pruefungsleistung = self.view.waehle_aus_liste(pruefungsleistung_liste, lambda p: f"{p.titel} ({p.datum})")       # Fragt den Benutzer, welche Prüfungsleistung entfernt werden soll
                            self.controller.pruefungsleistung_entfernen(self.konto_repository, konto, gewaehltes_modul, gewaehlte_pruefungsleistung)    # Entfernt die gewählte Prüfungsleistung
                            print("Prüfungsleistung erfolgreich entfernt.")
            elif wahl == "8":                                                                                                                           # Wenn der Benutzer "8" wählt, wird die Schleife beendet und der Benutzer abgemeldet
                print("Abmeldung erfolgreich.")
                break
            elif wahl == "9":                                                                                                                           # Wenn der Benutzer "9" wählt, wird das Konto gelöscht
                bestaetigung = input("Sind Sie sicher, dass Sie Ihr Konto löschen möchten? (ja/nein): ")                                                # Fragt den Benutzer nach einer Bestätigung zur Kontolöschung
                if bestaetigung.lower() == "ja":                                                                                                        # Wenn der Benutzer "ja" eingibt, wird das Konto gelöscht
                    self.controller.konto_loeschen(benutzername, self.konto_repository)                                                                 # Löscht das Benutzerkonto
                    print("Konto erfolgreich gelöscht. Die Anwendung wird beendet.")                                                                    # Gibt eine Erfolgsmeldung aus und beendet die Anwendung
                    break                                                                                                                               # Beendet die Schleife und somit die Anwendung
                else:
                    print("Abgebrochen.")                                                                                                               # Gibt eine Abbruchmeldung aus, wenn der Benutzer die Kontolöschung abbricht                                                                                             
            else:                                                                                                                                       # Wenn der Benutzer eine ungültige Auswahl trifft, wird eine Fehlermeldung ausgegeben
                print("Ungültige Auswahl. Bitte erneut versuchen.")                                                                                     # Gibt eine Fehlermeldung aus, wenn der Benutzer eine ungültige Auswahl trifft

    def _registrieren(self):
        daten = self.view.frage_registrierungsdaten_ab()                                # Fragt die Registrierungsdaten vom Benutzer ab
        konto = self.controller.registrieren(self.konto_repository, *daten)             # Registriert den Benutzer mit den abgefragten Daten
        if konto is None:                                                               # Wenn der Benutzername bereits existiert, wird eine Fehlermeldung ausgegeben
            print("Registrierung fehlgeschlagen. Benutzername existiert bereits.")
        else:                                                                           # Wenn die Registrierung erfolgreich war, wird eine Erfolgsmeldung ausgegeben
            print("Registrierung erfolgreich. Sie können sich jetzt anmelden.")

if __name__ == "__main__":                                                              # Wenn die Datei direkt ausgeführt wird, wird die Anwendung gestartet
    app = Application()                                                                 # Erstellt eine Instanz der Anwendung
    app.starten()                                                                       # Startet die Anwendung