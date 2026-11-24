import threading
import time

def count_numbers(n):
    print(f"Counting numbers from 1 to {n}:")
    for i in range(1, n + 1):
        print(i)
        time.sleep(0.5)

def calculate_squares(n):
    print(f"Calculating squares from 1 to {n}:")
    for i in range(1, n + 1):
        print(f"{i}^2 = {i * i}")
        time.sleep(0.5)

def calculate_cubes(n):
    print(f"Calculating cubes from 1 to {n}:")
    for i in range(1, n + 1):
        print(f"{i}^3 = {i * i * i}")
        time.sleep(0.5)

def main():
    n = 5

    t1 = threading.Thread(target=count_numbers, args=(n,))
    t2 = threading.Thread(target=calculate_squares, args=(n,))
    t3 = threading.Thread(target=calculate_cubes, args=(n,))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print("All threads completed.")

if __name__ == "__main__":
    main()
