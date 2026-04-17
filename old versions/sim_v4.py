import random

base_chargers = 6
extra_chargers = 2  # seus carregadores vendidos
num_cars = 70


def generate_cars():
    cars = []
    current_time = 0

    for i in range(num_cars):
        hour = current_time % 600

        if 200 < hour < 300 or 400 < hour < 520:
            arrival = current_time + random.randint(2, 6)
        else:
            arrival = current_time + random.randint(5, 12)

        charge = random.randint(40, 70)

        delay = random.choices(
            [0, 5, 10, 15, 20],
            weights=[30, 25, 20, 15, 10]
        )[0]

        priority = random.randint(1, 3)
        reserved = random.random() < 0.4

        cars.append({
            "arrival": arrival,
            "charge": charge,
            "delay": delay,
            "priority": priority,
            "reserved": reserved
        })

        current_time = arrival

    return cars


def simulate(cars, mode="none"):
    # modos:
    # "none" = sem sistema
    # "software" = só software
    # "full" = software + hardware

    if mode == "full":
        total_chargers = base_chargers + extra_chargers
    else:
        total_chargers = base_chargers

    chargers = [0] * total_chargers

    total_wait = 0
    total_idleness = 0

    queue = []

    current_time = 0
    i = 0

    while i < len(cars) or queue:

        while i < len(cars) and cars[i]["arrival"] <= current_time:
            queue.append(cars[i])
            i += 1

        # organização da fila
        if mode != "none":
            queue.sort(key=lambda x: (
                -x["priority"],
                not x["reserved"],
                x["arrival"]
            ))
        else:
            queue.sort(key=lambda x: x["arrival"])

        # processar carregadores
        for c in range(total_chargers):
            if chargers[c] <= current_time and queue:
                car = queue.pop(0)

                arrival = car["arrival"]
                charge = car["charge"]
                delay = car["delay"]

                wait = current_time - arrival

                if mode != "none":

                    # 🔵 BLE / resposta rápida
                    if random.random() < 0.7:
                        delay = int(delay * random.uniform(0.3, 0.7))

                    # 🔴 hardware melhora ainda mais
                    if mode == "full":
                        delay = int(delay * random.uniform(0.2, 0.5))

                    # ⚡ prioridade = carga mais rápida
                    if car["priority"] == 3:
                        charge = int(charge * 0.85)

                    # ⚡ smart charging (quando sistema cheio)
                    active = sum(1 for x in chargers if x > current_time)

                    if mode == "full" and active >= total_chargers * 0.8:
                        charge = int(charge * 1.2)  # desacelera um pouco

                    overhead = random.choice([0, 1, 2])

                else:
                    overhead = 0

                end = current_time + charge + overhead
                chargers[c] = end + delay

                total_wait += max(wait, 0)
                total_idleness += delay

        current_time += 1

    return total_wait / num_cars, total_idleness / num_cars


# =============================

executions = 5

results = {
    "none": [],
    "software": [],
    "full": []
}

for i in range(executions):
    cars = generate_cars()

    res_none = simulate(cars, "none")
    res_soft = simulate(cars, "software")
    res_full = simulate(cars, "full")

    results["none"].append(res_none)
    results["software"].append(res_soft)
    results["full"].append(res_full)

    print(f"\nExecução {i+1}:")
    print(f"Sem sistema -> Espera: {res_none[0]:.2f} | Ociosidade: {res_none[1]:.2f}")
    print(f"Só software -> Espera: {res_soft[0]:.2f} | Ociosidade: {res_soft[1]:.2f}")
    print(f"Com hardware -> Espera: {res_full[0]:.2f} | Ociosidade: {res_full[1]:.2f}")


def average(lst):
    return sum(x[0] for x in lst)/len(lst), sum(x[1] for x in lst)/len(lst)


avg_none = average(results["none"])
avg_soft = average(results["software"])
avg_full = average(results["full"])

print(f"\n=== RESULTADO MÉDIO ({executions} execuções) ===\n")

print("Sem sistema:")
print(f"Espera: {avg_none[0]:.2f} | Ociosidade: {avg_none[1]:.2f}")

print("\nSó software:")
print(f"Espera: {avg_soft[0]:.2f} | Ociosidade: {avg_soft[1]:.2f}")

print("\nSoftware + hardware:")
print(f"Espera: {avg_full[0]:.2f} | Ociosidade: {avg_full[1]:.2f}")


def improvement(a, b):
    return ((a - b) / a) * 100


print("\n=== MELHORIAS ===")

print(f"\nSoftware vs Sem sistema:")
print(f"Espera: {improvement(avg_none[0], avg_soft[0]):.2f}%")
print(f"Ociosidade: {improvement(avg_none[1], avg_soft[1]):.2f}%")

print(f"\nHardware vs Sem sistema:")
print(f"Espera: {improvement(avg_none[0], avg_full[0]):.2f}%")
print(f"Ociosidade: {improvement(avg_none[1], avg_full[1]):.2f}%")