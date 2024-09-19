import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Constants as C
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


class Report_Menu:
    def __init__(self, Name, FONT = "Arial 16", THEME = "light blue 3"):
        #settings
        sg.set_options(font=FONT)
        sg.theme(THEME)
        br = 0

        #Data for Objectives
        user_df = pd.read_csv("users.csv")
        user_df = user_df[(user_df['Username'] == Name)]
        user_df = user_df.reset_index()

        #Adding Scores
        if user_df.add0[0] == True:
            add0 = '✔'
        else:
            add0 = 'X'
        if user_df.add1[0] == True:
            add1 = '✔'
        else:
            add1 = 'X'
        if user_df.add2[0] == True:
            add2 = '✔'
        else:
            add2 = 'X'
        if user_df.add3[0] == True:
            add3 = '✔'
        else:
            add3 = 'X'
        if user_df.add4[0] == True:
            add4 = '✔'
        else:
            add4 = 'X'
        if user_df.add5[0] == True:
            add5 = '✔'
        else:
            add5 = 'X'
        #Mult Scores
        if user_df.mult0[0] == True:
            mult0 = '✔'
        else:
            mult0 = 'X'
        if user_df.mult1[0] == True:
            mult1 = '✔'
        else:
            mult1 = 'X'
        if user_df.mult2[0] == True:
            mult2 = '✔'
        else:
            mult2 = 'X'
        if user_df.mult3[0] == True:
            mult3 = '✔'
        else:
            mult3 = 'X'
        #Div Scores
        if user_df.div0[0] == True:
            div0 = '✔'
        else:
            div0 = 'X'
        if user_df.div1[0] == True:
            div1 = '✔'
        else:
            div1 = 'X'
        if user_df.div2[0] == True:
            div2 = '✔'
        else:
            div2 = 'X'
        #Frac Score
        if user_df.frac0[0] == True:
            frac0 = '✔'
        else:
            frac0 = 'X'
        if user_df.frac1[0] == True:
            frac1 = '✔'
        else:
            frac1 = 'X'
        if user_df.frac2[0] == True:
            frac2 = '✔'
        else:
            frac2 = 'X'
        if user_df.frac3[0] == True:
            frac3 = '✔'
        else:
            frac3 = 'X'


        #Objective Layout Objects
        add = sg.Text(f"Add/Sub   K: {add0}    1st: {add1}   2nd: {add2} 3rd: {add3}  4th: {add4}  5th: {add5}", size=(45), font="Arial 24")
        mult = sg.Text(f"Mult       3rd: {mult0}   x25: {mult1}    4th: {mult2}  5th: {mult3}", size=(45), font="Arial 24")
        div = sg.Txt(f"Div         3rd: {div0}   4th: {div1}    5th: {div2}", size=(45), font="Arial 24")
        frac = sg.Text(f"Frac       3rd: {frac0}  Add: {frac1}  Mult: {frac2}  Div: {frac3}", size=(45), font="Arial 24")
        dif_object = sg.OptionMenu(C.add_difficulties, default_value= C.add_difficulties[0], key="-level-", pad=((0, 0), (20, 0)), enable_events=True)
        score = sg.Text("Score  Best:     Mean:      Community Mean:", font="arial 20")
        time =  sg.Text("Time  Best:     Mean:      Community Mean:", font="arial 20")
        #Graph Layout Objects
        score_plot_canvas = sg.Graph((640, 480), (0, 0), (640, 480), key='Graph1')
        time_plot_canvas = sg.Graph((640, 480), (0, 0), (640, 480), key='Graph2')

        layout = [
            [sg.Push(), sg.Text(f"{Name}'s Report", font="Arial 38", pad=(0, (33, 0)), text_color="dark red"), sg.Push()],
            [sg.HLine(pad=(0, (0,25)))],
            [sg.Push(), add, sg.Push()],
            [sg.Push(), mult, sg.Push()],
            [sg.Push(), div, sg.Push()],
            [sg.Push(), frac, sg.Push()],
            [sg.HLine()],
            [sg.Push(), sg.Text('Question Type: ', pad=((0,0), (20,0))), sg.OptionMenu(C.problem_types, key = "-type-", default_value=C.problem_types[0], pad=((0, 75), (20,0)), enable_events=True), sg.Text("Question Difficulty: ", pad=((75, 0), (20,0))), dif_object, sg.Push()],
            [sg.Push(), score, sg.Push()],
            [sg.Push(), time, sg.Push()],
            [sg.Push(), score_plot_canvas, time_plot_canvas, sg.Push()],
            [sg.Push(), sg.Button("Back", size=(10,2), pad=(50,30)), sg.Push()]
        ]

        #Open Window
        window = sg.Window("Flash Math: Questions", layout, finalize=True)
        window.maximize()

        #Data for Graph
        df = pd.read_csv("data.csv")
        df = df[df['Level'] == C.add_difficulties[0]]
        data = df[(df['Name'] == Name) & (df['Type'] == C.problem_types[0]) & (df['Level'] == C.add_difficulties[0])]
        data.loc[:, "Date"] = pd.to_datetime(df['Date'], format="%m/%d/%y %H:%M:%S")
        data = data.sort_values(by="Date", ascending=True, ignore_index=True)
        goal = C.get_goal(C.add_difficulties[0])

        #Initial Graph
        graph1 = window['Graph1']
        graph2 = window['Graph2']
        fig1 = plt.figure(1)                # Create a new figure
        ax1 = plt.subplot(111)              # Add a subplot to the current figure.
        fig2 = plt.figure(2)                # Create a new figure
        ax2 = plt.subplot(111)              # Add a subplot to the current figure.
        self.pack_figure(graph1, fig1)           # Pack figure under graph
        self.pack_figure(graph2, fig2)
        self.plot_figure(1, data, goal, 20)
        self.plot_figure(2, data, goal, 20)

        #Loop Variables
        first = True

        while True:
            if first == True: #Runs in first pass only
                #Sets variables
                qtype = C.problem_types[0]
                goal = C.get_goal(C.add_difficulties[0])
                level = C.add_difficulties[0]
                score_limit = C.get_question_limit(C.add_difficulties[0])
                first = False
            else: #Pass 2+
                event, values = window.read()

                #Main Event Loop
                if event in ["Back", sg.WIN_CLOSED]:
                    window.close()
                    break
                #Changes the difficulty menu
                elif event == "-type-":
                    if values["-type-"] == C.problem_types[0]:
                        dif_object.update(values=C.add_difficulties, value=C.add_difficulties[0])
                        values["-level-"] = C.add_difficulties[0]
                    if values["-type-"] == C.problem_types[1]:
                        dif_object.update(values=C.mult_difficulties, value=C.mult_difficulties[0])
                        values["-level-"] = C.mult_difficulties[0]
                    elif values["-type-"] == C.problem_types[2]:
                        dif_object.update(values=C.div_difficulties, value=C.div_difficulties[0])
                        values["-level-"] = C.div_difficulties[0]
                    elif values["-type-"] == C.problem_types[3]:
                        dif_object.update(values=C.frac_difficulties, value=C.frac_difficulties[0])
                        values["-level-"] = C.frac_difficulties[0]
                    print(event)

                #Sets variables
                qtype = values["-type-"]
                level = values["-level-"]
                goal = C.get_goal(level)
                score_limit = C.get_question_limit(level)

            #Data for graph
            df = pd.read_csv("data.csv")
            df = df[df['Level'] == level]
            data = df[(df['Name'] == Name) & (df['Type'] == qtype) & (df['Level'] == level)]
            data.loc[:, "Date"] = pd.to_datetime(df['Date'], format="%m/%d/%y %H:%M:%S")
            data = data.sort_values(by="Date", ascending=True, ignore_index=True)

            # Limited data to past 20 entries for means
            count = data.shape[0]
            if count < 20:
                data_limited = data
            else:
                data_limited = data.loc[:19]

            # User Statistics
            avg_dur = round(data_limited.Time.mean(), 1) #Only looks at last 20 entries
            avg_score = round(data_limited.Score.mean(), 1) #Only looks at last 20 entries
            max_score = data.Score.max()
            min_time = data.Time.min()

            #Community Statistics
            comm_dur = round(df.Time.mean(),1)
            comm_score = round(df.Score.mean(),1)

            #Updates statistics into layout for current level
            time.update(f"Time:     Best: {min_time}     Mean: {avg_dur}     Community Mean: {comm_dur}")
            score.update(f"Score:    Best: {max_score}     Mean: {avg_score}     Community Mean: {comm_score}")

            #Draws plots
            self.plot_figure(1, data, goal, score_limit)
            self.plot_figure(2, data, goal, score_limit)
            window.refresh()


    def pack_figure(self, graph, figure):
        canvas = FigureCanvasTkAgg(figure, graph.Widget)
        plot_widget = canvas.get_tk_widget()
        plot_widget.pack(side='top', fill='both', expand=1)
        return plot_widget


    def plot_figure(self, index, data, goal, score_limit=20):
        fig = plt.figure(index)  # Active an existing figure
        ax = plt.gca()  # Get the current axes
        ax.cla()  # Clear the current axes# Get the current axes

        x = data.Date  # Data to be used

        if index == 1:
            y = data.Score
            plt.title("Score", fontsize=16)
            ax.set_ylabel("Score", fontsize=14)
            plt.yticks(np.arange(0, score_limit + 1, step=2))  # Set label locations.
            ax.set_ylim(0, score_limit + 1)
            ax.set_xlabel("Date", fontsize=14)
            plt.xticks(rotation=30)
        else:
            y = data.Time
            ax.set_title("Time", fontsize=16)
            ax.set_ylabel("Time (Secs)", fontsize=14)
            ax.set_ylim(0, 180)
            plt.xticks(rotation=30)
            plt.axhline(y=goal, color='g', linestyle='-')
            plt.axhspan(0, goal, color="g", alpha=.25)
        ax.set_xlabel("Date")
        ax.grid()
        plt.scatter(x, y)  # Plot y versus x as lines and/or markers
        fig.canvas.draw()  # Rendor figure into canvas



