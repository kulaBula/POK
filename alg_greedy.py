#Algorytm Zachłanny

# 1. Wczytywanie danych instancji
f = open("dane.txt", "r");
lines = f.readlines()
liczba_procesorow = int(lines[0])
liczba_zadan = int(lines[1])
for _ in range(2, liczba_zadan)
# 2. Przydzielanie zadania na wolny procesor (zajętość procesora możemy liczyć po prostu zliczając czasy zadań do niego już przydzielonych)
# 2.1 Procesory nich będą reprezentowane przez listę
# 2.2 Zidentyfikować (jakoś) "wolny procesor" -> [najwolniejsza opcja] za każdym razem szukać minimum po liście procesorów i do niego dodawać
# Jak sprytnie zapisywać, który procesor jest najszybciej wolny, tak, żeby to robić w czasie lepszym niż o(n^2)?
# 2.3 Przypisać zadanie 

# 3. Znaleźć, na którym procesorze jest najdłuższy czas

# POMYSŁ: za pomocą odpowiedniego wyświetlania przedstawić uszeregowanie tych procesów


