import paho.mqtt.client as mqtt
import time

IP_DU_CLOUD_PC = "192.168.1.77" 
TOPIC_EDGE = "capteur/temperature"    
TOPIC_CLOUD = "cloud/moyenne"         

liste_donnees = []
PERIODE = 5.0 

def on_message(client, userdata, msg):
    try:
        valeur = float(msg.payload.decode())
        liste_donnees.append(valeur)
    except ValueError:
        pass 

client_edge = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Edge_Filter_Final")
client_edge.on_message = on_message
client_edge.connect("127.0.0.1", 1883, 60)
client_edge.subscribe(TOPIC_EDGE) 
client_edge.loop_start() 

client_cloud = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Edge_To_Cloud_Final")
try:
    client_cloud.connect(IP_DU_CLOUD_PC, 1883, 60)
    print("Filtrage Edge : Connecté au Cloud !")
except Exception as e:
    print(f"Erreur Cloud : {e}")
    exit()

print(f"Système de filtrage actif (période de {PERIODE}s).")
try:
    while True:
        time.sleep(PERIODE) 
        if len(liste_donnees) > 0:
            moyenne = sum(liste_donnees) / len(liste_donnees)
            message = f"{moyenne:.2f}"
            client_cloud.publish(TOPIC_CLOUD, message)
            print(f"-> Envoyé au Cloud : {message} (calculé sur {len(liste_donnees)} valeurs)")
            liste_donnees.clear()
        else:
            print("-> Aucune donnée reçue pendant cette période...")
except KeyboardInterrupt:
    client_edge.loop_stop()
    client_edge.disconnect()
    client_cloud.disconnect()