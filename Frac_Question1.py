import Constants as C
import PySimpleGUI as sg

import time
import datetime as dt
import os
import pandas as pd


class Frac_Quiz1:
    def __init__(self, NAME, TYPE, LEVEL, FONT = "Arial 16", THEME = "light blue 3"):
        #Shared and Saved Variables
        self.user = NAME
        self.type = TYPE
        self.level = LEVEL
        self.score = 0
        self.time: int
        self.answer: int

        question_limit = C.get_question_limit(self.level)

        # settings
        sg.set_options(font=FONT)
        sg.theme(THEME)
        br = 0


        #Variable Layout objects
        self.Question_Canvas = sg.Canvas(background_color='light grey', size=(600, 400))
        self.Input_a = sg.Input(font="Arial 48 bold", size=(5, 1), background_color="lightgrey", pad=0, focus=True,
                              do_not_clear=False, justification='center', key="-num-")
        self.Input_b = sg.Input(font="Arial 48 bold", size=(5, 1), background_color="lightgrey", pad=0,
                              do_not_clear=False, justification='center', key="-dem-")

        layout = [
                [sg.Push(), sg.Text("Flash Math", font="Arial 64 bold", text_color="dark red", pad=(0, (100, 0))), sg.Push()],
                [sg.HLine(pad=(0, (0,50)))],
                [sg.Push(), self.Question_Canvas, sg.Push()],
                [sg.Push(), sg.Text("Numberator:", size=11), self.Input_a, sg.Push()],
                [sg.Push(), sg.Text("Denominator:", size = 11), self.Input_b, sg.Push()],
                [sg.Push(), sg.Button("Enter", bind_return_key=True, size = (10,2)), sg.Button("Back", size=(10,2)), sg.Push()]
        ]

        self.window = sg.Window("Flash Math: Questions", layout, finalize=True)
        self.window.maximize()

        # Loop Variables
        question_number = 0
        start_time = time.perf_counter()
        wronged = {"a": [], "symbol": [], "b": [], "answer": []}
        wrong = False
        accidental_hit = False
        passed = False


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


            tkc = self.Question_Canvas.TKCanvas

            if question_number > question_limit:
                tkc.create_text(150,35, text=f"Correction {question_number-question_limit}", font= "Arial 32 underline")
            else:
                tkc.create_text(150, 35, text=f"Question {question_number}", font="Arial 32 underline")

            fig = [
                tkc.create_text(225, 165, text=a.numerator, font='Arial 48 underline bold'),
                tkc.create_text(225, 235, text =a.denominator, font='Arial 48 bold'),
                tkc.create_text(300, 200, text=symbol, font=('Arial Bold', 48)),
                tkc.create_text(375, 165, text=b.numerator, font='Arial 48 underline bold'),
                tkc.create_text(375, 235, text=b.denominator, font="Arial 48 bold"),
                tkc.create_text(450, 200, text="=", font="Arial 48 bold")
            ]

            wrong = False
            accidental_hit = False


            event, values = self.window.read()

            if event in ["Back", sg.WIN_CLOSED]:
                br = 1
                self.window.close()
                break

            # Catches accidental enters or letters in input
            try:
                float(values["-num-"])
                float(values["-dem-"])
            except:
                accidental_hit = True
                continue


            if event == "Enter":
                if (int(values['-num-']) == self.answer.numerator) and (int(values['-dem-']) == self.answer.denominator):
                    if question_number <= question_limit:
                        self.score += 1
                    self.correct_feedback()
                else:
                    self.wrong_feedback()
                    wrong = True
                    self.score -= 1
                    wronged["a"]= wronged["a"] + [a]
                    wronged["b"]= wronged["b"] + [b]
                    wronged["symbol"] = wronged["symbol"] + [symbol]
                    wronged["answer"]= wronged["answer"] + [self.answer]

        # Close Window Actions
        if br == 0:
            stop_time = time.perf_counter()
            self.time = round(stop_time - start_time)
            goal = C.get_goal(self.level)
            if (self.score == question_limit) and self.time <= goal:
                C.update_user(self.user, self.type, self.level)
                passed = True
            self.save(self.user, self.type, self.level, self.score, self.time)
            self.score_menu(goal, passed, question_limit)
            self.window.close()




    def correct_feedback(self):
        """Gives feedback for a correct answer"""
        self.Question_Canvas.update(background_color="lightgreen")
        self.Input_a.set_focus()
        self.window.refresh()
        time.sleep(0.25)
        self.Question_Canvas.update(background_color="lightgrey")

        self.Question_Canvas.tk_canvas.delete("all")
        self.window.refresh()

    def wrong_feedback(self):
        """Gives feedback for a wrong answer"""
        self.Question_Canvas.update(background_color="red")
        self.Input_a.set_focus()
        self.Input_a.update(value=self.answer.numerator, readonly=True)
        self.Input_b.update(value=self.answer.denominator, readonly=True)
        self.window.refresh()
        time.sleep(2)
        self.Input_a.update(value="", readonly=False)
        self.Input_b.update(value="", readonly=False)
        self.Question_Canvas.update(background_color="lightgrey")

        self.window.refresh()

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
            [sg.Text(f"Name: {self.user}", background_color='lightgrey', pad=0, size=(35, 1))],
            [sg.Text(f"Type: {self.type}", background_color='lightgrey', pad=0, size=(35, 1))],
            [sg.Text(f"Level: {self.level}", background_color='lightgrey', pad=0, size=(35, 1))],
            [sg.Text(f"Score: {self.score}", background_color='lightgrey', pad=0, size=(35, 1))],
            [sg.Text(f"Goal Time: {goal}", background_color='lightgrey', pad=0, size=(35, 1))],
            [sg.Text(f"Time: {self.time}", background_color='lightgrey', pad=0, size=(35, 1))],
            [sg.Push(), sg.Button("Exit"), sg.Push()]
        ]

        #Open Window
        window = sg.Window("Flash Math: Score", layout)
        event, values = window.read()

        #Event loop
        if event in [sg.WIN_CLOSED, "Exit"]:
            window.close()

