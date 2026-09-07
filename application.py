from repositories import JSONBenutzerkontoRepository
from services import FortschrittService
from controller import StudentController
from view import KonsolenView

class Application:
    """Der Einstiegspunkt der Anwendung mit der Menüführung."""
    def __init__(self):
        # Hier werden alle Schichten einmalig zusammengesteckt: das Repository geht in den Service, der Service in den Controller
        # Dadurch ist dies die einzige Stelle, die die konkreten Klassen kennt, alle übrigen Schichten bekommen ihre Abhängigkeiten übergeben
        self.konto_repository = JSONBenutzerkontoRepository("konten.json")
        service = FortschrittService(self.konto_repository)
        self.controller = StudentController(service)
        self.view = KonsolenView()

    def starten(self):
        """Das Hauptmenü wird angezeigt, bis der Benutzer die Anwendung beendet."""
        while True:
            print("\n--- Hauptmenü ---")
            print("1. Anmelden")
            print("2. Registrieren")
            print("3. Passwort vergessen")
            print("4. Beenden")
            wahl = input("Auswahl: ")

            if wahl == "1":
                self._anmelden()
            elif wahl == "2":
                self._registrieren()
            elif wahl == "3":
                self._passwort_vergessen()
            elif wahl == "4":
                print("Beenden der Anwendung.")
                break
            else:
                print("Ungültige Auswahl. Bitte erneut versuchen.")

    def _anmelden(self):
        """Die Anmeldedaten werden abgefragt und bei Erfolg wird das Menü des Studenten geöffnet."""
        benutzername, passwort = self.view.frage_anmeldedaten_ab()
        # Das Konto wird hier geladen und an den Controller übergeben, weil die Prüfung im Benutzerkonto selbst liegt
        konto = self.konto_repository.laden(benutzername)
        # Bei unbekanntem Benutzernamen wird dieselbe Meldung ausgegeben wie bei falschem Passwort, damit nicht erkennbar ist, welcher Teil beim Login falsch war
        if konto is None:
            self.view.zeige_login_fehler()
            return
        login_erfolg = self.controller.login_versuchen(konto, benutzername, passwort)
        if login_erfolg:
            self._hauptmenue(benutzername)
        else:
            self.view.zeige_login_fehler()

    def _passwort_vergessen(self):
        """Nach korrekter Sicherheitsantwort wird ein neues Passwort gesetzt."""
        benutzername = self.view.frage_benutzername_ab()
        konto = self.konto_repository.laden(benutzername)
        # Anders als beim Login wird hier offengelegt, dass das Konto nicht existiert
        # Das ist eine bewusste Abwägung: Ohne diese Rückmeldung wüsste der Benutzer nicht, ob er sich nur im Namen vertippt hat
        # Verbergen ließe es sich ohnehin kaum, weil im nächsten Schritt die persönliche Sicherheitsfrage des Kontos angezeigt wird
        if konto is None:
            print("Benutzerkonto existiert nicht.")
            return
        antwort = self.view.frage_sicherheitsantwort_ab(konto.sicherheitsfrage)
        # Die Antwort wird geprüft, bevor nach dem neuen Passwort gefragt wird, sonst würde der Benutzer eines eingeben, das gar nicht gesetzt werden kann
        if not self.controller.sicherheitsantwort_pruefen(self.konto_repository, benutzername, antwort):
            print("Sicherheitsantwort ist nicht korrekt.")
            return
        neues_passwort = self.view.frage_neues_passwort_ab()
        erfolg = self.controller.passwort_setzen(self.konto_repository, benutzername, neues_passwort)
        if erfolg:
            print("Passwort erfolgreich zurückgesetzt.")
        else:
            print("Fehler beim Zurücksetzen des Passworts. Bitte versuchen Sie es erneut.")

    def _hauptmenue(self, benutzername):
        """Das Menü des angemeldeten Studenten wird angezeigt, bis er sich abmeldet."""
        while True:
            print("\n--- Menü ---")
            print("1. Fortschritt anzeigen")
            print("2. Gesamtübersicht anzeigen")
            print("3. Semester hinzufügen")
            print("4. Modul hinzufügen")
            print("5. Note eintragen")
            print("6. Semester entfernen")
            print("7. Modul entfernen")
            print("8. Prüfungsleistung entfernen")
            print("9. Abmelden")
            print("10. Konto löschen")
            wahl = input("Auswahl: ")

            if wahl == "1":
                fortschritt = self.controller.fortschritt_abrufen(benutzername)
                self.view.zeige_fortschritt(fortschritt)
                # Wartet auf die Eingabe, damit die Ausgabe nicht sofort vom nächsten Menü überschrieben wird
                input("\nDrücken Sie die Eingabetaste, um fortzufahren...")
            elif wahl == "2":
                # Hier wird nichts gespeichert, deshalb wird das Konto aus dem Tupel nicht weiterverwendet
                konto, semester_liste = self.controller.semester_auflisten(benutzername, self.konto_repository)
                self.view.zeige_gesamtuebersicht(semester_liste)
                self.view.zeige_module_nach_status(semester_liste)
                # Wartet auf die Eingabe, damit die Ausgabe nicht sofort vom nächsten Menü überschrieben wird
                input("\nDrücken Sie die Eingabetaste, um fortzufahren...")
            elif wahl == "3":
                semester = self.view.frage_semester_ab()
                erfolg = self.controller.semester_hinzufuegen(benutzername, self.konto_repository, semester)
                if erfolg:
                    print("Semester erfolgreich hinzugefügt.")
                else:
                    print("Semester konnte nicht hinzugefügt werden. Semester existiert bereits.")
            elif wahl == "4":
                modul_daten = self.view.frage_modul_ab()
                # semester_auflisten gibt das Konto mit zurück, damit es anschließend für das Speichern verwendet werden kann und nicht erneut geladen werden muss
                konto, semester_liste = self.controller.semester_auflisten(benutzername, self.konto_repository)
                if not semester_liste:
                    print("Keine Semester vorhanden. Bitte zuerst ein Semester hinzufügen.")
                else:
                    gewaehltes_semester = self.view.waehle_semester_aus(semester_liste)
                    erfolg = self.controller.modul_hinzufuegen(self.konto_repository, konto, gewaehltes_semester, modul_daten)
                    if erfolg:
                        print("Modul erfolgreich hinzugefügt.")
                    else:
                        print("Modul konnte nicht hinzugefügt werden. Modul existiert bereits.")
            elif wahl == "5":
                pruefungsleistung_daten = self.view.frage_pruefungsleistung_ab()
                konto, semester_liste = self.controller.semester_auflisten(benutzername, self.konto_repository)
                if not semester_liste:
                    print("Keine Semester vorhanden. Bitte zuerst ein Semester hinzufügen.")
                else:
                    gewaehltes_semester = self.view.waehle_semester_aus(semester_liste)
                    modul_liste = self.controller.modul_auflisten(gewaehltes_semester)
                    if not modul_liste:
                        print("Keine Module vorhanden. Bitte zuerst ein Modul hinzufügen.")
                    else:
                        gewaehltes_modul = self.view.waehle_modul_aus(modul_liste)
                        # Der Setter in Pruefungsleistung wirft bei einer ungültigen Note einen ValueError, der hier abgefangen wird, damit das Programm nicht abbricht
                        try:
                            self.controller.pruefungsleistung_eintragen(self.konto_repository, konto, gewaehltes_modul, pruefungsleistung_daten)
                            print("Prüfungsleistung erfolgreich eingetragen.")
                        except ValueError as e:
                            print(f"Fehler beim Eintragen der Prüfungsleistung: {e}")
            elif wahl == "6":
                konto, semester_liste = self.controller.semester_auflisten(benutzername, self.konto_repository)
                if not semester_liste:
                    print("Keine Semester vorhanden, es kann nichts entfernt werden.")
                else:
                    gewaehltes_semester = self.view.waehle_semester_aus(semester_liste)
                    self.controller.semester_entfernen(self.konto_repository, konto, gewaehltes_semester)
                    print("Semester erfolgreich entfernt.")
            elif wahl == "7":
                konto, semester_liste = self.controller.semester_auflisten(benutzername, self.konto_repository)
                if not semester_liste:
                    print("Keine Semester vorhanden, es kann kein Modul entfernt werden.")
                else:
                    gewaehltes_semester = self.view.waehle_semester_aus(semester_liste)
                    modul_liste = self.controller.modul_auflisten(gewaehltes_semester)
                    if not modul_liste:
                        print("Keine Module vorhanden, es kann nichts entfernt werden.")
                    else:
                        gewaehltes_modul = self.view.waehle_modul_aus(modul_liste)
                        self.controller.modul_entfernen(self.konto_repository, konto, gewaehltes_semester, gewaehltes_modul)
                        print("Modul erfolgreich entfernt.")
            elif wahl == "8":
                konto, semester_liste = self.controller.semester_auflisten(benutzername, self.konto_repository)
                if not semester_liste:
                    print("Keine Semester vorhanden, es kann keine Prüfungsleistung entfernt werden.")
                else:
                    gewaehltes_semester = self.view.waehle_semester_aus(semester_liste)
                    modul_liste = self.controller.modul_auflisten(gewaehltes_semester)
                    if not modul_liste:
                        print("Keine Module vorhanden, es kann keine Prüfungsleistung entfernt werden.")
                    else:
                        gewaehltes_modul = self.view.waehle_modul_aus(modul_liste)
                        pruefungsleistung_liste = gewaehltes_modul.pruefungsleistungen
                        if not pruefungsleistung_liste:
                            print("Keine Prüfungsleistungen vorhanden, es kann nichts entfernt werden.")
                        else:
                            gewaehlte_pruefungsleistung = self.view.waehle_pruefungsleistung_aus(pruefungsleistung_liste)
                            self.controller.pruefungsleistung_entfernen(self.konto_repository, konto, gewaehltes_modul, gewaehlte_pruefungsleistung)
                            print("Prüfungsleistung erfolgreich entfernt.")
            elif wahl == "9":
                print("Abmeldung erfolgreich.")
                break
            elif wahl == "10":
                # Das Löschen ist nicht rückgängig zu machen, deshalb die ausdrückliche Bestätigung
                bestaetigung = input("Sind Sie sicher, dass Sie Ihr Konto löschen möchten? (ja/nein): ")
                if bestaetigung.lower() == "ja":
                    erfolg = self.controller.konto_loeschen(benutzername, self.konto_repository)
                    if erfolg:
                        print("Konto erfolgreich gelöscht. Sie werden abgemeldet.")
                        break
                    else:
                        print("Fehler beim Löschen des Kontos.")
                else:
                    print("Abgebrochen.")
            else:
                print("Ungültige Auswahl. Bitte erneut versuchen.")

    def _registrieren(self):
        """Die Registrierungsdaten werden abgefragt und ein neues Konto angelegt."""
        daten = self.view.frage_registrierungsdaten_ab()
        # Die View liefert alle Werte als Tupel, das mit * in die einzelnen Parameter von registrieren entpackt wird
        konto = self.controller.registrieren(self.konto_repository, *daten)
        if konto is None:
            print("Registrierung fehlgeschlagen. Benutzername existiert bereits.")
        else:
            print("Registrierung erfolgreich. Sie können sich jetzt anmelden.")

# Nur beim direkten Ausführen startet die Anwendung, beim Import als Modul passiert nichts
if __name__ == "__main__":
    try:
        app = Application()
        app.starten()
    except RuntimeError as fehler:
        print(f"\nEin schwerwiegender Fehler ist aufgetreten: {fehler}")
        print("Das Programm wird beendet.")
