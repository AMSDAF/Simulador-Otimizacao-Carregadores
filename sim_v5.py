import random

base_chargers = 6
extra_chargers = 2
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

        battery = random.randint(10, 80)
        charge = int((100 - battery) * random.uniform(0.6, 1.0))

        delay = random.choices(
            [0, 5, 10, 15, 20],
            weights=[30, 25, 20, 15, 10]
        )[0]

        priority = random.randint(1, 3)
        reserved = random.random() < 0.4

        lazy = random.random() < 0.3

        cars.append({
            "arrival": arrival,
            "charge": charge,
            "delay": delay,
            "priority": priority,
            "reserved": reserved,
            "lazy": lazy
        })

        current_time = arrival

    return cars


def simulate(cars, mode="none"):

    if mode in ["full", "hardware_plus"]:
        total_chargers = base_chargers + extra_chargers
    else:
        total_chargers = base_chargers

    chargers = [0] * total_chargers

    total_wait = 0
    total_idleness = 0
    attended = 0

    queue = []

    current_time = 0
    i = 0

    while i < len(cars) or queue:

        while i < len(cars) and cars[i]["arrival"] <= current_time:
            queue.append(cars[i])
            i += 1

        if mode in ["software", "hybrid", "full"]:
            queue.sort(key=lambda x: (
                -x["priority"],
                not x["reserved"],
                x["arrival"]
            ))
        else:
            queue.sort(key=lambda x: x["arrival"])

        for c in range(total_chargers):
            if chargers[c] <= current_time and queue:
                car = queue.pop(0)

                arrival = car["arrival"]
                charge = car["charge"]
                delay = car["delay"]

                wait = current_time - arrival

                if wait > 60 and random.random() < 0.5:
                    continue

                if car["lazy"]:
                    delay += random.randint(10, 25)

                # =========================

                if mode in ["software", "hybrid", "full"]:
                    if random.random() < 0.7:
                        delay = int(delay * random.uniform(0.3, 0.7))

                    if car["priority"] == 3:
                        charge = int(charge * 0.85)

                    if random.random() < 0.1 and mode == "software":
                        delay += random.randint(5, 15)

                    overhead = random.choice([0, 1, 2])
                else:
                    overhead = 0

                if mode in ["hardware", "hybrid", "hardware_plus", "full"]:
                    delay = int(delay * random.uniform(0.2, 0.5))

                if mode in ["hybrid", "full"]:
                    active = sum(1 for x in chargers if x > current_time)
                    max_power = int(total_chargers * 0.6)

                    if active > max_power:
                        if random.random() < 0.5:
                            charge = int(charge * 1.2)

                # =========================

                end = current_time + charge + overhead
                chargers[c] = end + delay

                total_wait += max(wait, 0)
                total_idleness += delay
                attended += 1

        current_time += 1

    if attended == 0:
        return 0, 0

    return total_wait / attended, total_idleness / attended

# =============================

executions = 5

modes = ["none", "software", "hardware", "hybrid", "hardware_plus", "full"]

results = {m: [] for m in modes}

for i in range(executions):
    cars = generate_cars()

    print(f"\nExecução {i+1}:")

    for m in modes:
        res = simulate(cars, m)
        results[m].append(res)

        label = {
            "none": "Sem sistema",
            "software": "Só software",
            "hardware": "Só hardware",
            "hybrid": "Hardware + software",
            "hardware_plus": "Hardware + mais carregadores",
            "full": "Completo (tudo)"
        }

        print(f"{label[m]} -> Espera: {res[0]:.2f} | Ociosidade: {res[1]:.2f}")


def average(lst):
    return sum(x[0] for x in lst)/len(lst), sum(x[1] for x in lst)/len(lst)


print(f"\n=== RESULTADO MÉDIO ({executions} execuções) ===\n")

averages = {}

for m in modes:
    avg = average(results[m])
    averages[m] = avg
    print(f"{m}: Espera: {avg[0]:.2f} | Ociosidade: {avg[1]:.2f}")


def improvement(a, b):
    return ((a - b) / a) * 100


print("\n=== MELHORIAS (vs base) ===")

base = averages["none"]

for m in modes[1:]:
    print(f"\n{m}:")
    print(f"Espera: {improvement(base[0], averages[m][0]):.2f}%")
    print(f"Ociosidade: {improvement(base[1], averages[m][1]):.2f}%")