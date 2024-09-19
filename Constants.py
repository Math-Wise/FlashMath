import random as rand
import math
import fractions as frac
import pandas as pd
pd.set_option('display.max_columns', 500)

problem_types = ["Add/Sub", "Multiplying", "Dividing", "Fractions"]

add_difficulties = ["K (+/-10)", "1st (+/-20)", "2nd (+/-100)", "3rd (+1000)", "4th Grade (+10000)", "5th (+0.01)"]
mult_difficulties = ["3rd Grade (x12)", "Mental Challenge (x25)", "4th Grade (x100)", "5th (x0.01)"]
div_difficulties = ["3rd Grade (144/12)", "4th Grade(10000/10)", "5th Grade (10000/100)"]
frac_difficulties = ["3rd (Are equal)", "5th Adding", "5th Mult", "5th Division"]

limit_1 = [div_difficulties[2]]
limit_3 = mult_difficulties[2:]
limit_5 = [add_difficulties[4]]
limit_10 = add_difficulties[3:] + [mult_difficulties[1]] + [div_difficulties[1]] + frac_difficulties[1:]
limit_20 = add_difficulties[:3] + [mult_difficulties[0]] + [div_difficulties[0]] + [frac_difficulties[0]]

goal_45 = add_difficulties[0:2] + [mult_difficulties[0]] + [div_difficulties[0]]
goal_75 = add_difficulties[2:4] + [mult_difficulties[1]] + [div_difficulties[2]] + [frac_difficulties[0]]
goal_90 = mult_difficulties[2:] + [div_difficulties[1]] + frac_difficulties[1:]
goal_120 = add_difficulties[4:]

# alg_difficulties = ["Function Notation", "Function Operation", "Parent Functions", ]
# tri_difficulties = ["Radians", "Functions"]
# calc_difficulties = ["Limits", "Derivatives", "Integrals"]


def get_problem(type, level):
    """
    Takes type and level and return a problem
    :param type: Problem type from ~problem_types~
    :param level:  Difficulty level from ~_difficulties
    :return: a - first number in problem
    :return: symbol - opperation symbol
    :return: b - second number in problem
    :return: answer - answer for problem
    """

    options = ["add", "sub"]

    #Add/Sub Problems
    if type == problem_types[0]:
        #Sets max sum
        if level == add_difficulties[0]:
            max_sum = 10
        elif level == add_difficulties[1]:
            max_sum = 20
        elif level == add_difficulties[2] or level == add_difficulties[5]:
            max_sum = 100
        elif level == add_difficulties[3]:
            max_sum = 1000
        elif level == add_difficulties[4]:
            max_sum = 10000

        #Gets a, b, and answer
        if level == add_difficulties[5]: #decimal case
            answer = round(rand.uniform(1, max_sum), 2)
            a = round(rand.uniform(0, answer), 2)
            b = round(answer - a, 2)
        else: #integer case
            answer = rand.randint(1, max_sum)
            a = rand.randint(0, answer)
            b = answer - a

        # chooses addition or subtraction problem
        choice = rand.choice(options)
        if choice == "add":
            symbol = "+"
        elif choice == "sub":
            symbol = "-"
            temp = a
            a = answer
            answer = temp


    #Multiplicaion Problems
    elif type == problem_types[1]:
        symbol = "x"
        #Sets max factors
        if level == mult_difficulties[0] or level == mult_difficulties[3]:
            max_factor = 12
        elif level == mult_difficulties[1]:
            max_factor = 25
        elif level == mult_difficulties[2]:
            max_factor = 100

        #Decimal case
        if level == mult_difficulties[3]:
            a = round(rand.uniform(0, max_factor), 1)
            b = round(rand.uniform(0, max_factor), 1)
            answer = round(a*b, 4)
        #Interger case
        else:
            a = rand.randint(0, max_factor)
            b = rand.randint(0, max_factor)
            answer = a*b



    #Division Problems
    elif type == problem_types[2]:
        symbol = "/"
        if level == div_difficulties[0]:
            max_divisor = 12
            max_quotient = 12
        elif level == div_difficulties[1]:
            max_divisor = 10
            max_quotient = 999
        elif level == div_difficulties[2]:
            max_divisor = 99
            max_quotient = 999

        #gets a, b, and answer
        b = rand.randint(1, max_divisor)
        answer = rand.randint(0, max_quotient)
        a = b * answer


    #Fraction Problems
    elif type == problem_types[3]:
        #Is equal to
        if level == frac_difficulties[0]:
            symbol = "="
            frac_choices = ["equal", "not equal"]
            if rand.choice(frac_choices) == frac_choices[0]:
                while True:
                    a = [rand.randint(0, 12), rand.randint(1, 12)]
                    c = rand.randint(1, 12)
                    b = [num * c for num in a]
                    answer = "True"
                    if math.gcd(a[0], a[1]) == 1:
                        break
            else:
                answer = "False"
                while True:
                    a = [rand.randint(0, 12), rand.randint(1, 12)]
                    c = rand.randint(1, 12)
                    b = [rand.randint(0,12)*c, rand.randint(1, 12)*c]
                    if (b[0]/b[1] != a[0]/a[1]) and (math.gcd(a[0], a[1]) == 1):
                        break
        #Adding or subtraction
        if level == frac_difficulties[1]:
            a = frac.Fraction(rand.randint(0, 12), rand.randint(1, 12))
            b = frac.Fraction(rand.randint(0, 12), rand.randint(1, 12))

            choice = rand.choice(options)
            if choice == "add":
                symbol = "+"
                answer = a+b
            elif choice == "sub":
                symbol = "-"
                if a < b:
                    temp = b
                    b = a
                    a = temp
                answer = a-b
        #Multiplication
        if level == frac_difficulties[2]:
            symbol = "x"
            a = frac.Fraction(rand.randint(0, 12), rand.randint(1, 12))
            b = frac.Fraction(rand.randint(0, 12), rand.randint(1, 12))
            answer = a*b
        if level == frac_difficulties[3]:
            symbol = "÷"
            a = frac.Fraction(rand.randint(0, 12), rand.randint(1, 12))
            b = frac.Fraction(rand.randint(1, 12), rand.randint(1, 12))
            answer = a/b

    return a, symbol, b, answer

def get_goal(level):
    if level in goal_45:
        goal = 45
    elif level in goal_75:
        goal = 75
    elif level in goal_90:
        goal = 90
    elif level in goal_120:
        goal = 120

    return goal

def get_question_limit(level):
    if level in limit_1:
        question_limit = 1
    elif level in limit_3:
        question_limit = 3
    elif level in limit_5:
        question_limit = 5
    elif level in limit_10:
        question_limit = 10
    elif level in limit_20:
        question_limit = 20
    return question_limit

def str_to_list(string):
    string = "[False, False, False, False, False]"
    string = string.replace("[", "")
    string = string.replace("]", "")

    return string.split(", ")


def update_user(name, type, level):
    df = pd.read_csv("users.csv")


    if type == problem_types[0]:
        if level == add_difficulties[0]:
            df.loc[df.Username == name, "add0"] = True
        elif level == add_difficulties[1]:
            df.loc[df.Username == name, "add1"] = True
        elif level == add_difficulties[2]:
            df.loc[df.Username == name, "add2"] = True
        elif level == add_difficulties[3]:
            df.loc[df.Username == name, "add3"] = True
        elif level == add_difficulties[4]:
            df.loc[df.Username == name, "add4"] = True
        elif level == add_difficulties[5]:
            df.loc[df.Username == name, "add5"] = True
    elif type == problem_types[1]:
        if level == mult_difficulties[0]:
            df.loc[df.Username == name, "mult0"] = True
        elif level == mult_difficulties[1]:
            df.loc[df.Username == name, "mult1"] = True
        elif level == mult_difficulties[2]:
            df.loc[df.Username == name, "mult2"] = True
        elif level == mult_difficulties[3]:
            df.loc[df.Username == name, "mult3"] = True
    elif type == problem_types[2]:
        if level == div_difficulties[0]:
            df.loc[df.Username == name, "div0"] = True
        elif level == div_difficulties[1]:
            df.loc[df.Username == name, "div1"] = True
        elif level == div_difficulties[2]:
            df.loc[df.Username == name, "div2"] = True
    elif type == problem_types[3]:
        if level == frac_difficulties[0]:
            df.loc[df.Username == name, "frac0"] = True
        elif level == frac_difficulties[1]:
            df.loc[df.Username == name, "frac1"] = True
        elif level == frac_difficulties[2]:
            df.loc[df.Username == name, "frac2"] = True
        elif level == frac_difficulties[3]:
            df.loc[df.Username == name, "frac3"] = True


    df.to_csv("users.csv", index=False)

