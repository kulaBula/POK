#Algorytm Zachłanny
# 1. Wczytywanie danych instancji
FILE = "JO_20.txt"
print(FILE)
f = open(FILE)
lines = f.readlines()
zadania = []
liczba_procesorow = int(lines[0])
szereg = []
liczba_zadan = int(lines[1])
for i in range(2, liczba_zadan+2):
    x = int(lines[i])
    zadania.append(x)
    szereg.append([])
#print(zadania)
# 2. Przydzielanie zadania na wolny procesor (zajętość procesora możemy liczyć po prostu zliczając czasy zadań do niego już przydzielonych)
# 2.1 Procesory nich będą reprezentowane przez listę
procesory = [0] * liczba_procesorow
# 2.2 Zidentyfikować (jakoś) "wolny procesor" -> [najwolniejsza opcja] za każdym razem szukać minimum po liście procesorów i do niego dodawać
# Jak sprytnie zapisywać, który procesor jest najszybciej wolny, tak, żeby to robić w czasie lepszym niż o(n^2)?
licznik = 1
for zadanie in zadania:
    ind_najwolniejszy_procesor = procesory.index(min(procesory))
    procesory[ind_najwolniejszy_procesor] += zadanie 
    szereg[ind_najwolniejszy_procesor].append(licznik)
    licznik+=1
print(procesory)

# 3. Znaleźć, na którym procesorze jest najdłuższy czas
print("C_max = ", max(procesory))
# POMYSŁ: za pomocą odpowiedniego wyświetlania przedstawić uszeregowanie tych procesów
print("Uszeregowanie:")
for i in range(liczba_procesorow):
    print(f"Procesor {i}: {szereg[i]}")