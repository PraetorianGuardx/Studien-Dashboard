from abc import ABC, abstractmethod
from modelle import Student
import jsonpickle

class StudentRepository(ABC):                           # Abstrakte Basisklasse für das StudentRepository
    @abstractmethod
    def speichern(self, student):                       # Abstrakte Methode zum Speichern eines Studenten
        pass

    @abstractmethod
    def laden(self, benutzername):                      # Abstrakte Methode zum Laden eines Studenten
        pass

class JSONStudentRepository(StudentRepository):         # Implementierung des StudentRepository für JSON-Dateien
    def __init__(self, dateipfad):                      # Initialisiert das Repository mit einem Dateipfad
        self.dateipfad = dateipfad

    def speichern(self, student):                       # Speichert einen Studenten in einer JSON-Datei
        with open(self.dateipfad, 'w') as datei:        # Öffnet die Datei im Schreibmodus
            datei.write(jsonpickle.encode(student))     # Serialisiert das Studentenobjekt und schreibt es in die Datei

    def laden(self, benutzername):                      # Lädt einen Studenten aus einer JSON-Datei
        with open(self.dateipfad, 'r') as datei:        # Öffnet die Datei im Lesemodus
            student = jsonpickle.decode(datei.read())   # Deserialisiert das Studentenobjekt aus der Datei
            if student.vorname == benutzername:         # Überprüft, ob der Vorname des Studenten mit dem Benutzernamen übereinstimmt
                return student                          # Gibt das Studentenobjekt zurück, wenn es übereinstimmt
            else:
                return None                             # Gibt None zurück, wenn kein passender Student gefunden wurde 

# Quelle: https://www.youtube.com/watch?v=97V7ICVeTJc
# Quelle: https://pypi.org/project/jsonpickle/