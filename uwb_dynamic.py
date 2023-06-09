import serial
import time
import re
from Measurement import Measurement
ser = serial.Serial('/dev/ttyACM0', 115200)
from GradientDescent import GradientDescent


import paho.mqtt.client as mqtt

# the callback for when the client receives a connack response from the server.
def on_connect(client, userdata, flags, rc):
    print("connected with result code "+str(rc))
    client.subscribe("location/#")
# the callback for when a publish message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# the callback for when a message is published to the server.
def on_publish(client, userdata, result): 
    print("data published.")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.connect("192.168.1.5", 1883, 60)

# Publish a message.
client.publish("location/NewLocation", '{"xCoordinate":100,"yCoordinate":0,"zCoordinate":0}')

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()



anchor_data = {}
AP_location= {
    'D62A':{
     'POS': 1,
      'SSID': 'D62A',
      'x': 1.00,
      'y': 1.45,
      'z': 0.8,
    },
    '5A33':{
      'POS': 1,
      'SSID': '5A33',
      'x': 1.00,
      'y': 5.00,
      'z': 0.80,
    },
    'CBAF':{
      'POS': 2,
      'SSID': 'CBAF',
      'x': 9.00,
      'y': 5.00,
      'z': 0.80,
    },
    '868C':{
      'POS': 3,
      'SSID': '868C',
      'x': 7.00,
      'y': 1.00,
      'z': 0.80,
    }
}

gradient_descent = GradientDescent(
    learning_rate=0.01, max_iterations=1000, tolerance=1e-5
)
# Define the callback function
def callback_function(data):
    # Perform additional actions as needed
    measurements = []
    for key,value in data.items():
        M = Measurement(value['t'],key,float(value['v']),0,AP_location[key])
        measurements.append(M)
    pos = gradient_descent.train(measurements, {"x": 0, "y": 0, "z": 0})
    print(pos)
    client.publish("location/NewLocation", f'{pos}')
start_time = time.monotonic()

# Loop indefinitely
while True:
    # Read the output from Minicom
    output_bytes = ser.readline()
    try:
        output = output_bytes.decode('ISO-8859-1', errors='ignore')
    except UnicodeDecodeError:
        # Skip over any invalid bytes
        continue

    # Add a timestamp to each line of output
    milliseconds = int(round(time.time() * 1000))
    pattern = r"(\b\w{4}\b)(\[\d+\.\d+,\d+\.\d+,\d+\.\d+\])=(\d+\.\d+)"
    matches = re.findall(pattern, output)
    for match in matches:
        identifier = match[0]
        measurements = match[1]
        value = match[2]
        anchor_data[identifier] = {'v': value, 't': milliseconds}
        # print("Identifier:", identifier)
        # print("Value:", anchor_data[identifier])
        # print()
    all_measurements_valid = all(
        abs(milliseconds - data['t']) <= 100 for data in anchor_data.values()
    )
    #print(all_measurements_valid)
    if all_measurements_valid:
        # Call the callback function
        callback_function(anchor_data)



