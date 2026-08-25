from modelle import Modulstatus, Pruefungsleistung, Modul, Semester, Studiengang, Belegung

mathe = Modul("Mathematik", Modulstatus.ABGESCHLOSSEN, 5)
klausur_mathe = Pruefungsleistung("Klausur Mathe", "01.06.2024")
klausur_mathe.note = 1.0
mathe.pruefungsleistung_hinzufuegen(klausur_mathe)

security = Modul("Security", Modulstatus.ABGESCHLOSSEN, 10)
klausur_security = Pruefungsleistung("Klausur Security", "15.06.2024")
klausur_security.note = 3.0
security.pruefungsleistung_hinzufuegen(klausur_security)

sem1 = Semester(1)
sem1.modul_hinzufuegen(mathe)
sem1.modul_hinzufuegen(security)

belegung = Belegung("01.10.2024")
belegung.semester_hinzufuegen(sem1)

print(belegung.ects_erreicht_berechnen())
print(belegung.notendurchschnitt_berechnen())