from datetime import time
import numpy as np
from numpy.linalg import multi_dot


class KalmanFilterUWB:
    def __init__(self, q):
        '''"
        Give matrices for an estimator of the form
        _____
        q_pred = A*q + G*[ax, ay, az]  |ax+bu
        p_pred = A*Pup*A.T + GQG.T |c + du
        z = [x,y,z, x1,y1,z1]
        '''
        self.z = []
        self.A = np.eye(np.size(q, 0))
        self.G = np.eye(np.size(q, 0)) * 0.5  # for 2 Hz we multiply by 0.5. im trying 0.2
        self.H = np.array(
            [[1.0, 0.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0]])
        self.R = np.array(
            [[0.5, 0, 0, 0, 0, 0],
             [0, 0.5, 0, 0, 0, 0],
             [0, 0, 0.1, 0, 0, 0],
             [0, 0, 0, 0.4, 0, 0],
             [0, 0, 0, 0, 0.4, 0],
             [0, 0, 0, 0, 0, 100]])
        self.Q = np.eye(np.size(q, 0))   # process noise it was * 0.5
        self.q = q

        self.S = []

    # def get_state_estimation(self, q, u, z, p_update_old, FLAG):

    def get_state_estimation(self, q, u, z, p_update_old, FLAG):
        self.q = q
        self.u = np.matrix(u).T  # transpose it
        self.z = np.matrix(z).T

        if len(self.z) == 3:
            self.H = np.eye(3)
            self.R = np.array(
                [[0.5, 0, 0],
                 [0, 0.5, 0],
                 [0, 0, 0.5]
                 ])  # measurement noise //0.3 >>2- meters instead of 1 //8 is good

        self.p_update_old = p_update_old
        self.FLAG = FLAG

        self.q_prediction = np.dot(self.A, self.q)+np.dot(self.G, self.u)
        self.p_prediction = multi_dot(
            [self.A, self.p_update_old, self.A.T]) + multi_dot([self.G, self.Q, self.G.T])

        if self.FLAG:
            self.s_update =np.dot( np.dot(self.H, self.p_prediction), self.H.T) + self.R
            # print(f"s_update>>{self.s_update}")
            self.W_gain = multi_dot(
                [self.p_prediction, self.H.T, np.linalg.inv(self.s_update)])

            self.q_update = self.q_prediction + \
                np.dot(self.W_gain,  (self.z - np.dot(self.H, self.q_prediction)))
            # print(f"q_update>>{self.q_update}")
            self.p_update = np.dot(
                (np.eye(3)-np.dot(self.W_gain, self.H)), self.p_prediction)
            # print(f"self.p_update >> \n{self.p_update}")
        else:
            self.p_update = self.p_prediction
            self.q_update = self.q_prediction
        self.S = [self.p_update, self.q_update]  # modification part
        return self.S
        # return self.q_update.T.tolist()[0]


if __name__ == "__main__":
    from mqtt_subscriber import MqttSubscriber
    import time

    q = np.zeros((3, 1))
    p = np.zeros((3, 3))
    state = KalmanFilterUWB(q)
    accelerometer = MqttSubscriber("localhost", topic="accelerometer_LSM303AGR")
    accelerometer.start()
    First_time = True
    while True:
        u_raw = []
        if accelerometer.pos:
            xu = accelerometer.pos[0]
            yu = accelerometer.pos[1]
            zu = accelerometer.pos[2]
            u_raw = [xu, yu, zu]

            u = []# current speed_x, speed_y, speed_z
            for value in u_raw:
                # if abs(value)>9:
                #     if value>0:
                #         value = value-9.8
                #     else:
                #         value = value+9.8
                if abs(value)<0.5:
                    # if value>0 or value<0:
                    value = 0
                u.append(value)
            # print(u)
            if First_time:
                z = [0, 0, 0]
            First_time = False



            p, q = state.get_state_estimation(q, u, z, p, True)
            
            if not First_time:
                z = q.T.tolist()[0]
            # # print(f"this is p >>\n{p1}")
            print(f"pos >>\tx\ty\tz\n\t\t\t{q.T.tolist()[0]}")
            time.sleep(0.3)