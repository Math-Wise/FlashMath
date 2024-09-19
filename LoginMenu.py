import pandas as pd
import PySimpleGUI as sg

class Login_Menu:
    def __init__(self, FONT = "Arial 16", THEME = "light blue 3"):
        #Sets Theme
        sg.theme(THEME)
        sg.set_options(font= FONT)

        #Object Variables
        self.username: str
        self.password: str
        self.df = pd.read_csv("users.csv")

        #Main Layout
        layout = [
            [sg.Push(), sg.Text("Flash Math", font="Arial 64 bold", text_color="dark red"), sg.Push()],
            [sg.Text("Username:"), sg.Input(key="-user-", focus=True), sg.Button("Login", size=5, bind_return_key=True)],
            [sg.Text("Password:"), sg.Input(key="-password-"), sg.Button("Exit", size=5)],
            [sg.Push(), sg.Text("Create Account", enable_events=True, font=FONT+" underline", pad=(40,0)), sg.Text("Forgot Password", enable_events=True, font=FONT+" underline", pad=(40,0)), sg.Push()]
        ]

        #Open Main Window
        window = sg.Window("Flash Math: Login", layout, margins=(75, 50))

        #Main Loop
        while True:
            event, values = window.read()

            #Login Attempt
            if event == "Login":
                self.username = values['-user-']
                self.password = values['-password-']

                try:
                    index = self.df.index[self.df['Username'] == self.username][0]
                except:
                    index=None

                if self.username not in self.df["Username"].values:
                    self.user_not_found()
                elif self.df['Password'][index] != self.password:
                    self.wrong_password()
                else:
                    window.close()
                    break
            #Create an Account
            elif event == "Create Account":
                self.create_user()
            #Forgot Password
            elif event == "Forgot Password":
                self.forgot_password()
            #Close
            elif event == "Exit":
                window.close()
                exit("Closed")
            elif event == sg.WIN_CLOSED:
                break

    def create_user(self):
        """
        Runs GUI for creating an account.
        Adds Username and password to users.cvs
        """
        layout = [
            [sg.Push(), sg.Text("Create an Account"), sg.Push()],
            [sg.Text("New Username:", size =17), sg.Input(key="-user-")],
            [sg.Text("New Password:", size =17), sg.Input(key="-password-")],
            [sg.Text("Confirm Password:", size =17), sg.Input(key="-password_match-")],
            [sg.Push(), sg.Button("Create", pad=(50,0)), sg.Button("Exit", pad=(50,0)), sg.Push()]
        ]

        # Open Window
        window = sg.Window("Flash Math: Login", layout, margins=(75, 50))

        # Main Loop
        while True:
            event, values = window.read()
            #Attempt to create an accout
            if event == "Create":
                if values['-user-'] in self.df["Username"].values:
                    self.username_taken()
                elif values['-password-'] != values['-password_match-']:
                    self.passwords_error()
                else:
                    new_entry = [values['-user-'], values['-password-'],
                                    False, False, False, False, False, False,
                                    False, False, False, False,
                                    False, False, False,
                                    False, False, False, False
                                ]
                    self.df.loc[self.df.shape[0]] = new_entry
                    self.df.to_csv("users.csv", index=False)
                    self.user_added()
                    window.close()
                    break
            #Exit
            elif event in ("Exit", sg.WIN_CLOSED):
                window.close()
                break

    def forgot_password(self):
        """Popup display for 'Forgot Password"""
        layout = [[sg.Text("This feature is not supported.\nEmail wyattehooper@gmail.com for assistance"), sg.Button("Exit")]]
        window = sg.Window("Flash Math: Forgot Password", layout)
        event, values = window.read()
        if event =="Exit":
            window.close()

    def user_added(self):
        """Popup display for successful user added"""
        layout = [
            [sg.Text("Account has been successfully made."), sg.Button("Exit")]]
        window = sg.Window("Flash Math: User Added", layout)
        event, values = window.read()
        if event == "Exit":
            window.close()

    def username_taken(self):
        """Popup display for username already taken"""
        layout = [
            [sg.Text("This username is taken. Please try another name."), sg.Button("Exit")]]
        window = sg.Window("Flash Math: Username Taken", layout)
        event, values = window.read()
        if event == "Exit":
            window.close()

    def passwords_error(self):
        """Popup display for passwords do not match in user creation"""
        layout = [
            [sg.Text("The passwords do not match."), sg.Button("Exit")]]
        window = sg.Window("Flash Math: Passwords Do Not Match", layout)
        event, values = window.read()
        if event == "Exit":
            window.close()

    def user_not_found(self):
        """Popup display for no username found during login"""
        layout = [
            [sg.Text("Username not found."), sg.Button("Exit")]]
        window = sg.Window("Flash Math: User Not Found", layout)
        event, values = window.read()
        if event == "Exit":
            window.close()

    def wrong_password(self):
        """Popup display for wrong password during login"""
        layout = [
            [sg.Text("Password did not match."), sg.Button("Exit")]]
        window = sg.Window("Flash Math: Wrong Password", layout)
        event, values = window.read()
        if event == "Exit":
            window.close()