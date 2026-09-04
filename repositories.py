from abc import ABC, abstractmethod
import jsonpickle


class BenutzerkontoRepository(ABC):                                 # Abstrakte Basisklasse für das BenutzerkontoRepository
    @abstractmethod
    def speichern(self, konto):                                     # Abstrakte Methode zum Speichern eines Benutzerkontos
        pass

    @abstractmethod
    def laden(self, benutzername):                                  # Abstrakte Methode zum Laden eines Benutzerkontos
        pass

    @abstractmethod
    def loeschen(self, benutzername):                               # Abstrakte Methode zum Löschen eines Benutzerkontos
        pass

class JSONBenutzerkontoRepository(BenutzerkontoRepository):         # Implementierung des BenutzerkontoRepository für JSON-Dateien
    def __init__(self, dateipfad):                                  # Initialisiert das Repository mit einem Dateipfad
        self.dateipfad = dateipfad

    def speichern(self, konto):                                     # Speichert ein Benutzerkonto in einer JSON-Datei
        konten = self._alle_laden()                                 # Lädt alle vorhandenen Konten
        konten[konto.benutzername.strip().lower()] = konto          # Speichert das Benutzerkonto im Dictionary, wobei der Schlüssel der normalisierte Benutzername ist
        with open(self.dateipfad, 'w') as datei:                    # Öffnet die Datei im Schreibmodus
            datei.write(jsonpickle.encode(konten))                  # Serialisiert alle Benutzerkonten und schreibt sie in die Datei

    def laden(self, benutzername):                                  # Lädt ein Benutzerkonto aus einer JSON-Datei
        konten = self._alle_laden()                                 # Lädt alle vorhandenen Konten
        return konten.get(benutzername.strip().lower())             # Gibt das Benutzerkonto für den angegebenen Benutzernamen zurück, oder None, wenn es nicht gefunden wurde

    def _alle_laden(self):                                          # Hilfsmethode zum Laden aller Benutzerkonten
        try:
            with open(self.dateipfad, 'r') as datei:                # Öffnet die Datei im Lesemodus
                inhalt = datei.read()                               # Liest den Inhalt der Datei
                if not inhalt:                                      # Überprüft, ob die Datei leer ist
                    return {}                                       # Gibt ein leeres Dictionary zurück, wenn die Datei leer ist
                return jsonpickle.decode(inhalt)                    # Deserialisiert und gibt alle Benutzerkonten zurück
        except FileNotFoundError:                                   # Fängt den Fehler ab, wenn die Datei nicht gefunden wird
            return {}                                               # Gibt ein leeres Dictionary zurück, wenn keine Konten vorhanden sind
        except Exception as fehler:                                 # Fängt alle anderen Fehler ab, die beim Laden der Datei auftreten können
            # Wirft einen RuntimeError, um auf die beschädigte Datei hinzuweisen und Datenverlust zu vermeiden
            raise RuntimeError(f"Die Datei {self.dateipfad} ist beschädigt oder kann nicht gelesen werden. Um Dateiverlust zu vermeiden, wird die Datei nicht automatisch überschrieben.") from fehler

    def loeschen(self, benutzername):                               # Löscht ein Benutzerkonto aus der JSON-Datei
        konten = self._alle_laden()                                 # Lädt alle vorhandenen Konten
        if benutzername.strip().lower() in konten:                  # Überprüft, ob das Benutzerkonto existiert
            del konten[benutzername.strip().lower()]                # Löscht das Benutzerkonto
            with open(self.dateipfad, 'w') as datei:                # Öffnet die Datei im Schreibmodus
                datei.write(jsonpickle.encode(konten))              # Serialisiert die verbleibenden Konten und schreibt sie in die Datei
            return True                                             # Gibt True zurück, wenn das Konto erfolgreich gelöscht wurde
        return False                                                # Gibt False zurück, wenn das Konto nicht gefunden wurde

# Quelle: https://www.youtube.com/watch?v=97V7ICVeTJc
# Quelle: https://pypi.org/project/jsonpickle/