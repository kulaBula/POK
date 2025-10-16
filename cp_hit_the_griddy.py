#Algorytm Zachłanny

#funckja do wyświetlania uszeregowania
def da_function(procesory):
    print()
    print("Procesor 1:", "_ " * procesory[0])
    print("Procesor 2:", "_ " * procesory[1])
    print("Procesor 3:", "_ " * procesory[2])
    print("Procesor 4:", "_ " * procesory[3])
    print("czas [s]   ", "_ " * (max(procesory)+1))
    print("            ", end = "")
    for i in range(1, max(procesory)+2): 
        print(i, end = " ")
    print()

# 1. Wczytywanie danych instancji
#f = open("cp_numbers.txt", "r")
f = open("dane.txt", "r")
lines = f.readlines()
zadania = []
liczba_procesorow = int(lines[0])
liczba_zadan = int(lines[1])
for i in range(2, liczba_zadan+2):
    x = int(lines[i])
    zadania.append(x)
print("Czasy zadań: ", zadania)
# 2. Przydzielanie zadania na wolny procesor (zajętość procesora możemy liczyć po prostu zliczając czasy zadań do niego już przydzielonych)
# 2.1 Procesory nich będą reprezentowane przez listę
procesory = [0] * liczba_procesorow
# 2.2 Zidentyfikować (jakoś) "wolny procesor" -> [najwolniejsza opcja] za każdym razem szukać minimum po liście procesorów i do niego dodawać
# Jak sprytnie zapisywać, który procesor jest najszybciej wolny, tak, żeby to robić w czasie lepszym niż o(n^2)?
for zadanie in zadania:
    ind_najwolniejszy_procesor = procesory.index(min(procesory))
    procesory[ind_najwolniejszy_procesor] += zadanie # 2.3 Przypisać zadanie
print("Czasy procesorów: ", procesory)
# POMYSŁ: za pomocą odpowiedniego wyświetlania przedstawić uszeregowanie tych procesów
da_function(procesory)
# 3. Znaleźć, na którym procesorze jest najdłuższy czas
print("C_max = ", max(procesory))
    