from tkinter import *
from venv import create

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import networkx as nx

from tarjan_planner.config_manager import ConfigManager

def plot_graph():
    # Tried several different methods to get a working ui running, this is the closest i managed
    relatives = get_plots()

    g = nx.Graph()
    longitudes = []
    latitudes = []
    for relative in relatives:
        latitude = relatives[relative]["latitude"]
        longitude = relatives[relative]["longitude"]
        longitudes.append(longitude)
        latitudes.append(latitude)
        #g.add_node(relatives[relative]["street_name"], pos=(longitude, latitude))
        #g.add_edge(u_of_edge=(longitude, latitude), v_of_edge=(longitude, latitude))

    longitudes = np.array(longitudes)
    latitudes = np.array(latitudes)


    # g.add_edge(1, 2)
    # g.add_edge(2, 3)
    # g.add_edge(3, 4)
    # g.add_edge(1, 4)
    # g.add_edge(1, 5)

    #nx.draw(g, with_labels=True)
    long = [100, 120, 140, 160]
    lat = [20, 30, 40, 50]
    plt.scatter(longitudes, latitudes)
    plt.title("Tarjan Planner")
    plt.xlabel("longitude")
    plt.ylabel("latitude")
    plt.grid()
    plt.axis("on")
    plt.show()

def get_plots():
    relatives = ConfigManager.load_config("relatives")
    return relatives




