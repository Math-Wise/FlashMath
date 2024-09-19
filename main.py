import Constants as C
from LoginMenu import Login_Menu
from LevelSelectionMenu import Level_Selection_Menu
from ASMD_Questions import Question_Menu
from Frac_Questions0 import Frac_Quiz0
from Frac_Question1 import Frac_Quiz1
from ReportMenu import Report_Menu

#Opens login menu and records who logs in
login = Login_Menu()
name = login.username

type = C.problem_types[0]
level = C.add_difficulties[0]

while True:
    #Type and level selection
    selection = Level_Selection_Menu(name, type, level)
    type = selection.type
    level = selection.level

    #Quiz
    if selection.event == "Report":
        report = Report_Menu(name)
    elif level == C.frac_difficulties[0]:
        quiz = Frac_Quiz0(name, type, level)
    elif type == C.problem_types[3]:
        quiz = Frac_Quiz1(name, type, level)
    else:
        quiz = Question_Menu(name, type, level)