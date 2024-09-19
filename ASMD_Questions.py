#Self Created Files
import Constants as C

#GUI Imports
import tkinter
import PySimpleGUI as sg

#Function Imports
import math
import time
import os
import pandas as pd
import datetime as dt


class Question_Menu():
    def __init__(self, NAME, TYPE, LEVEL, FONT = "Arial 16", THEME = "light blue 3"):
        #Shared and Saved Variables
        self.user = NAME
        self.type = TYPE
        self.level = LEVEL
        self.score = 0
        self.time: int
        self.answer: int

        question_limit = C.get_question_limit(self.level)

        #settings
        sg.set_options(font=FONT)
        sg.theme(THEME)
        br = 0

        #Variable Layout objects
        self.Question_Canvas = sg.Canvas(size= (600, 400), background_color="lightgrey")
        self.Input = sg.Input(font="Arial 48 bold", size=(5,1), background_color="lightgrey", pad=0, focus=True, do_not_clear=False, justification='right', key="-answer-")


        layout = [
            [sg.Push(), sg.Text("Flash Math", font="Arial 64 bold", text_color="dark red", pad=(0, (100, 0))), sg.Push()],
            [sg.HLine(pad=(0, (0,50)))],
            [sg.Push(), self.Question_Canvas, sg.Push()],
            [sg.Push(), self.Input, sg.Push()],
            [sg.Push(), sg.Button("Enter", bind_return_key=True, size=(10,2), pad=(50, 30)), sg.Button("Back", size=(10,2), pad=(50,30)), sg.Push()]
        ]

        #Open Window
        self.window = sg.Window("Flash Math: Questions", layout, finalize=True)
        self.window.maximize()


        #Loop Variables
        question_number = 0
        start_time = time.perf_counter()
        wronged = {"a": [], "symbol": [], "b": [], "answer": []}
        wrong = False
        accidental_hit = False
        passed = False


        #Main Loop
        while True:
            if (wrong == False) and (accidental_hit == False):
                if question_number < question_limit:
                    a, symbol, b, self.answer = C.get_problem(self.type, self.level)
                    question_number += 1
                elif question_number >= question_limit:
                    try:
                        a = wronged["a"][question_number - question_limit]
                        b = wronged["b"][question_number - question_limit]
                        symbol = wronged["symbol"][question_number - question_limit]
                        self.answer = wronged["answer"][question_number - question_limit]
                        question_number += 1
                    except:
                        break


                #Draw on Canvas
                tkc = self.Question_Canvas.TKCanvas

                #Question number
                if question_number > question_limit:
                    tkc.create_text(150,35, text=f"Correction {question_number-question_limit}", font= "Arial 32 underline")
                else:
                    tkc.create_text(150, 35, text=f"Question {question_number}", font="Arial 32 underline")
                if self.level in [C.add_difficulties[5], C.mult_difficulties[3]]:
                    width = math.ceil(math.log(max([a, b]), 10) + 1) * 30 + 110
                    fig = [
                        tkc.create_text(300, 200, text=f"{a:.2f}\n{symbol} {b:.2f}", font=('Arial Bold', 48),
                                        justify=tkinter.RIGHT),  # a
                        tkc.create_line(300 - width / 2, 275, 300 + width / 2, 275, width=8)
                    ]
                elif self.type in C.problem_types[0:2]:
                    width = math.ceil(math.log(max([a, b]), 10)+1)*30+60
                    fig = [
                        tkc.create_text(300, 200, text=f"{a}\n{symbol} {b}", font=('Arial Bold', 48), justify=tkinter.RIGHT),  # a
                        tkc.create_line(300-width/2, 275, 300+width/2, 275, width=8)
                    ]
                elif self.level == C.div_difficulties[0]:
                    fig = [
                        tkc.create_text(300, 200, text=f"{a} / {b} =", font =('Arial Bold', 48))
                    ]
                elif self.type == C.problem_types[2]:
                    length = math.ceil(math.log(a+.001, 10))*36+30
                    shift = math.ceil(math.log(b+.001, 10))*18+16
                    fig = [
                        tkc.create_line(300+shift-length/2, 168, 300+shift+length/2, 168, width=7),
                        tkc.create_line(303+shift-length/2, 168, 303+shift-length/2, 178, width=7),
                        tkc.create_text(300, 200, text=f"{b} ){a}", font=('Arial Bold', 48))
                    ]

            wrong = 0
            accidental_hit = False

            event, values = self.window.read()
            # Exit Event
            if event in ("Back", sg.WIN_CLOSED):
                self.window.close()
                br = 1
                break

            # Catches accidental enters or letters in input
            try:
                float(values["-answer-"])
            except:
                accidental_hit = True
                continue

            #Event Loop
            if event == "Enter":
                if float(values["-answer-"]) == self.answer:
                    if question_number <= question_limit:
                        self.score += 1
                    self.correct_feedback()
                else:
                    self.wrong_feedback()
                    wrong = 1
                    self.score -= 1
                    wronged["a"]= wronged["a"] + [a]
                    wronged["b"]= wronged["b"] + [b]
                    wronged["symbol"] = wronged["symbol"] + [symbol]
                    wronged["answer"]= wronged["answer"] + [self.answer]



        #Close Window Actions
        if br == 0:

            stop_time = time.perf_counter()
            self.time=round(stop_time-start_time)
            goal = C.get_goal(self.level)
            if (self.score == question_limit) and self.time <= goal:
                C.update_user(self.user, self.type, self.level)
                passed = True
            self.save(self.user, self.type, self.level, self.score, self.time)
            self.score_menu(goal, passed, question_limit)
            self.window.close()


    def save(self, name, type, level, score, time):
        """
        Saves data to data.csv
        :param name: The users username
        :param type: The question type
        :param level: The level of the questions
        :param score: The score from the questions
        :param time: The time it took to finish
        """
        new_data = [name, type, level, dt.datetime.now().strftime("%m/%d/%y %H:%M:%S"), score, time]

        #Checks to see if the file exists
        if not os.path.exists("data.csv"):
            data = {"Name": [], "Type": [], "Level": [], "Datetime": [], "Score": [], "Time": []}
            df = pd.DataFrame.from_dict(data)
            df.loc[0] = new_data
        else: #reads file into df
            df = pd.read_csv("data.csv")
            df.loc[df.shape[0]] = new_data

        #Saves df
        df.to_csv("data.csv", index=False)

    def score_menu(self, goal, passed, question_limit):
        """
        Displays stats at the end of quiz
        """
        if passed:
            text = f"Goal Achieved!"
            color = "green"
        else:
            text = f"You need a time under {goal} and a score of {question_limit}."
            color = "red"

        layout = [
            [sg.Push(), sg.Text("Flash Math", font="Arial 64 bold", text_color="dark red", pad=(0, (25, 0))),
             sg.Push()],
            [sg.HLine(pad=(0, (0, 25)))],
            [sg.Text(text, background_color=color, justification="center", pad=0, size=(35, 1))],
            [sg.Text(f"Name: {self.user}", background_color='lightgrey', pad=0, size = (35,1))],
            [sg.Text(f"Type: {self.type}", background_color='lightgrey', pad=0, size = (35,1))],
            [sg.Text(f"Level: {self.level}", background_color='lightgrey', pad=0, size = (35,1))],
            [sg.Text(f"Score: {self.score}", background_color='lightgrey', pad=0, size = (35,1))],
            [sg.Text(f"Goal Time: {goal}", background_color='lightgrey', pad=0, size=(35, 1))],
            [sg.Text(f"Time: {self.time}", background_color='lightgrey', pad=0, size = (35,1))],
            [sg.Push(), sg.Button("Exit"), sg.Push()]
        ]

        #Open Window
        window = sg.Window("Flash Math: Score", layout)
        event, values = window.read()

        #Event loop
        if event in [sg.WIN_CLOSED, "Exit"]:
            window.close()

    def correct_feedback(self):
        """Gives feedback for a correct answer"""
        self.Question_Canvas.update(background_color="lightgreen")
        self.Input.update(background_color="lightgreen")
        self.window.refresh()
        time.sleep(0.25)
        self.Question_Canvas.update(background_color="lightgrey")
        self.Input.update(background_color="lightgrey")
        self.Question_Canvas.tk_canvas.delete("all")
        self.window.refresh()

    def wrong_feedback(self):
        """Gives feedback for a wrong answer"""
        self.Question_Canvas.update(background_color="red")
        self.Input.update(value = self.answer, background_color="red", readonly=True)
        self.window.refresh()
        time.sleep(2)
        self.Question_Canvas.update(background_color="lightgrey")
        self.Input.update(value="", background_color="lightgrey", readonly= False)
        self.window.refresh()






