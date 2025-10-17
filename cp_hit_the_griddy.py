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
def reprezentacja_kropkowa(procesory, liczba_procesorow, c_max):
    s = len(str(c_max)) - 2
    modul = 10**s
    for i in range(liczba_procesorow):
        print(f"Procesor {i+1}: ", "."*(int(procesory[i]/modul)), procesory[i])

# 1. Wczytywanie danych instancji
#f = open("cp_numbers.txt", "r")
f = open("plik100.txt", "r")
lines = f.readlines()
zadania = []
wypis = []
liczba_procesorow = int(lines[0])
liczba_zadan = int(lines[1])
for i in range(2, liczba_zadan+2):
    x = int(lines[i])
    zadania.append(x)
print("Czasy zadań: ", zadania)
# 2. Przydzielanie zadania na wolny procesor (zajętość procesora możemy liczyć po prostu zliczając czasy zadań do niego już przydzielonych)
# 2.1 Procesory nich będą reprezentowane przez listę
procesory = [0] * liczba_procesorow

for zadanie in zadania:
    ind_najwolniejszy_procesor = procesory.index(min(procesory))
    procesory[ind_najwolniejszy_procesor] += zadanie # 2.3 Przypisać zadanie
#print("Czasy procesorów: ", procesory)

# 3. Znaleźć, na którym procesorze jest najdłuższy czas -> Cmax
c_max = max(procesory)
print("C_max = ", c_max)

# Output z równymi przerwami
# Potrzebna jest lista procesor + nr procesora + czas + kropki z napisem
col = [7, 3, 70]
cp_max = c_max
s = len(str(cp_max))-2
modul = 10**s
for i in range(liczba_procesorow):
    wypis.append([])
    kropki = "."*int(procesory[i]/modul)+ " " + str(procesory[i])
    wypis[i].append(["Procesor", str(i+1), kropki])

# Wypis przygotowanych danych
for row in wypis:
    row= row[0]
    formatted = f"{row[0]:<{col[0]}} {row[1]:<{col[1]}} {row[2]:<{col[2]}}"
    print(formatted)
