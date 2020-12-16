from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from datetime import datetime
import json,glob
from pathlib import Path
import random


Builder.load_file("design.kv")

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current="sign_up_screen" 
    def login(self,uname,pwrd):
        with open("users.json") as file:
            users=json.load(file)

        if uname in users and users[uname]['password']==pwrd:
            self.manager.current="login_screen_success"
        else:
            self.ids.login_wrong.text='wrong username or password'

    def forgot_password(self):
        self.manager.current="forgot_password_screen"


class ForgotPasswordScreen(Screen):
    def backtologin(self):
        self.manager.current="login_screen"           

          

class SignUpScreen(Screen):
    def add_user(self,usn,pasw):
       with open("users.json") as file:
           users=json.load(file)

       users[usn]={"username":usn , "password":pasw , "date created":datetime.now().strftime("%Y-%M-%d %H-%M-%S")}   
       with open("users.json","w") as file:
           json.dump(users,file)
       self.manager.current="sign_up_screen_success"
       print(users)    

class SignUpScreenSuccess(Screen):
    def gotologin(self):
        self.manager.current='login_screen'
        self.manager.transition.direction='right'
class LoginScreenSuccess(Screen):
    def logout(self):
        self.manager.transition.direction='right'
        self.manager.current='login_screen'

    def get_quote(self,feel):
        feel=feel.lower()
        avaliable_feelings=glob.glob('quotes/*txt')
        
        avaliable_feelings=[Path(filename).stem for filename in avaliable_feelings ]
        if feel in avaliable_feelings:
            with open(f"quotes/{feel}.txt",encoding="utf8") as file:
                quote=file.readlines()
                self.ids.quote.text=random.choice(quote)
        else:
            self.ids.quote.text="even we can't understand how u feel....try another feeling"      

class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass
class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()
