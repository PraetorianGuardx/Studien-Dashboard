from abc import ABC, abstractmethod
from modelle import Student
import json

class StudentRepository(ABC):                       # Abstrakte Basisklasse für das StudentRepository
    @abstractmethod
    def speichern(self, student):                   # Abstrakte Methode zum Speichern eines Studenten
        pass

    @abstractmethod
    def laden(self, benutzername):                  # Abstrakte Methode zum Laden eines Studenten
        pass

class JSONStudentRepository(StudentRepository):     # Implementierung des StudentRepository für JSON-Dateien
    def __init__(self, dateipfad):                  # Initialisiert das Repository mit einem Dateipfad
        self.dateipfad = dateipfad

    def speichern(self, student):                   # Speichert einen Studenten in einer JSON-Datei
        daten = {
            "vorname": student.vorname,
            "nachname": student.nachname,
            "zielnote": student.zielnote,
            "regelstudienzeit": student.regelstudienzeit,
        }
        with open(self.dateipfad, 'w') as datei:    # Öffnet die Datei im Schreibmodus
            json.dump(daten, datei)                 # Speichert die Daten als JSON

    def laden(self, benutzername):                                                                                  # Lädt einen Studenten aus einer JSON-Datei
        with open(self.dateipfad, 'r') as datei:                                                                    # Öffnet die Datei im Lesemodus
            daten = json.load(datei)                                                                                # Lädt die Daten aus der JSON-Datei
            if daten["vorname"] == benutzername:                                                                    # Überprüft, ob der Vorname mit dem Benutzernamen übereinstimmt
                return Student(daten["vorname"], daten["nachname"], daten["zielnote"], daten["regelstudienzeit"])   # Gibt das Student-Objekt zurück, wenn der Benutzername übereinstimmt
            else:
                return None                                                                                         # Gibt None zurück, wenn der Benutzername nicht übereinstimmt