import paho.mqtt.client as mqttClient
import time
import json

class Mqtt_Manager:
    
    Connected = False  # global variable for the state of the connection

    def __init__(self, host, port, user=None, passwd=None):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.client = mqttClient.Client() 
        self.client.on_connect = self.on_connect  # attach function to callback
        self.client.on_message = self.on_message 
        self.data = []
        self.multiple_data = []
        self.hitcounter = 0

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            global Connected  # Use global variable
            Connected = True  # Signal connection
        else:
            print("Connection failed")

    def on_message(self, client, userdata, message):
        'change here if want different data structure'
        # print(message.payload.decode("utf-8"))
        self.data = message.payload.decode("utf-8")
        # if self.hitcounter>1:
        #     self.multiple_data = [float(i) for i in self.data[1:-1].split(",")]

        print(self.data)
        # processed_data = json.loads(self.data)
        # print(self.multiple_data[0])
        # print(processed_data[1])


    def connect(self):
        self.client.connect(self.host, port=self.port)  # connect to broker
        self.client.loop_start()  # start the loop

    def subs(self, *args):
        local_counter = 0
        ids = []
        # self.hitcounter+=1
        for topics in args:
            local_counter+=1
            ids.append(local_counter)   
        self.client.subscribe(list(zip(args, ids)))  # topic
    
    def publish(self, topc, msg):
        print("published!")
        self.client.publish(topc, msg)

# try:
#     while True:
#         time.sleep(2)
#         # value = "from subs"
#         # client.publish("my_publish_test", value)

# except KeyboardInterrupt:
#     print("exiting")
#     client.disconnect()
#     client.loop_stop()
if __name__=="__main__":
    test = Mqtt_Manager("localhost", 1883)
    test.connect()
    test.subs("accelerometer_LSM303AGR", "gyroscope_LSM6DSL")#gyroscope_LSM6DSL
    # test.subs("gyroscope_LSM6DSL")
    while True:
        time.sleep(0.1)
        # print(test.data)
        # test.publish("A", "works!!")
        # test.publish("B", "works2!!")
