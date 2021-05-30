from typing import ValuesView
import numpy.matlib
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot
import matplotlib.animation as animation
from collections import deque

'''
Python-based dead reckoning algorithm for inertial navigation system
System Input:
	- Accelerometer Data
	- Gyroscope Data
'''


def sin(x):
    return math.sin(x)


def cos(x):
    return math.cos(x)


class Dead_Reckoning():
    def __init__(self):
        # Raw data from accelerometer and gyroscope
        self.globalVec = [np.array([[0],
                                    [0],
                                    [0]])]
        self.globalPos = [np.array([[0],
                                    [0],
                                    [0]])]
        self.angles = [np.array([[0],
                                 [0],
                                 [0]])]
        # Initially, it is an identity matrix
        self.rotation_matrix = np.array([[1, 0, 0],
                                         [0, 1, 0],
                                         [0, 0, 1]])
        g = 9.81
        self.gravity = np.array([[0],
                                 [0],
                                 [-1*g]])
        self.x = [0]
        self.y = [0]
        self.z = [0]
        self.xhat = [np.array([[0.00001],
                               [0],
                               [0]])]

        self.yhat = [np.array([[0],
                               [0.00001],
                               [0]])]

        self.zhat = [np.array([[0],
                               [0],
                               [0.00001]])]

    def simulate(self, localAcc, localAngular, delta_t):
        self.raw_acc = localAcc
        self.raw_ang_vel = localAngular
        self.localAcc = localAcc
        self.delta_t = delta_t
        # for i in range(self.steps):
        # 	print("Step #: " + str(i))
        angle_delta = np.array(self.raw_ang_vel) * self.delta_t

        C = float(angle_delta[2])
        B = float(angle_delta[1])
        A = float(angle_delta[0])

        rotation = np.array([[cos(C)*cos(B), -1*sin(C)*cos(A) + cos(C)*sin(B)*sin(A), sin(C)*sin(A) + cos(C)*sin(B)*cos(A)],
                             [sin(C)*cos(B), cos(C)*cos(A) + sin(C)*sin(B) *
                              sin(A), -1*cos(C)*sin(A) + sin(C)*sin(B)*cos(A)],
                             [-1*sin(B), cos(B)*sin(A), cos(B)*cos(A)]])

        self.rotation_matrix = np.matmul(self.rotation_matrix, rotation)

        new_global_acc = self.rotation_matrix.dot(
            self.localAcc) - self.gravity  
        # print('Accel')
        # print(new_global_acc)

        new_global_vel = self.globalVec[-1] + self.delta_t * new_global_acc
        self.globalVec.append(new_global_vel)
        # print("Vel")
        # print(new_global_vel)

        new_global_pos = self.globalPos[-1] + self.delta_t * new_global_vel
        self.globalPos.append(new_global_pos)

        # print(f"Y is here>> {self.y[-1]}")
        self.x.append(float(new_global_pos[0]))
        self.y.append(float(new_global_pos[1]))
        self.z.append(float(new_global_pos[2]))
        print(f"X>>: {self.x[-1]}, Y>>: {self.y[-1]}, Z>>: {self.z[-1]}")
        # print(f"velX>>: {new_global_vel[0]}, velY>>: {new_global_vel[1]}, velZ>>: {new_global_vel[2]}")

        # print("X>>>: " + str(float(new_global_pos[0])))
        # print("Y>>>: " + str(float(new_global_pos[1])))
        # print("Z>>>: " + str(float(new_global_pos[2])))

        new_xhat = np.matmul(self.rotation_matrix, np.array([[1],
                                                            [0],
                                                            [0]]))

        new_yhat = np.matmul(self.rotation_matrix, np.array([[0],
                                                            [1],
                                                            [0]]))

        new_zhat = np.matmul(self.rotation_matrix, np.array([[0],
                                                            [0],
                                                            [1]]))

        self.xhat.append(new_xhat)
        self.yhat.append(new_yhat)
        self.zhat.append(new_zhat)

        # print("X-Hat")
        # print(new_xhat)
        # print("Y-Hat")
        # print(new_yhat)
        # print("Z-Hat")
        # print(new_zhat)

    def plot_traj(self):
        fig = pyplot.figure()
        ax = Axes3D(fig)
        ax.set_xlabel('$X$')
        ax.set_ylabel('$Y$')
        ax.set_zlabel('$Z$')
        # ax.set_xlim(-0.05,0.05)
        # ax.set_ylim(-0.05,0.05)
        # ax.set_zlim(-0.5,0.5)
        ax.set_title(
            "Dead Reckoning from Raw Accelerometer and Gyroscope Modules - Simulation")
        ax.scatter(self.x, self.y, self.z, s=[0.2]*len(self.x))
        ax.scatter([0], [0], [0], c="g")
        ax.scatter([self.x[-1]], [self.y[-1]], [self.z[-1]], c="r")
        pyplot.show()


if __name__ == "__main__":
    from mqtt_subscriber import MqttSubscriber
    import time
    "mqtt initiation"
    magnetometer = MqttSubscriber("localhost", topic="magnetometer_LSM303AGR")
    magnetometer.start()
    gyroscope = MqttSubscriber("localhost", topic="gyroscope_LSM6DSL")
    gyroscope.start()
    accelerometer = MqttSubscriber("localhost", topic="accelerometer_LSM6DSL")
    # accelerometer = MqttSubscriber("localhost", topic="accelerometer_LSM303AGR")
    accelerometer.start()
    step = 0
    delta_t = 0.03
    test = Dead_Reckoning()
    while step < 100:
        # if len(accelerometer.pos)>0:
        # 	print(accelerometer.pos)
        if len(magnetometer.pos_nested) > 0 and len(accelerometer.pos_nested) > 0 and len(gyroscope.pos_nested) > 0:
            time.sleep(0.2)
            # print(magnetometer.pos, step)

            test.simulate(accelerometer.pos_nested,
                          gyroscope.pos_nested, delta_t)
            step += 1

    test.plot_traj()
