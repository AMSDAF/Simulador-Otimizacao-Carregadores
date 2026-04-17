import random

num_chargers = 6
num_cars = 20

cars = []

current_time = 0
for i in range(num_cars):
    arrival = current_time + random.randint(5, 20)
    charge = random.randint(40, 90)
    delay = random.choice([0, 10, 20])

    cars.append({
        "arrival": arrival,
        "charge": charge,
        "delay": delay
    })

    current_time = arrival

def simulate(system = False):
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
            delay = int(delay * 0.4)
        
        end = start + charge + delay

        chargers[idx] = end

        total_wait += wait
        total_idleness += delay
    
    average_waiting_time = total_wait / num_cars
    average_idleness = total_idleness / num_cars

    return average_idleness, average_waiting_time

no_system = simulate(system = False)
with_system = simulate(system = True)

print("Sem o nosso sistema: ")
print(f"Tempo médio de espera: {no_system[0]:.2f} min")
print(f"Ociosidade média: {no_system[1]:.2f} min")

print("\nCom o nosso sistema: ")
print(f"Tempo médio de espera: {with_system[0]:.2f} min")
print(f"Ociosidade média: {with_system[1]:.2f} min")