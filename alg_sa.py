import math
import random
import copy

def strategia_przesuniecia_ostatniego_z_max_do_min(zadania_na_procesorach, procesory):
    # Stategia opiera się na przeniesieniu zadania z najdłuższego procesora do najkrótszego
    # znajdywanie procesora o najdłuższym czasie
    max_idx = procesory.index(max(procesory))
    # znajdywanie procesora o najkrótszym czasie
    min_idx = procesory.index(min(procesory))     
    # procesory[min_idx][-1], procesory[max_idx][-1] = procesory[max_idx][-1], procesory[min_idx][-1] #zamiana elementów miejscami
    # Dodanie ostatniego zadania z najdłuższego procesora na minimalny procesor
    zadania_na_procesorach[min_idx].append(zadania_na_procesorach[max_idx][-1])
    # Zwiększamy czas pracy procesora min
    procesory[min_idx]+=zadania_na_procesorach[max_idx][-1]
    # Skracamy czas pracy procesora max
    procesory[max_idx]-=zadania_na_procesorach[max_idx][-1] 
    # Usuwamy proces z procesora max
    del zadania_na_procesorach[max_idx][-1] 
    return zadania_na_procesorach, procesory

def strategia_losowej_zamiany(zad, proc, l:int):
    # Wybieramy dwa losowe procesory, z których wybieramy po losowym zadaniu i zamieniamy je miejscami
    proc_a_idx = random.randint(0, l-1) # wybór losowego procesora a
    proc_b_idx = random.randint(0, l-1) # wybór losowego procesora b
    while(proc_a_idx==proc_b_idx):
        proc_b_idx = random.randint(0, l-1) 
    liczba_zadan_a = len(zad[proc_a_idx]) 
    liczba_zadan_b = len(zad[proc_b_idx]) 
    proc_a_2_idx = random.randint(0, liczba_zadan_a-1) # wybór losowego zadania na procesorze a
    proc_b_2_idx = random.randint(0, liczba_zadan_b-1) # wybór losowego zadania na procesorze b
    while(proc_a_2_idx==proc_b_2_idx):
        proc_b_2_idx = random.randint(0, liczba_zadan_b-1)
    # Zamiana miejscami 
    zad[proc_a_idx].append(zad[proc_b_idx][proc_b_2_idx]) # dodajemy na koniec procesora a zadanie z procesora b
    zad[proc_b_idx].append(zad[proc_a_idx][proc_a_2_idx]) # dodajemy na koniec procesora b zadanie z procesora a
    proc[proc_a_idx]+=(zad[proc_b_idx][proc_b_2_idx]-zad[proc_a_idx][proc_a_2_idx]) # aktualizujemy czas procesora a
    proc[proc_b_idx]+=(zad[proc_a_idx][proc_a_2_idx]-zad[proc_b_idx][proc_b_2_idx]) # aktualizujemy czas procesora b
    del zad[proc_a_idx][proc_a_2_idx] # Usuwamy przeniesione zadanie z procesora a
    del zad[proc_b_idx][proc_b_2_idx] # Usuwamy przeniesione zadanie z procesora b
    
def algorytm_sa(rozwiazanie_poczatkowe, czasy_poczatkowe, l:int, max_iter:int, temperatura:float, wsp_chlodzenia:float, cmax:float):
    # Algorytm modyfikuje rozwiązane podane jako argument!!!
    Cbest = cmax # zmienna do przechowywania najlepszego rozwiązania
    c = cmax
    iteracje = 0
    x = rozwiazanie_poczatkowe # zmienna przechowująca aktualne rozwiązanie
    y = czasy_poczatkowe # zmienna przechowująca czasy aktualnego rozwiązania
    # Główna pętla: wyżarzanie (rozbudować kryteria stopu o min temperaturę, brak zmiany rozwiązania)
    while(iteracje<max_iter):
        # 1. Budujemy sąsiada
        sasiad = copy.deepcopy(x)
        czasy_sasiada = copy.deepcopy(y)
        strategia_losowej_zamiany(sasiad, czasy_sasiada, l)
        # 2. Obliczamy wartość rozwiązania sąsiada
        new_c = max(czasy_sasiada) #Czy da się uprościć obliczanie kosztu? Jeśli byśmy wiedzieli, jakie dwa procesory brały udział w budowaniu nowego rozwiązania możemy to prościej policzyć 
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

def wyswietl_uszeregowanie(p, l, c):
    wypis =[]
    col = [7, 3, 70] # Szerokości kolumn
    cp_max = c
    s = len(str(cp_max))-2
    modul = 10**s
    # Konstruowanie listy danych potrzebnej do formatowania
    for i in range(l):
        wypis.append([])
        kropki = "."*int(p[i]/modul)+ " " + str(p[i])
        wypis[i].append(["Procesor", str(i+1), kropki])
    # Wypis przygotowanych danych
    for row in wypis:
        row= row[0]
        formatted = f"{row[0]:<{col[0]}} {row[1]:<{col[1]}} {row[2]:<{col[2]}}"
        print(formatted)

def algorytm_greedy(zad, l: int):
    # 2. Przydzielanie zadania na wolny procesor
    procesory = [0] * l # lista reprezentująca procesory
    zadania_na_procesorach = [ [] for _ in range(l)] # lista przechowująca informacje, które zadania są na którym procesorze są które zadania
    # 2.1 Przydzielanie zadania do wolnego procesora
    for zadanie in zad:
        ind_najwolniejszy_procesor = procesory.index(min(procesory)) # wyszukanie wolnego procesora
        procesory[ind_najwolniejszy_procesor] += zadanie # 2.3 Przypisać zadanie
        zadania_na_procesorach[ind_najwolniejszy_procesor].append(zadanie)
    c = max(procesory)
    return procesory, zadania_na_procesorach, c

def wczytywanie(plik):
    f = open(plik, "r")
    lines = f.readlines()
    zadania = []
    liczba_procesorow = int(lines[0])
    liczba_zadan = int(lines[1])
    for i in range(2, liczba_zadan+2):
        x = int(lines[i])
        zadania.append(x)
    return zadania, liczba_procesorow

def run_loop(epochs, file, iter, temp, alfa, c):
    C_max = c
    c_ = c
    for _ in range(epochs):
        zadania, liczba_procesorow = wczytywanie(file)
        czasy_procesorow, zadania_na_procesorach, c_max = algorytm_greedy(zadania, liczba_procesorow)
        c_ = algorytm_sa(zadania_na_procesorach, czasy_procesorow, liczba_procesorow, iter, temp, alfa, c_)
        if (c_ < C_max):
            print(f"Znaleziono nowe cmax {c_}")
            C_max = c_
    return C_max

# 1. Wczytywanie danych instancji
FILE = "plik100.txt"
zadania, liczba_procesorow = wczytywanie(FILE)
# 2. Budowa rozwiązania bazowego algorytmem zachłannym
czasy_procesorow, zadania_na_procesorach, c_max = algorytm_greedy(zadania, liczba_procesorow)
print("C_max = ", c_max)
# 3. Poprawianie rowiązania bazowego algorytmem symulowanego wyżarzania
ITER = 600
TEMP = 600
ALFA = 0.85
c_max = algorytm_sa(zadania_na_procesorach, czasy_procesorow, liczba_procesorow, ITER, TEMP, ALFA, c_max)
print(f"Rozwiazanie znalezione po {ITER} iteracjach: {c_max}")
# 4. Wyświetlenie uszeregowania
#wyswietl_uszeregowanie(czasy_procesorow, liczba_procesorow, c_max)
print(f"C_max: {run_loop(1000, FILE, ITER, TEMP, ALFA, c_max)}")