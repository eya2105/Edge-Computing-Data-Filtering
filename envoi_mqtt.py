import paho.mqtt.client as mqtt
import time
import math
import random
from simulateur_capteur import Simulateur


IP_DE_TA_VM = "192.168.1.172" 
TOPIC = "capteur/temperature"


#MODE = "PERIODIQUE"
MODE = "POISSON"  


LAMBDA = 10  # 10 messages par seconde en moyenne

def next_time_interval(l):
    n = random.random() * 1.0
    return -math.log(1.0 - n) / l


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "PC_Capteur")
client.connect(IP_DE_TA_VM, 1883, 60)
print(f"Connecté au broker Edge. Mode : {MODE}")

sim = Simulateur(seed=12345, mean=20, standard_deviation=5, error_rate=0.01, error_length=4.21, minimum=0, maximum=40)
NbreMessages = 10000 
Time = 0

print("Début de l'envoi...")

try:
    for i in range(NbreMessages):
        # 1. Calcul du délai selon le mode choisi
        if MODE == "PERIODIQUE":
            time.sleep(1) 
            Time += 1
        else:
            tt = next_time_interval(LAMBDA)
            time.sleep(tt)
            Time += tt
        
        # 2. Génération et envoi de la valeur
        valeur = sim.calculate_next_value()
        message = f"{valeur:.2f}"
        client.publish(TOPIC, message)
        
        # 3. Affichage
        print(f"Publishing Time: {Time:.2f}s | Envoyé : {message}")
        
except KeyboardInterrupt:
    print("\nArrêt de l'envoi.")
    client.disconnect()