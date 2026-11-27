import random
from pathlib import Path


QUEUE_LENGTH = 100
RUNS = 10000

BASE_DIR = Path(__file__).resolve().parent
RESULTS_FILE = BASE_DIR / "results.txt"


def normal_customer_time():
    take_money = random.uniform(1.0, 3.0)
    check_money = random.uniform(0.5, 1.5)
    give_product = random.uniform(1.0, 2.5)

    change_time = 0

    if random.random() < 0.5:
        change_time = random.uniform(0.5, 1.5)

    return take_money + check_money + give_product + change_time


def cheater_customer_time():
    give_exact_money = random.uniform(0.5, 1.0)
    give_product = random.uniform(1.0, 2.5)

    return give_exact_money + give_product


def simulate_queue(with_cheater=False):
    service_times = []

    cheater_position = None

    if with_cheater:
        cheater_position = random.randint(0, QUEUE_LENGTH - 1)

    for i in range(QUEUE_LENGTH):
        if with_cheater and i == cheater_position:
            service_time = cheater_customer_time()
        else:
            service_time = normal_customer_time()

        service_times.append(service_time)

    total_time = sum(service_times)

    waiting_times = []
    elapsed = 0

    for service_time in service_times:
        waiting_times.append(elapsed)
        elapsed += service_time

    average_waiting_time = sum(waiting_times) / QUEUE_LENGTH

    return total_time, average_waiting_time


def run_experiment(with_cheater=False):
    total_times = []
    waiting_times = []

    for _ in range(RUNS):
        total_time, average_wait = simulate_queue(with_cheater)

        total_times.append(total_time)
        waiting_times.append(average_wait)

    average_total_time = sum(total_times) / RUNS
    average_waiting_time = sum(waiting_times) / RUNS

    return average_total_time, average_waiting_time


def main():
    print("Запуск симуляції...")

    normal_total, normal_wait = run_experiment(False)
    cheater_total, cheater_wait = run_experiment(True)

    total_difference = normal_total - cheater_total
    wait_difference = normal_wait - cheater_wait

    result = f"""
=== Лабораторна робота №10 ===

Кількість людей у черзі: {QUEUE_LENGTH}
Кількість запусків: {RUNS}

ЗВИЧАЙНА ЧЕРГА
Середній час завершення черги: {normal_total:.2f} сек
Середній час очікування однієї людини: {normal_wait:.2f} сек

ЧЕРГА З ЧІТЕРОМ
Середній час завершення черги: {cheater_total:.2f} сек
Середній час очікування однієї людини: {cheater_wait:.2f} сек

РІЗНИЦЯ
Черга з читером завершується швидше на: {total_difference:.2f} сек
Середній час очікування менший на: {wait_difference:.2f} сек
"""

    print(result)

    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        file.write(result)

    print(f"Результат збережено у файл: {RESULTS_FILE.name}")


if __name__ == "__main__":
    main()