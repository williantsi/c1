import json, requests 
from datetime import datetime
from datetime import timedelta
import time
import paho.mqtt.client as paho

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
    
user = "gockejzx"
password = "Vs4ughu-_nzO"
 
client = paho.Client()
client.on_publish = on_publish
client.username_pw_set(user, password=password) 
client.connect("driver.cloudmqtt.com", 18951)

client.loop_start()

while True: 

    url = requests.get("https://esp8266-4c64e-default-rtdb.firebaseio.com/test.json")
    text = url.text

    data = json.loads(text)
    
    data_e_hora_atuais = datetime.now()
    data_e_hora_atuais = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M:%S")
    data_e_hora_atuais = datetime.strptime(data_e_hora_atuais, '%d/%m/%Y %H:%M:%S')
    data_e_hora_atuais = datetime.timestamp(data_e_hora_atuais)
    data_e_hora_atuais = int(data_e_hora_atuais)
    
    data_e_hora_esp = data["hora"]
   # data_e_hora_esp = data_e_hora_esp.strftime("%d/%m/%Y %H:%M:%S")
    data_e_hora_esp = datetime.strptime(data_e_hora_esp, '%d/%m/%Y %H:%M:%S')
    data_e_hora_esp = datetime.timestamp(data_e_hora_esp)
    data_e_hora_esp = int(data_e_hora_esp)


    diff = data_e_hora_atuais-data_e_hora_esp
    
    print(diff)
    
    if (diff >= 86420):
        print("Desligado")
        (rc, mid) = client.publish("copabase/c6/toggle", "0", qos=0)
        (rc, mid) = client.publish("copabase/c6/temperatura", data["temperatura"], qos=0)
        (rc, mid) = client.publish("copabase/c6/text", data["hora"], qos=0)
    else:
        print("Ligado")
        (rc, mid) = client.publish("copabase/c6/toggle", "1", qos=0)
        (rc, mid) = client.publish("copabase/c6/temperatura", data["temperatura"], qos=0)
        (rc, mid) = client.publish("copabase/c6/text", data["hora"], qos=0)
    time.sleep(2)



