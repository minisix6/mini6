
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from concurrent.futures import ThreadPoolExecutor as process
import time
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
# from kivymd.uix.stacklayout import MDStackLayout
# from kivymd.uix.gridlayout import MDGridLayout
# from kivy.core.window import Window
# from concurrent.futures import ThreadPoolExecutor as process
# from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFlatButton
# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.snackbar import BaseSnackbar, Snackbar
# from kivymd.uix.behaviors import RectangularElevationBehavior
# from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.behaviors.focus_behavior import FocusBehavior
# import re
# from kivy.animation import Animation
# from kivymd.uix.widget import MDWidget
# from kivy.properties import ObjectProperty, StringProperty, NumericProperty, DictProperty
# from kivymd.uix.scrollview import MDScrollView
# from screen_module import SubSm, Sm, LoginScreen, SignupScreen, AppsScreen, HomeScreen, LoadScreen, \
#     LogScreen, SettingScreen ,CalculatorScreen , OneLineList ,IconLeftWidget
from data_base import MedData
# from win32api import GetSystemMetrics

Window.size = (300 , 648)
kv = """

#: include theme.kv

Sm:
    id:sm
    LoadingScreen:
        name: 'loading_scr'
        MDFloatLayout:
            orientation:'vertical'
            MDFloatLayout:
                MDSpinner:
                    size_hint:(.3 , .3)
                    pos_hint:{'center_x':.5,'center_y':.5}
                    active:True
                MDLabel:
                    text:'loading'
                    size_hint:(.2,.2)
                    pos_hint:{'center_x':.52,'center_y':.5}
                    theme_text_color:'Custom'
                    text_color:app.theme_cls.primary_color
            MDFloatLayout:
                id : layout
                MDLabel:
                    id: exception
                    text:''
                    pos_hint:{'center_x':.5,'center_y':.2}
                    theme_text_color:'Error'
            MDFlatButton:
                pos_hint:{'x':.1 , 'center_y':.25}
                text:"test"
                on_press:app.go_to_screen('log_scr')
"""

class Sm(ScreenManager):
    pass

class LoadingScreen(Screen):
    def loading_screen(self):
        # self.get_root_size()
        self.root.current = 'loading_scr'
        print('before' , self.root.screen_names)
        for scr in self.root.screen_names:
            if scr != 'loading_scr':
                self.root.remove_widget(self.root.get_screen(scr))
        print('after' , self.root.screen_names)
    #     process1 = process()
    #     process1.submit(self.try_load)
    #
    # def try_load(self):
    #     return_screen = None
    #     try:
    #         return_screen = self.load_primary_data()
    #         if return_screen == 'error':
    #             raise Exception
    #     except Exception:
    #         print('eccept')
    #         # self.root.get_screen('loading_scr').ids.exception.text = self.primary_data['error']
    #         # self.root.get_screen('loading_scr').ids.exception.halign = 'center'
    #         # self.root.get_screen('loading_scr').ids.layout.add_widget(
    #         #     MDTextButton(text='exit', on_press=self.stop, theme_text_color='Custom',
    #         #                  text_color=self.theme_cls.primary_color,
    #         #                  pos_hint={
    #         #                      'center_x': .5, 'center_y': .1
    #         #                  }))
    #     else:
    #         self.go_to_screen(return_screen)
    #     finally:
    #         print(return_screen)




class MedFunc(MedData, LoadingScreen,):

    def __init__(self, **kwargs):
        super(MedFunc, self).__init__(**kwargs)
        self.snackbar = None
        self.more = ''
        self.dialog = None

    def get_root_size(self):

        self.size = (300, 500)
        # Window.size = (GetSystemMetrics(0) , GetSystemMetrics(1))
        Window.size = (300 , 648)
    def callback(self, *args):
        print(args)

    def go_to_screen(self, scr):
        screen_list = [
            'loading_scr','load_scr', 'log_scr', 'login_scr','signup_scr', 'home_s', 'apps_s','setting_s','calculator_s'
        ]
        try:
            if scr not in screen_list:
                raise KeyError
        except KeyError:
            self.notification(f'{scr}screen not exist')
        else:
            i = scr.index('_')
            screen = scr[:i]
            eval(f'self.{screen}_screen()')

    def show_dialog(self, title=None, dialog_text=None, args=None):
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text=dialog_text,
                opacity=.8,
                pos_hint={'center_x': .5, 'center_y': .5},
                buttons=args
            )
        self.dialog.open()

    def close_dialog(self, touch):
        # print(touch)
        self.dialog.dismiss()
        self.dialog = None

    def clean_str(self, var_str):
        return re.sub(r'\W+|^(?=\d)', '_', var_str)

    def go_app(self, args):
        print(type(args))
        if type(args) is str:
            print(args, 'go app func')
        else:
            print(args.text)

    def notification(self, args):
        if not self.snackbar:
            self.snackbar = CustomSnackbar(
                text=args,
                icon="information",
                snackbar_x="2dp",
                snackbar_y="2dp",
                buttons=[MDFlatButton(text="More", on_press=self.more_func)]
            )
            self.snackbar.size_hint_x = 1
            self.more = args
            self.snackbar.open()
        self.snackbar = None

    def more_func(self, arge):
        self.show_dialog(title='more',
                         dialog_text=self.more,
                         args=[MDFlatButton(text='Exit', on_press=self.close_dialog)])

    def change_theme(self, theme):
        if theme == 'Light':
            self.theme_cls.primary_palette = "Cyan"
            self.theme_cls.accent_palette = "Blue"
            self.theme_cls.theme_style = "Light"
        elif theme == 'Dark':
            self.theme_cls.primary_palette = "Teal"
            self.theme_cls.accent_palette = "Red"
            self.theme_cls.theme_style = "Dark"

    def save_setting(self):
        self.loading_screen()

class MedApp(MedFunc):

    def __init__(self, **kwargs):
        super(MedApp, self).__init__(**kwargs)

    def build(self):
        return Builder.load_string(kv)

    def on_start(self):
        self.loading_screen()

    def test(self, *args):
        print('test')


if __name__ == '__main__':
    app = MedApp()
    app.run()