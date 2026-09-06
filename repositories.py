from abc import ABC, abstractmethod
import jsonpickle


class BenutzerkontoRepository(ABC):
    """Schnittstelle für das dauerhafte Speichern von Benutzerkonten."""
    # Als abstrakte Klasse angelegt, damit Service- und Controller-Schicht nur gegen diese Schnittstelle arbeiten
    # Eine spätere Umstellung auf eine Datenbank wäre eine neue Unterklasse, ohne dass sich die übrigen Schichten ändern müssten
    @abstractmethod
    def speichern(self, konto):
        """Ein Benutzerkonto wird gespeichert, ein bereits vorhandenes wird dabei ersetzt."""
        pass

    @abstractmethod
    def laden(self, benutzername):
        """Das Benutzerkonto wird zum Benutzernamen zurückgegeben, sonst None."""
        pass

    @abstractmethod
    def loeschen(self, benutzername):
        """Das Benutzerkonto wird entfernt und True wird zurückgegeben, falls es vorhanden ist."""
        pass

class JSONBenutzerkontoRepository(BenutzerkontoRepository):
    """Dateibasierte Umsetzung des BenutzerkontoRepository, die alle Konten gemeinsam in einer JSON-Datei hält."""
    # jsonpickle schreibt die Objektstruktur direkt in die Datei, aus diesem Grund stehen dort Angaben wie "py/object": "benutzerkonto.Benutzerkonto"
    # Das Dateiformat ist dadurch eng an die Klasse gekoppelt, würde eine Klasse umbenannt oder in ein anderes Modul verschoben werden, ließe sich die bestehende konten.json nicht mehr laden
    # Für dieses Projekt ist das vertretbar, weil nur diese Anwendung auf die Datei zugreift, für ein echtes Mehrbenutzersystem wäre ein reines JSON oder eine Datenbank in Zukunft die bessere Wahl
    def __init__(self, dateipfad):
        self.dateipfad = dateipfad

    def speichern(self, konto):
        """Das Konto wird in der Datei gespeichert oder ersetzt, falls es bereits vorhanden ist."""
        # Alle Konten liegen gemeinsam in einem Dictionary, deshalb wird die Datei vollständig gelesen, ergänzt und neu geschrieben
        konten = self._alle_laden()
        # Der normalisierte Benutzername dient als Schlüssel, damit "Müller" und "müller" nicht als zwei getrennte Konten angelegt werden können
        konten[konto.benutzername.strip().lower()] = konto
        # Die Kodierung wird ausdrücklich gesetzt, sonst richtet sich Python nach der Einstellung des Betriebssystems
        # Eine unter Windows geschriebene Datei ließe sich sonst auf einem anders eingestellten System nicht zuverlässig lesen
        with open(self.dateipfad, "w", encoding = "utf-8") as datei:
            datei.write(jsonpickle.encode(konten))

    def laden(self, benutzername):
        """Das Benutzerkonto wird zum Benutzernamen zurückgegeben, sonst None."""
        konten = self._alle_laden()
        return konten.get(benutzername.strip().lower())

    def _alle_laden(self):
        """Alle Benutzerkonten werden aus der Datei ausgelesen und als Dictionary zurückgegeben."""
        try:
            with open(self.dateipfad, "r", encoding = "utf-8") as datei:
                inhalt = datei.read()
                # Eine leere Datei gilt nicht als Fehler, sondern ist der Zustand vor der ersten Registrierung
                if not inhalt:
                    return {}
                return jsonpickle.decode(inhalt)
        # Eine fehlende Datei ist ebenfalls normal beim allerersten Start
        except FileNotFoundError:
            return {}
        # Alle übrigen Fehler werden bewusst nicht verschluckt, sondern weitergereicht
        # Würde hier stattdessen ein leeres Dictionary zurückgegeben, würde der nächste Speichervorgang die beschädigte Datei mit einem einzigen Konto überschreiben
        # Alle übrigen Konten würden unwiderruflich gelöscht werden
        except Exception as fehler:
            raise RuntimeError(f"Die Datei {self.dateipfad} ist beschädigt oder kann nicht gelesen werden. Um Datenverlust zu vermeiden, wird die Datei nicht automatisch überschrieben.") from fehler

    def loeschen(self, benutzername):
        """Das Benutzerkonto wird entfernt und True wird zurückgegeben, falls es vorhanden ist."""
        konten = self._alle_laden()
        if benutzername.strip().lower() in konten:
            del konten[benutzername.strip().lower()]
            with open(self.dateipfad, "w",encoding = "utf-8") as datei:
                datei.write(jsonpickle.encode(konten))
            return True
        return False