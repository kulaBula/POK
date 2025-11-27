#Algorytm Zachłanny problemu P||Cmax
import math
import random
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
# Funkcja wizualizująca czasy uszeregowania zadań na procesorach bez formatowania
def reprezentacja_kropkowa(procesory, liczba_procesorow, c_max):
    s = len(str(c_max)) - 2
    modul = 10**s
    for i in range(liczba_procesorow):
        print(f"Procesor {i+1}: ", "."*(int(procesory[i]/modul)), procesory[i])

# 1. Wczytywanie danych instancji
FILE = "plik100.txt" # TU PODAJ NAZWE PLIKU
f = open(FILE, "r")
lines = f.readlines()
zadania = []
wypis = [] # Tablica potrzebna do wizualizacji zajętości procesorów
liczba_procesorow = int(lines[0])
liczba_zadan = int(lines[1])

for i in range(2, liczba_zadan+2):
    x = int(lines[i])
    zadania.append(x)
#print("Czasy zadań: ", zadania)
# 2. Przydzielanie zadania na wolny procesor
procesory = [0] * liczba_procesorow # lista reprezentująca procesory
zadania_na_procesorach = [ [] for _ in range(liczba_procesorow)] # lista przechowująca informacje, które zadania są na którym procesorze są które zadania
# 2.1 Przydzielanie zadania do wolnego procesora
for zadanie in zadania:
    ind_najwolniejszy_procesor = procesory.index(min(procesory)) # wyszukanie wolnego procesora
    procesory[ind_najwolniejszy_procesor] += zadanie # 2.3 Przypisać zadanie
    zadania_na_procesorach[ind_najwolniejszy_procesor].append(zadanie)
#print("Czasy procesorów: ", procesory)

# Symulowane wyżarzanie
def stategia_budowania_sasiada(zadania_na_procesorach, procesory):
    # Stategia opiera się na przeniesieniu zadania z najdłuższego procesora do najkrótszego
    # znajdywanie procesora o najdłuższym czasie
    max_idx = procesory.index(max(procesory))
    # znajdywanie procesora o najkrótszym czasie
    min_idx = procesory.index(min(procesory))     
    # procesory[min_idx][-1], procesory[max_idx][-1] = procesory[max_idx][-1], procesory[min_idx][-1] #zamiana elementów miejscami
    # Dodanie ostatniego zadania z najdłuższego procesora na minimalny procesor
    #print("Zadania na min procesorze przed zamiana: ")
    #print(zadania_na_procesorach[min_idx])
    zadania_na_procesorach[min_idx].append(zadania_na_procesorach[max_idx][-1])
    #print("Zadania na min procesorze po zamianie:")
    #print(zadania_na_procesorach[min_idx])
    # Zwiększamy czas pracy procesora min
    #print(f"Stary czas min {procesory[min_idx]}")
    procesory[min_idx]+=zadania_na_procesorach[max_idx][-1]
    #print(f"Nowy czas min {procesory[min_idx]}")
    # Skracamy czas pracy procesora max
    #print(f"Stary czas max {procesory[max_idx]}")
    procesory[max_idx]-=zadania_na_procesorach[max_idx][-1] 
    #print(f"Stary czas max {procesory[max_idx]}")
    # Usuwamy proces z procesora max
    #print("Zadania na max procesorze przed zamiana:")
    #print(zadania_na_procesorach[max_idx])
    del zadania_na_procesorach[max_idx][-1] 
    #print("Zadanie na max procesorze po zamianie:")
    #print(zadania_na_procesorach[max_idx])
    return zadania_na_procesorach, procesory

def algorytm_sa(rozwiazanie_poczatkowe, czasy_poczatkowe, max_iter, temperatura, wsp_chlodzenia, cmax):
    Cbest = cmax # zmienna do przechowywania najlepszego rozwiązania
    c = cmax
    iteracje = 0
    x = rozwiazanie_poczatkowe # zmienna przechowująca aktualne rozwiązanie
    y = czasy_poczatkowe # zmienna przechowująca czasy aktualnego rozwiązania
    # Główna pętla: wyżarzanie (rozbudować kryteria stopu o min temperaturę, brak zmiany rozwiązania)
    while(iteracje<max_iter):
        # 1. Budujemy sąsiada
        sasiad, czasy_sasiada = stategia_budowania_sasiada(x, y)
        # 2. Obliczamy wartość rozwiązania sąsiada
        new_c = max(czasy_sasiada)
        # 3. Porównujemy nowe rozwiązanie z poprzednim
        delta = new_c - c # Obliczamy różnicę w funkcji celu (energię)
        # 3.1 Jeśli rozwiązanie jest lepsze:
        if(delta < 0):
            c = new_c
            x = sasiad 
            y = czasy_sasiada
            # 3.2 Sprawdzamy, czy nie osiągneliśmy nowego najlepszego rozwiązania
            if(new_c< Cbest):
                Cbest = new_c # Znaleziono nowe najmniejsze rozwiązanie globalne -> Tu by można je zapisać do dowej zmiennej i potem zwrócić 
        # 3.3 Jeśli rozwiązanie jest gorsze:
        else:
            # Obliczamy prawdopodobieństwo akceptacji gorszego rozwiązania
            p = math.exp((delta*(-1))/temperatura)
            # Losujemy losową liczbę z przedziału od 0 do 1
            r = random.randrange(0, 1)
            # Sprawdzamy, czy rozwiązanie zostanie przyjęte czy nie
            if(r<p):
                #akceptujemy rozwiązanie
                x = sasiad
                y = czasy_sasiada
        # 4. Obniżamy temperaturę 
        temperatura = temperatura*wsp_chlodzenia
        # 5. Inkrementujemy liczbę iteracji
        iteracje+=1
    return Cbest


# 3. Znaleźć, na którym procesorze jest najdłuższy czas -> Cmax
c_max = max(procesory)
print("C_max = ", c_max)

# 4. Wizualizacja zajętości poszczególnych procesorów
# Potrzebna jest lista procesor + nr procesora + czas + kropki z napisem
col = [7, 3, 70] # Szerokości kolumn
cp_max = c_max
s = len(str(cp_max))-2
modul = 10**s
# 4.1 Konstruowanie listy danych potrzebnej do formatowania
for i in range(liczba_procesorow):
    wypis.append([])
    kropki = "."*int(procesory[i]/modul)+ " " + str(procesory[i])
    wypis[i].append(["Procesor", str(i+1), kropki])

# 4.2 Wypis przygotowanych danych
for row in wypis:
    row= row[0]
    formatted = f"{row[0]:<{col[0]}} {row[1]:<{col[1]}} {row[2]:<{col[2]}}"
    print(formatted)


# Testowanie strategii zamiany
# zadania_na_procesorach, procesory = stategia_budowania_sasiada(zadania_na_procesorach, procesory)
# c_max = max(procesory)
# print("C_max = ", c_max)

# wypis = []
# col = [7, 3, 70] # Szerokości kolumn
# cp_max = c_max
# s = len(str(cp_max))-2
# modul = 10**s
# # 4.1 Konstruowanie listy danych potrzebnej do formatowania
# for i in range(liczba_procesorow):
#     wypis.append([])
#     kropki = "."*int(procesory[i]/modul)+ " " + str(procesory[i])
#     wypis[i].append(["Procesor", str(i+1), kropki])

# # 4.2 Wypis przygotowanych danych
# for row in wypis:
#     row= row[0]
#     formatted = f"{row[0]:<{col[0]}} {row[1]:<{col[1]}} {row[2]:<{col[2]}}"
#     print(formatted)


# Testowanie algorytmu symulowanego wyżarzania
c_max = algorytm_sa(zadania_na_procesorach, procesory, 11, 400, 0.95, c_max)
print(f"Rozwiązanie znalezione po 10 iteracjach: {c_max}")
wypis =[]
col = [7, 3, 70] # Szerokości kolumn
cp_max = c_max
s = len(str(cp_max))-2
modul = 10**s
# 4.1 Konstruowanie listy danych potrzebnej do formatowania
for i in range(liczba_procesorow):
    wypis.append([])
    kropki = "."*int(procesory[i]/modul)+ " " + str(procesory[i])
    wypis[i].append(["Procesor", str(i+1), kropki])

# 4.2 Wypis przygotowanych danych
for row in wypis:
    row= row[0]
    formatted = f"{row[0]:<{col[0]}} {row[1]:<{col[1]}} {row[2]:<{col[2]}}"
    print(formatted)