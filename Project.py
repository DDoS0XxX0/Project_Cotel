import random
import time
import os

# --- Модель объекта управления ---
class Boiler:
    def __init__(self):
        self.temp = 20.0      # температура
        self.pressure = 1.0   # давление
        self.level = 50.0     # уровень жидкости (%)
        self.heater_on = False
        self.pump_on = False

    def update(self):
        # Динамика: нагреватель повышает температуру, насос снижает уровень
        if self.heater_on:
            self.temp += random.uniform(0.5, 1.5)
        else:
            self.temp -= random.uniform(0.2, 0.8)
        if self.pump_on:
            self.level -= random.uniform(1, 3)
        else:
            self.level += random.uniform(0.5, 1)
        # Давление зависит от температуры
        self.pressure = 1.0 + (self.temp - 20) * 0.05 + random.uniform(-0.1, 0.1)
        # Ограничения
        self.temp = max(15, min(120, self.temp))
        self.pressure = max(0.8, min(2.5, self.pressure))
        self.level = max(0, min(100, self.level))

    def check_alarms(self):
        alarms = []
        if self.temp > 90:
            alarms.append("⚠️ АВАРИЯ: Перегрев!")
        if self.pressure > 2.0:
            alarms.append("⚠️ АВАРИЯ: Избыточное давление!")
        if self.level < 10:
            alarms.append("⚠️ АВАРИЯ: Низкий уровень!")
        return alarms

# --- Интерфейс диспетчера ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_status(boiler):
    print("=" * 40)
    print("             КОТЕЛЬНАЯ")
    print("=" * 40)
    print(f"Температура: {boiler.temp:.1f} °C")
    print(f"Давление:    {boiler.pressure:.2f} бар")
    print(f"Уровень:     {boiler.level:.1f} %")
    print("-" * 40)
    print(f"Нагреватель: {'ВКЛЮЧЕН' if boiler.heater_on else 'выключен'}")
    print(f"Насос:       {'ВКЛЮЧЕН' if boiler.pump_on else 'выключен'}")
    print("-" * 40)
    alarms = boiler.check_alarms()
    if alarms:
        for a in alarms:
            print(a)
    else:
        print("✓ Режим работы – нормальный")
    print("=" * 40)
    print("[1] Вкл/Выкл нагреватель")
    print("[2] Вкл/Выкл насос")
    print("[q] Выход")

# --- Главный цикл ---
boiler = Boiler()
running = True

while running:
    clear_screen()
    show_status(boiler)
    key = input("\nКоманда: ").strip().lower()
    if key == '1':
        boiler.heater_on = not boiler.heater_on
        print(f"Нагреватель {'включен' if boiler.heater_on else 'выключен'}")
        time.sleep(1)
    elif key == '2':
        boiler.pump_on = not boiler.pump_on
        print(f"Насос {'включен' if boiler.pump_on else 'выключен'}")
        time.sleep(1)
    elif key == 'q':
        running = False
    # Обновление параметров происходит каждый цикл
    boiler.update()