import Constants as C
import PySimpleGUI as sg
import fractions as frac



class Level_Selection_Menu():
    def __init__(self, USERNAME, default_type = C.problem_types[0], default_level = C.add_difficulties[0], FONT = "Arial 16", THEME = "light blue 3"):
        #Shared Variables
        self.level: str
        self.type: str
        self.event = "none"

        #Settings
        sg.set_options(font=FONT)
        sg.theme(THEME)

        if default_type == C.problem_types[0]:
            difficulties = C.add_difficulties
        elif default_type == C.problem_types[1]:
            difficulties = C.mult_difficulties
        elif default_type == C.problem_types[2]:
            difficulties = C.div_difficulties
        elif default_type == C.problem_types[3]:
            difficulties = C.frac_difficulties

        a, symbol, b, answer = C.get_problem(default_type, default_level)

        if default_level == C.frac_difficulties[0]:
            example = f"{a[0]}/{a[1]} = {b[0]}/{b[1]}: {answer}"
        elif default_type in C.problem_types[3]:
            example = f"{a.numerator}/{a.denominator} {symbol} {b.numerator}/{b.denominator} = {answer.numerator}/{answer.denominator}"
        else:
            example = f"{a}{symbol}{b}={answer}"

        #Variable Layout Objects
        dif_object = sg.OptionMenu(difficulties, default_value= default_level, key="-level-", pad=((0, 0), (20, 0)), enable_events=True)
        exampleText = sg.Text(example, key="-example-", font="Arial 32 bold", size=15, background_color="lightgrey", justification="center", border_width=10)

        layout = [
            [sg.Push(), sg.Text("Flash Math", font="Arial 64 bold", text_color="dark red"), sg.Push()],
            [sg.HLine()],
            [sg.Push(), sg.Text(f'Welcome {USERNAME}!', font="arial 32 bold"), sg.Push()],
            [sg.Push(), sg.Text('Select the question type and difficulty using the menu below. Click "Begin" to start answering questions.'), sg.Push()],
            [sg.Push(),sg.Text('Question Type: ', pad=((0,0), (20,0))), sg.OptionMenu(C.problem_types, key = "-type-", default_value=default_type, pad=((0, 75), (20,0)), enable_events=True), sg.Text("Question Difficulty: ", pad=((75, 0), (20,0))), dif_object, sg.Push()],
            [sg.Push(), sg.Text("Example Problem", font="Arial 24 bold", pad=30), sg.Push()],
            [sg.Push(), exampleText, sg.Button('Refresh'), sg.Push()],
            [sg.HLine()],
            [sg.Push(), sg.Button("Begin", size=(10,2), pad=(100, 50)), sg.Button("Report", size=(10,2), pad=(100, 50)), sg.Button("Exit", size=(10,2), pad=(100,50)), sg.Push()]
            ]

        window = sg.Window("Flash Math: Level Selection", layout, finalize=True, margins=(150,150))
        window.maximize()

        #Main Loop
        while True:
            event, values = window.read()
            print(event)
            self.level=values['-level-']
            self.type=values['-type-']

            if event == "Begin":
                window.close()
                break
            elif event == "Report":
                print("worked")
                self.event = "Report"
                window.close()
                break
            elif event == "Refresh":
                pass
            if event == "-type-":
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
                window.refresh()





            elif event in ("Exit", sg.WIN_CLOSED):
                window.close()
                exit("Closed")

            self.type = values['-type-']
            self.level = values['-level-']



            a, symbol, b, answer = C.get_problem(self.type, self.level)

            if self.level == C.frac_difficulties[0]:
                example = f"{a[0]}/{a[1]} = {b[0]}/{b[1]}: {answer}"
            elif self.type in C.problem_types[3]:
                example = f"{a.numerator}/{a.denominator} {symbol} {b.numerator}/{b.denominator} = {answer.numerator}/{answer.denominator}"
            else:
                example = f"{a}{symbol}{b}={answer}"

            exampleText.update(value=example)
            window.refresh()



