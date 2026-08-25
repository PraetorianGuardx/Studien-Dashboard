from modelle import Modulstatus, Modul, Semester

mathe = Modul("Mathematik", Modulstatus.AKTUELL, 5)
python_kurs = Modul("Python", Modulstatus.ABGESCHLOSSEN, 5)

sem1 = Semester(1)
sem1.modul_hinzufuegen(mathe)
sem1.modul_hinzufuegen(python_kurs)

for modul in sem1.module:
    print(modul.name)