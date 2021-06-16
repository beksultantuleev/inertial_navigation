from Dead_reckoning import Dead_Reckoning
from Mqtt_manager import Mqtt_Manager
from Data_Manager import Data_Manager

import time
phone = False
if phone:
    "mqtt initiation"
    magnetometer = Mqtt_Manager("localhost", "magnetometer_phone")
    gyroscope = Mqtt_Manager("localhost", "gyroscope_phone")
    accelerometer = Mqtt_Manager("localhost", "accelerometer_phone")
else:
    magnetometer = Mqtt_Manager("localhost", "magnetometer_LSM303AGR")
    gyroscope = Mqtt_Manager("localhost", "gyroscope_LSM6DSL")
    # accelerometer = MqttSubscriber("localhost", "accelerometer_LSM6DSL")
    accelerometer = Mqtt_Manager("localhost", "accelerometer_LSM303AGR")

step = 0
delta_t = 0.01 #0.002
test = Dead_Reckoning()
file_writer = Data_Manager()
while step<80:

    if len(magnetometer.processed_data_nested) > 0 and len(accelerometer.processed_data_nested) > 0 and len(gyroscope.processed_data_nested) > 0:
        time.sleep(0.1)
        test.simulate(accelerometer.processed_data_nested,
                        gyroscope.processed_data_nested, delta_t)
        
        magnetometer.publish("X", test.fixed_x)
        magnetometer.publish("Y", test.fixed_y)
        magnetometer.publish("Z", test.fixed_z)
        # file_writer.start(test.fixed_x, test.fixed_y, test.fixed_z)
        step += 1

test.plot_traj()