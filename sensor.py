import json,time,random,paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id="minefleet-sensor")
c.connect("localhost",1883,60); c.loop_start()
print("Sensor publicando. Ctrl+C para parar.")
seq=1
try:
    while True:
        data={"vehicle_id":"CAM-042","sequence":seq,"temperature":round(random.uniform(65,95),1)}
        info=c.publish("minefleet/caminhoes/telemetria",json.dumps(data),qos=1); info.wait_for_publish()
        print("Publicado:",data); seq+=1; time.sleep(3)
except KeyboardInterrupt: pass
finally: c.loop_stop(); c.disconnect()
