import random
FILE_NAME = "dane.txt"
N_PROCESOROW = 10
N_ZADAN = 20
MAX_CZAS_ZADANIA=6
f = open("dane.txt", "w")
f.write(f"{N_PROCESOROW}\n")
f.write(f"{N_ZADAN}\n")
for _ in range(N_ZADAN):
    f.write(f"{random.randint(1,MAX_CZAS_ZADANIA)}\n")
f.close()
