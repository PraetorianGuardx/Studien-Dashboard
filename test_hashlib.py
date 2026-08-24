import hashlib                                          # Import der hashlib-Bibliothek, die Funktionen für kryptografische Hashes bereitstellt

passwort = "mein_passwort"                              # Beispiel-Passwort

hash1 = hashlib.sha256(passwort.encode()).hexdigest()   # Erstellen des Hashs des Passworts
hash2 = hashlib.sha256(passwort.encode()).hexdigest()   # Erstellen des Hashs des Passworts erneut

print("hash1:", hash1)
print("hash2:", hash2)
print("Hashes sind gleich:", hash1 == hash2)            # Überprüfen, ob die beiden Hashes gleich sind    