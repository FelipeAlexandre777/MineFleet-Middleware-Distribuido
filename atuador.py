import paho.mqtt.client as mqtt
def connected(c,u,f,rc,props):
    print("Atuador conectado:",rc); c.subscribe("minefleet/caminhoes/alertas",qos=1)
def message(c,u,m): print("Atuador recebeu:",m.payload.decode())
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id="minefleet-atuador")
c.on_connect=connected; c.on_message=message; c.connect("localhost",1883,60)
print("Aguardando alertas. Ctrl+C para parar.")
try: c.loop_forever()
except KeyboardInterrupt: c.disconnect()
