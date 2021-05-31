import math
import datetime
import time
from mqtt_subscriber import MqttSubscriber


class Inertial_navigation:
    def __init__(self):
        "mqtt initiation"
        self.magnetometer = MqttSubscriber("localhost", topic="magnetometer_LSM303AGR")
        self.magnetometer.start()

        self.gyroscope = MqttSubscriber("localhost", topic="gyroscope_LSM6DSL")
        self.gyroscope.start()

        self.accelerometer = MqttSubscriber("localhost", topic="accelerometer_LSM6DSL") #_LSM6DSL #_LSM303AGR
        self.accelerometer.start()

        self.RAD_TO_DEG = 57.29578
        self.M_PI = math.pi
        self.G_GAIN = 1         # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
        self.AA =  0.40              # Complementary filter constant
        self.MAG_LPF_FACTOR = 0.4    # Low pass filter constant magnetometer
        self.ACC_LPF_FACTOR = 0.4    # Low pass filter constant for accelerometer
        self.ACC_MEDIANTABLESIZE = 9         # Median filter table size for accelerometer. Higher = smoother but a longer delay
        self.MAG_MEDIANTABLESIZE = 9         # Median filter table size for magnetometer. Higher = smoother but a longer delay


        # Kalman filter variables
        self.Q_angle = 0.02
        self.Q_gyro = 0.0015
        self.R_angle = 0.005
        self.y_bias = 0.0
        self.x_bias = 0.0
        self.XP_00 = 0.0
        self.XP_01 = 0.0
        self.XP_10 = 0.0
        self.XP_11 = 0.0
        self.YP_00 = 0.0
        self.YP_01 = 0.0
        self.YP_10 = 0.0
        self.YP_11 = 0.0
        self.KFangleX = 0.0
        self.KFangleY = 0.0

        self.ACCx = 0
        self.ACCy = 0
        self.ACCz = 0
        self.GYRx = 0
        self.GYRy = 0
        self.GYRz = 0
        self.MAGx = 0
        self.MAGy = 0
        self.MAGz = 0

        self.a = datetime.datetime.now()

    def kalmanFilterX(self, accAngle, gyroRate, DT):
        x = 0.0
        S = 0.0

        KFangleX = self.KFangleX + DT * (gyroRate - self.x_bias)

        self.XP_00 = self.XP_00 + \
            (- DT * (self.XP_10 + self.XP_01) + self.Q_angle * DT)
        self.XP_01 = self.XP_01 + (- DT * self.XP_11)
        self.XP_10 = self.XP_10 + (- DT * self.XP_11)
        self.XP_11 = self.XP_11 + (+ self.Q_gyro * DT)

        x = accAngle - KFangleX
        S = self.XP_00 + self.R_angle
        self.K_0 = self.XP_00 / S
        self.K_1 = self.XP_10 / S

        self.KFangleX = self.KFangleX + (self.K_0 * x)
        self.x_bias = self.x_bias + (self.K_1 * x)

        self.XP_00 = self.XP_00 - (self.K_0 * self.XP_00)
        self.XP_01 = self.XP_01 - (self.K_0 * self.XP_01)
        self.XP_10 = self.XP_10 - (self.K_1 * self.XP_00)
        self.XP_11 = self.XP_11 - (self.K_1 * self.XP_01)

        return self.KFangleX

    def kalmanFilterY(self, accAngle, gyroRate, DT):
        y = 0.0
        S = 0.0

        self.KFangleY = self.KFangleY + DT * (gyroRate - self.y_bias)

        self.YP_00 = self.YP_00 + \
            (- DT * (self.YP_10 + self.YP_01) + self.Q_angle * DT)
        self.YP_01 = self.YP_01 + (- DT * self.YP_11)
        self.YP_10 = self.YP_10 + (- DT * self.YP_11)
        self.YP_11 = self.YP_11 + (+ self.Q_gyro * DT)

        y = accAngle - self.KFangleY
        S = self.YP_00 + self.R_angle
        self.K_0 = self.YP_00 / S
        self.K_1 = self.YP_10 / S

        self.KFangleY = self.KFangleY + (self.K_0 * y)
        self.y_bias = self.y_bias + (self.K_1 * y)

        self.YP_00 = self.YP_00 - (self.K_0 * self.YP_00)
        self.YP_01 = self.YP_01 - (self.K_0 * self.YP_01)
        self.YP_10 = self.YP_10 - (self.K_1 * self.YP_00)
        self.YP_11 = self.YP_11 - (self.K_1 * self.YP_01)

        return self.KFangleY

    
    def accXYangle(self):
        self.AccXangle =  (math.atan2(self.ACCy,self.ACCz)*self.RAD_TO_DEG)
        self.AccYangle =  (math.atan2(self.ACCz,self.ACCx)+math.pi)*self.RAD_TO_DEG
        
        if self.AccYangle > 90:
            self.AccYangle -= 270.0
        else:
            self.AccYangle += 90.0
        return [self.AccXangle, self.AccYangle]
    
    def gyro_to_angle(self):
        #Convert Gyro raw to degrees per second
        rate_gyr_x =  self.GYRx * self.G_GAIN
        rate_gyr_y =  self.GYRy * self.G_GAIN
        rate_gyr_z =  self.GYRz * self.G_GAIN
        return [rate_gyr_x, rate_gyr_y]

    def loop_time(self):
        b = datetime.datetime.now() - self.a
        self.a = datetime.datetime.now()
        LP = b.microseconds/(1000000*1.0)
        return LP
        # outputString = "Loop Time %5.2f " % ( LP )

    def axsis_distribution(self):
        if self.magnetometer.pos and self.accelerometer.pos and self.gyroscope.pos:

            self.ACCx = test.accelerometer.pos[0]/1000
            self.ACCy = test.accelerometer.pos[1]/1000
            self.ACCz = test.accelerometer.pos[2]/1000
            self.GYRx = test.gyroscope.pos[0]/1000
            self.GYRy = test.gyroscope.pos[1]/1000
            self.GYRz = test.gyroscope.pos[2]/1000
            self.MAGx = test.magnetometer.pos[0]/1000
            self.MAGy = test.magnetometer.pos[1]/1000
            self.MAGz = test.magnetometer.pos[2]/1000

if __name__ == "__main__":
    test = Inertial_navigation()
    while True:

        lp = test.loop_time()
        test.axsis_distribution()
        accXangle = test.accXYangle()[0]
        accYangle = test.accXYangle()[1]

        rate_gyrX = test.gyro_to_angle()[0]
        rate_gyrY = test.gyro_to_angle()[1]

        x = test.kalmanFilterX(accXangle, rate_gyrY, lp)
        y = test.kalmanFilterY(accYangle, rate_gyrY, lp)
        print(f"x: {x}, y: {y}")
        time.sleep(0.2)