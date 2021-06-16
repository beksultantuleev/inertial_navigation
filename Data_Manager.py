
import csv
import random
import time

'i gues i dont need it'
class Data_Manager:
    def __init__(self):
        self.fieldnames = ["index", "posX", "posY", "posZ"]
        self.x_value = 1
        self.posX = 0
        self.posY = 0
        self.posZ = 0

        with open('data.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            csv_writer.writeheader()

    def start(self, X, Y, Z):

        with open('data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)

            info = {
                "index": self.x_value,
                "posX": X,
                "posY": Y,
                "posZ": Z
            }

            csv_writer.writerow(info)
            print(X, Y, Z)

            self.x_value += 1



if __name__ == "__main__":
    test = Data_Manager()
    while True:
        test.start(random.randint(1, 6), random.randint(1, 6), random.randint(1, 6))
