import paho.mqtt.client as mqtt
import threading
import time


class MqttSubscriber:
    def __init__(self, brokerip=None, brokerport=1883, topic=None):
        self.__brokerip = brokerip
        self.__brokerport = brokerport
        self.__topic = topic
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        self.message = None
        self.receive = True
        self.start_loc = None
        self.end_loc = None
        self.pos = [] #[0,0,0]
        self.checker = False

    def __on_connect(self, client, userdata, flags, rc):
        print("** subscriber connection **")
        self.__client.subscribe(self.__topic, qos=0)

    def __on_disconnect(self, client, userdata, rc):
        print("** disconnection **")

    def __on_message(self, client, userdata, message):
        # print(message.topic)
        data = message.payload[1:-1].decode("utf-8").split(",") #change here
        # print(data)
        self.pos = [float(data[0]), float(data[1]), float(data[2])]
        # self.lis = [self.pos[0], self.pos[1], self.pos[2]]
        self.checker = True

    def start(self):
        thread = threading.Thread(target=self.__subscribe)
        thread.start()

    def __subscribe(self):
        self.__client.connect(self.__brokerip, self.__brokerport)
        self.__client.loop_forever()
        # self.__client.loop_start()

    def stop(self):
        self.__client.unsubscribe(self.__topic)
        self.__client.disconnect()

    # def get_pos(self)
    #     return

if __name__ == '__main__':
    mqttSubscriber = MqttSubscriber("localhost", topic="magnetometer")
    mqttSubscriber.start()
    # tmp = mqttSubscriber.pos
    # tmp1 = tmp
    
    while(1):
        # print(tmp[:-2])
        # print(tmp[:-2])
        print(mqttSubscriber.pos)
        # print(mqttSubscriber.pos[0:1])
        time.sleep(0.3)
        print(mqttSubscriber.checker)