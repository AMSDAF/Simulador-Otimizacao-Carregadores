import random

num_chargers = 6
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
        delay = random.choices([0, 5, 10, 15, 20], weights=[30, 25, 20, 15, 10])[0]

        cars.append({
            "arrival": arrival,
            "charge": charge,
            "delay": delay
        })

        current_time = arrival

    return cars

def simulate(cars, system = False):
    chargers = [0] * num_chargers
    total_wait = 0
    total_idleness = 0

    for car in cars:
        arrival = car["arrival"]
        charge = car["charge"]
        delay = car["delay"]

        idx = chargers.index(min(chargers))
        free_time = chargers[idx]

        start = max(arrival, free_time)
        wait = start - arrival

        if system:
            if random.random() < 0.6:
                delay = int(delay * random.uniform(0.3, 0.7))
        
        end = start + charge
        chargers[idx] = end + delay

        total_wait += wait
        total_idleness += delay

    return total_wait / num_cars, total_idleness / num_cars

executions = 5

wait_with = []
wait_without = []
idleness_with = []
idleness_without = []

for i in range(executions):
    cars = generate_cars()

    without = simulate(cars, False)
    with_ = simulate(cars, True)

    wait_without.append(without[0])
    wait_with.append(with_[0])
    idleness_without.append(without[1])
    idleness_with.append(with_[1])

    print(f"\nExecução {i+1}:")
    print(f"Sem sistema -> Espera: {without[0]:.2f} | Ociosidade: {without[1]:.2f}")
    print(f"Com sistema -> Espera: {with_[0]:.2f} | Ociosidade: {with_[1]:.2f}")

medium_wait_without = sum(wait_without) / executions
medium_wait_with = sum(wait_with) / executions
medium_idleness_without = sum(idleness_without) / executions
medium_idleness_with = sum(idleness_with) / executions

print(f"=== RESULTADO MÉDIO ({executions} execuções) ===\n")

print("Sem o nosso sistema: ")
print(f"Tempo médio de espera: {medium_wait_without:.2f} min")
print(f"Ociosidade média: {medium_idleness_without:.2f} min")

print("\nCom o nosso sistema: ")
print(f"Tempo médio de espera: {medium_wait_with:.2f} min")
print(f"Ociosidade média: {medium_idleness_with:.2f} min")

wait_improvement = ((medium_wait_without - medium_wait_with) / medium_wait_without) * 100
idleness_improvement = ((medium_idleness_without - medium_idleness_with) / medium_idleness_without) * 100

print("\n=== MELHORIAS ===")
print(f"Redução no tempo de espera: {wait_improvement:.2f}%")
print(f"Redução na ociosidade: {idleness_improvement:.2f}%")