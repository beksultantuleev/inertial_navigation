
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()


def animate(i):
    data = pd.read_csv('data.csv')
    x = data['index']
    y1 = data['posX']
    y2 = data['posY']
    y3 = data["posZ"]

    plt.cla()

    ax = plt.axes(projection='3d')
    ax.plot3D(y1, y2,  y3, "green",label = "movement")

    # plt.plot(y1, y2, label='movement')
    plt.xlabel("Y")
    plt.ylabel("X")
    plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=100)

plt.tight_layout()
plt.show()