import math

import numpy as np
import pandas as pd
import Constants as C
from matplotlib import use as use_agg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import PySimpleGUI as sg

def pack_figure(graph, figure):
    canvas = FigureCanvasTkAgg(figure, graph.Widget)
    plot_widget = canvas.get_tk_widget()
    plot_widget.pack(side='top', fill='both', expand=1)
    return plot_widget

def plot_figure(index, data, goal):
    fig = plt.figure(index)         # Active an existing figure
    ax = plt.gca()                  # Get the current axes
    ax.cla()                        # Clear the current axes# Get the current axes

    x = data.Date                   # Data to be used

    if index == 1:
        y = data.Score
        plt.title("Score", fontsize=16)
        ax.set_ylabel("Score", fontsize=14)
        plt.yticks(np.arange(0, 21, step=2))  # Set label locations.
        ax.set_ylim(0, 21)
        ax.set_xlabel("Date", fontsize=14)
        plt.xticks(rotation=30)
    else:
        y=data.Time
        ax.set_title("Time", fontsize=16)
        ax.set_ylabel("Time (Secs)", fontsize=14)
        ax.set_ylim(0, 180)
        plt.xticks(rotation=30)
        plt.axhline(y=goal, color='g', linestyle='-')
        plt.axhspan(0, goal, color="g", alpha=.25)
    ax.set_xlabel("Date")
    ax.grid()
    plt.scatter(x, y)                  # Plot y versus x as lines and/or markers
    fig.canvas.draw()               # Rendor figure into canvas

# Use Tkinter Agg
use_agg('TkAgg')

layout = [[sg.Graph((640, 480), (0, 0), (640, 480), key='Graph1'), sg.Graph((640, 480), (0, 0), (640, 480), key='Graph2')]]
window = sg.Window('Matplotlib', layout, finalize=True)


df = pd.read_csv("data.csv")
df = df[df['Level'] == C.add_difficulties[0]]
data = df[(df['Name'] == "Wyatte") & (df['Type'] == C.problem_types[0]) & (df['Level'] == C.add_difficulties[0])]
data.loc[:, "Date"] = pd.to_datetime(df['Date'], format="%m/%d/%y %H:%M:%S")
data = data.sort_values(by="Date", ascending=True, ignore_index=True)

df1 = pd.read_csv("data.csv")
df1 = df1[df1['Level'] == C.add_difficulties[1]]
data1 = df1[(df1['Name'] == "Wyatte") & (df1['Type'] == C.problem_types[0]) & (df1['Level'] == C.add_difficulties[1])]
data1.loc[:, "Date"] = pd.to_datetime(df1['Date'], format="%m/%d/%y %H:%M:%S")
data1 = data1.sort_values(by="Date", ascending=True, ignore_index=True)

goal = C.get_goal(C.add_difficulties[0])

# Initial
graph1 = window['Graph1']
graph2 = window['Graph2']
# plt.ioff()                          # Turn the interactive mode off
fig1 = plt.figure(1)                # Create a new figure
ax1 = plt.subplot(111)              # Add a subplot to the current figure.
fig2 = plt.figure(2)                # Create a new figure
ax2 = plt.subplot(111)              # Add a subplot to the current figure.
pack_figure(graph1, fig1)           # Pack figure under graph
pack_figure(graph2, fig2)
plot_figure(1, data, goal)
plot_figure(2, data, goal)

while True:

    event, values = window.read(timeout=5000)

    if event == sg.WINDOW_CLOSED:
        break
    elif event == sg.TIMEOUT_EVENT:
        print("Change")
        goal1 = C.get_goal(C.add_difficulties[1])
        plot_figure(1, data1, goal1)

        plot_figure(2, data1, goal1)

window.close()

