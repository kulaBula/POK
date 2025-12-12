import math
import random
import copy

def insertion_sort_sync(arr, t_arr):
    n = len(arr)
    c = 0
    s = 0
    for j in range(1, n):
        key = arr[j]
        t_key = t_arr[j] # Zapamiętujemy również odpowiadający element z t_arr
        i = j-1
        
        # Sortowanie malejące: operator porownania przy arr i key
        while i >= 0 and arr[i] < key:
            arr[i+1] = arr[i]
            t_arr[i+1] = t_arr[i] # Przesuwamy element w t_arr
            i = i-1
            c += 1
            s += 1
            
        arr[i+1] = key
        t_arr[i+1] = t_key 
        s += 1
        
    return arr, t_arr, c, s

def strategia_min_max_proc_rand_zad_poprawiona(zad, proc, l:int):
    len_max = len(zad[0])
    if len_max == 0:
        return # Nie można wykonać ruchu, jeśli P_MAX jest pusty
    # Wybieramy losowe zadanie do przeniesienia Z P_MAX (zad[0])
    idx_max = random.randint(0, len_max - 1)
    czas_przenoszonego_zadania = zad[0][idx_max] # czas zadania przed usunięciem
    del zad[0][idx_max] #Usuń zadanie z listy zadań max
    zad[-1].append(czas_przenoszonego_zadania) #Dodaj zadanie do listy zadań min
    proc[0] -= czas_przenoszonego_zadania # akutalizacja czasu max
    proc[-1] += czas_przenoszonego_zadania # aktualizacja czasu min
    insertion_sort_sync(proc, zad)

def algorytm_sa(rozwiazanie_poczatkowe, czasy_poczatkowe, l:int, max_iter:int, temperatura:float, wsp_chlodzenia:float, cmax:float):
    # Algorytm modyfikuje rozwiązane podane jako argument!!!
    Cbest = cmax # zmienna do przechowywania najlepszego rozwiązania
    c = cmax
    iteracje = 0
    x = rozwiazanie_poczatkowe # zmienna przechowująca aktualne rozwiązanie
    y = czasy_poczatkowe # zmienna przechowująca czasy aktualnego rozwiązania
    p = 0
    # Główna pętla: wyżarzanie (rozbudować kryteria stopu o min temperaturę, brak zmiany rozwiązania)
    while(iteracje<max_iter):
        # 1. Budujemy sąsiada
        sasiad = copy.deepcopy(x)
        czasy_sasiada = copy.deepcopy(y)
        strategia_min_max_proc_rand_zad_poprawiona(sasiad, czasy_sasiada, l)
        # 2. Obliczamy wartość rozwiązania sąsiada
        new_c = max(czasy_sasiada)  
        # 3. Porównujemy nowe rozwiązanie z poprzednim
        delta = new_c - c # Obliczamy różnicę w funkcji celu (energię)
        # 3.1 Jeśli rozwiązanie jest lepsze:
        if(delta < 0):
            #print(f"Nowe lepsze rozwiazanie: {new_c}, delta: {delta}, iteracja: {iteracje}")
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
            r = random.random() # Losujemy losową liczbę z przedziału od 0 do 1
            # Sprawdzamy, czy rozwiązanie zostanie przyjęte czy nie
            if(r<p):
                #akceptujemy rozwiązanie
                x = sasiad
                y = czasy_sasiada
        # 4. Obniżamy temperaturę 
        temperatura = temperatura*wsp_chlodzenia
        # 5. Inkrementujemy liczbę iteracji
        iteracje+=1
        if(iteracje%10==0):
            #print(f"{iteracje}: Delta:{delta}, Temp: {temperatura}, Praw: {p}")
            pass
        
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

def wczytywanie(plik, sort_true: True):
    f = open(plik, "r")
    lines = f.readlines()
    zadania = []
    liczba_procesorow = int(lines[0])
    liczba_zadan = int(lines[1])
    for i in range(2, liczba_zadan+2):
        x = int(lines[i])
        zadania.append(x)
    # Sortowanie zadań względem ich długości 
    if(sort_true):
        zadania.sort(reverse=True)
    return zadania, liczba_procesorow

def run(p, file, runs:int, log:bool):
    C_best=10000000000
    for r in range(runs):
        zadania, liczba_procesorow = wczytywanie(file, p[file][0])
        czasy_procesorow, zadania_na_procesorach, c_max = algorytm_greedy(zadania, liczba_procesorow)
        ITER = p[file][1]
        TEMP = p[file][2]
        ALFA = p[file][3] # Współczynnik chłodzenia
        c_max = algorytm_sa(zadania_na_procesorach, czasy_procesorow, liczba_procesorow, ITER, TEMP, ALFA, c_max)
        #print(f"Rozwiazanie znalezione po {ITER} iteracjach: {c_max}")
        if(c_max<C_best):
            C_best = c_max
            if(log):
                print(f"Znaleziono nowe lepsze rozwiazanie przy run {r+1}: {C_best}")
    print(f"Najlepsze rozwiazanie Cmax dla {FILE}: {C_best}")

def run_all(p, runs:int, log:bool):
    files=["dane/n50m200.txt","dane/n50m1000.txt","dane/n10m200.txt","dane/m50.txt", "dane/m25.txt"]
    for f in files:
        print(f"Running file: {f}...")
        run(p, f, runs, log)
        print("Done.")

# MAIN
FILE = "dane/n50m200.txt"
params = {"dane/n50m200.txt": [True, 10000, 25000, 0.999999], #978 (1)
          "dane/n50m1000.txt": [True, 20000, 20000, 0.99999999] ,#9763
          "dane/n10m200.txt": [True, 15000, 20000, 0.99999999] ,#10999 
        "dane/m50.txt": [False, 2000, 20000, 0.999999] ,#151 (1)
        "dane/m25.txt": [True, 50000, 30000, 0.99999999] #3458
        }
run_all(params, 10, True)
