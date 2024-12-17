import time
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import ScreenManager, Screen
# from kivymd.uix.transition import MDSlideTransition, MDSwapTransition, MDFadeSlideTransition
from kivymd.uix.screen import MDScreen, MDHeroTo
from kivymd.uix.button import MDTextButton
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.core.window import Window
from kivymd.theming import ThemeManager
from concurrent.futures import ThreadPoolExecutor as process
# from kivymd.uix.taptargetview import MDTapTargetView
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivy.core.text import Label
from kivymd.uix.snackbar import BaseSnackbar,Snackbar
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors.focus_behavior import FocusBehavior
from kivymd.uix.list import OneLineIconListItem, IconRightWidget, IconLeftWidget, OneLineAvatarIconListItem, \
    OneLineListItem
import re
from kivy.animation import Animation
from kivymd.uix.widget import MDWidget


from kivy.properties import ObjectProperty ,StringProperty ,NumericProperty , DictProperty
# from kivymd.uix.scrollview import MDScrollView
from kivy.core.text import LabelBase
from kivymd import fonts_path

class ApiReceive:
    api_user_allow = [
        # [{userName : name , pass:number , phone : mac  , Statue : demo or remaningtime , savePass : Num } ,  ... ]
        {'userName': 'hamzeh', 'pass': '13671736', 'mac': '12345', 'statue': 'signIn', 'savePass': 'saved',
         'logOut': 'n', 'access': 'access'},
        {'userName': 'ghazaleh', 'pass': '1234', 'mac': '1234', 'statue': 'signIn', 'savePass': 'saved', 'logOut': 'y',
         'access': 'deny'},
        {'userName': 'ghanbarpur', 'pass': '1234', 'mac': '123', 'statue': 'signIn', 'savePass': '', 'logOut': 'y',
         'access': 'access'},
        {'userName': '', 'pass': '', 'mac': '12', 'statue': 'log', 'savePass': '', 'logOut': 'n', 'access': ''},
    ]

    def primary_api_check(self, mac_con=None):
        dic_data = False
        data_return = {'screen': '', 'userName': '', 'pass': '', 'savePass': '', 'error': ''}
        for dic in self.api_user_allow:
            if dic['mac'] == mac_con:
                dic_data = dic
        if dic_data is False:
            # save man and save time
            data_return['screen'] = 'load'
        else:
            # save time
            data_return['screen'] = dic_data['statue']
            if dic_data['statue'] == 'signIn':
                data_return['screen'] = 'login'
                data_return['userName'] = dic_data['userName']
                data_return['pass'] = dic_data['pass']
                data_return['savePass'] = dic_data['savePass']
                if dic_data['logOut'] == 'n':
                    # if dic_data['access'] == 'deny':
                    #     data_return['screen'] = 'login_error'
                    #     data_return['error'] = 'an error check payment'
                    # else:
                    data_return['screen'] = 'home'
        return data_return

    def return_data_to_save(self, dic):
        if dic is True:
            self.api_user_allow.append(dic)


class SqlReceive:
    install = 'install'  # and 'reinstall' , 'None'
    pre_build_file = '../med_kivy.kv'
    colors = {
        "Teal": {"200": "#95cfcf", "500": "#00FFFF", "700": "#0a7d7d", 'A700': '#cf8ccf'},
        "Red": {"200": "#f3f76f", "500": "#f7ff0f", "700": "#d0d61a", "A700": "#d13d5a"},
        "Cyan": {"200": "#b968fc", "500": "#8030c2", "700": "#44106e", 'A700': '#2d0c47'},
        "Blue": {"200": "#f0a254", "500": "#c2782f", "700": "#874d13", "A700": "#d13d5a"},

        "Dark": {"StatusBar": "#54cc58", "AppBar": "#212626", "Background": "#2e3332",
                 "CardsDialogs": "#404f4f", "Button": "#2a10ad", "TextField": "#deac18"},
        "Light": {"StatusBar": "#f2fdff", "AppBar": "#c7d4d6", "Background": "#f5f5f5",
                  "CardsDialogs": "#c7f6ff", "FlatButtonDown": "#C25111", "MDTextField": "#252520"}
    }
    root_size = (300, 500)
    default_theme = {'material_style': 'M2', 'theme_style': 'Dark',
                     'accent_palette': 'Red', 'primary_palette': 'Teal',
                     'primary_light_hue': '200', 'primary_hue': '500',
                     'primary_dark_hue': '700', 'accent_light_hue': '200',
                     'accent_hue': '500', 'accent_dark_hue': '700'}
    sql_first_time = 0  # =>open the first screen => change to '0' in second time and open the second screen


class MedData(MDApp):
    mac_con = '12345'  # get mac adress and ip
    screen_loaded = {'loading_screen': None, 'load_screen': None, 'log_screen': None, 'setting_screen': None,
                     'home_screen': None, 'login_screen': None, 'signup_screen': None, 'add_screen': None,
                     'speed_dial': None}
    apps_assortment = {'Medical Terminology Dictionary': ['Medical Terminology Dictionary'],
                       'Scales': ['MORSE', 'BRADEN', 'BMI', 'Clearance', 'GCS', 'WELLS', 'ForeScore', 'NGASR'],
                       'Drugs': ['Iran Generic Pharmacy', 'Drug Interactions', 'Pharmaceutical Calculations'],
                       'Laboratory': ['ABG', 'CBC']}
    floating_data={'ABG': ['contain', "on_press", lambda x: self.go_app('ABG')],}
    app_fav = ['MORSE']

    def __init__(self, **kwargs):
        super(MedData, self).__init__(**kwargs)
        self.window_size = Window.size
        self.primary_data = {}
        self.api = ApiReceive()
        self.sql = SqlReceive()
        self.statue = ''
        self.default_theme = self.sql.default_theme
        self.colors = self.sql.colors
        self.add_tab_list = []
        self.add_widget_list = []
        self.float_action_button = object

    def load_primary_data(self):
        self.primary_data = self.check_con()
        self.theme_cls.material_style = self.default_theme['material_style']
        self.theme_cls.theme_style = self.default_theme['theme_style']
        self.theme_cls.primary_palette = self.default_theme['primary_palette']
        self.theme_cls.accent_palette = self.default_theme['accent_palette']
        self.theme_cls.primary_dark_hue = self.default_theme['primary_dark_hue']
        self.theme_cls.primary_hue = self.default_theme['primary_hue']
        self.theme_cls.primary_light_hue = self.default_theme['primary_light_hue']
        self.theme_cls.accent_dark_hue = self.default_theme['accent_dark_hue']
        self.theme_cls.accent_hue = self.default_theme['accent_hue']
        self.theme_cls.accent_light_hue = self.default_theme['accent_light_hue']
        time.sleep(1)
        return self.primary_data['screen']

    def check_con(self):
        dic = self.api.primary_api_check(mac_con=self.mac_con)
        # if error dic[screen] = error and [error] = exception
        # dic['screen']='error'
        # dic['error']='check connection and retry'
        return dic


class MedUser(MedData):

    def __init__(self, **kwargs):
        super(MedUser, self).__init__(**kwargs)
        self.dialog = None

    def log_in(self):
        user_name = self.root.get_screen('login_scr').ids.user_name_field.text
        password = self.root.get_screen('login_scr').ids.pass_field.text
        if user_name == self.primary_data['userName'] and bool(user_name) is True:
            if password == self.primary_data['pass'] and bool(password) is True:
                # print('check save pass')
                self.home_screen()
            else:
                self.show_dialog(title='incorrect password', dialog_text='incorrect password', args=[
                    MDFlatButton(text='close', theme_text_color='Custom', text_color=self.theme_cls.accent_color,
                                 on_press=self.close_dialog, size_hint=(.5, .5)),
                    MDFlatButton(text='forget password', theme_text_color='Custom',
                                 text_color=self.theme_cls.accent_color,
                                 on_press=self.forget_password, size_hint=(.5, .5))])
        else:
            self.show_dialog(title='invalid username', dialog_text='invalid username', args=[
                MDFlatButton(text='close', theme_text_color='Custom', text_color=self.theme_cls.accent_color,
                             on_press=self.close_dialog, size_hint=(.5, .5)),
                MDFlatButton(text='sign up', theme_text_color='Custom',
                             text_color=self.theme_cls.accent_color,
                             on_press=self.sign_up, size_hint=(.5, .5))])

    def forget_password(self, args):
        # print('forget_password function', touch)
        if self.dialog:
            self.dialog.dismiss()  # if to call func direct change thise line
        app.dialog = None

    def sign_up(self, touch):
        # print('sign_up function', touch)
        if self.dialog:
            self.dialog.dismiss()  # if to call func direct change thise line
        self.dialog = None


class Sm(MDScreenManager):
    def __init__(self, **kwargs):
        super(Sm, self).__init__(**kwargs)


class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)

    def loading_screen(self):
        self.get_root_size()
        if self.screen_loaded['loading_screen'] is None:
            scr1 = Builder.load_file('../screens/loading_screen.kv')
            self.root.add_widget(scr1)
            self.screen_loaded['loading_screen'] = scr1
        self.root.current = 'loading_scr'
        process1 = process()
        process1.submit(self.try_load)

    # noinspection PyBroadException
    def try_load(self):
        return_screen = None
        try:
            while return_screen is None:
                return_screen = self.load_primary_data()
                if return_screen == 'error':
                    raise Exception
        except Exception:
            self.root.get_screen('loading_scr').ids.exception.text = self.primary_data['error']
            self.root.get_screen('loading_scr').ids.exception.halign = 'center'
            self.root.get_screen('loading_scr').ids.layout.add_widget(
                MDTextButton(text='exit', on_press=self.stop, theme_text_color='Custom',
                             text_color=self.theme_cls.primary_color,
                             pos_hint={
                                 'center_x': .5, 'center_y': .1
                             }))
        else:
            self.go_to_screen(return_screen)
        finally:
            print(return_screen)

#
# class LoadScreen(Screen):
#     def __init__(self, **kwargs):
#         super(LoadScreen, self).__init__(**kwargs)
#
#     def load_screen(self):
#         if self.screen_loaded['load_screen'] is None:
#             scr1 = Builder.load_file('screens/load_screen.kv')
#             self.root.add_widget(scr1)
#             self.screen_loaded['load_screen'] = scr1
#         self.root.current = 'load_scr'
#
#
# class LogScreen(Screen):
#     def __init__(self, **kwargs):
#         super(LogScreen, self).__init__(**kwargs)
#
#     def log_screen(self):
#         if self.screen_loaded['log_screen'] is None:
#             scr2 = Builder.load_file('./screens/log_screen.kv')
#             self.root.add_widget(scr2)
#             self.screen_loaded['log_screen'] = scr2
#         self.root.current = 'log_scr'
#
#
# class LoginScreen(Screen):
#     def __init__(self, **kwargs):
#         super(LoginScreen, self).__init__(**kwargs)
#
#     def login_screen(self):
#         if self.screen_loaded['login_screen'] is None:
#             scr3 = Builder.load_file('screens/login_screen.kv')
#             self.root.add_widget(scr3)
#             self.screen_loaded['login_screen'] = scr3
#         self.root.current = 'login_scr'
#         if bool(self.primary_data['userName']) is True:
#             self.root.get_screen('login_scr').ids.user_name_field.text = self.primary_data['userName']
#             if bool(self.primary_data['savePass']) is True:
#                 self.root.get_screen('login_scr').ids.pass_field.text = self.primary_data['pass']
#
#
# class SignupScreen(Screen):
#     def __init__(self, **kwargs):
#         super(SignupScreen, self).__init__(**kwargs)
#
#     def signup_screen(self):
#         if self.screen_loaded['signup_screen'] is None:
#             scr3 = Builder.load_file('screens/sm.kv')
#             self.root.add_widget(scr3)
#             self.screen_loaded['signup_screen'] = scr3
#         self.root.current = 'signup_scr'
#


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def home_screen(self):
        if self.screen_loaded['speed_dial'] is None:
            pass
            # self.floating_drawer()
        if self.screen_loaded['home_screen'] is None:
            scr4 = Builder.load_file('../screens/extra/home_screen1.kv')
            self.root.add_widget(scr4)
            self.screen_loaded['home_screen'] = scr4
        self.root.current = 'home_scr'

# class SettingScreen(Screen):
#     def __init__(self, **kwargs):
#         super(SettingScreen, self).__init__(**kwargs)
#
#     def setting_screen(self):
#         if self.screen_loaded['setting_screen'] is None:
#             scr3 = Builder.load_file('screens/setting_screen.kv')
#             self.root.add_widget(scr3)
#             self.screen_loaded['setting_screen'] = scr3
#         self.root.current = 'setting_scr'
#
#
# class AddScreen(Screen):
#
#     def __init__(self, **kwargs):
#         super(AddScreen, self).__init__(**kwargs)
#
#     def add_screen(self):
#         if self.screen_loaded['add_screen'] is None:
#             scr3 = Builder.load_file('screens/apps_screen.kv')
#             self.root.add_widget(scr3)
#             for group, sub in self.apps_assortment.items():
#                 num_of_sub = len(sub)
#                 layout = MDBoxLayout(orientation='vertical', adaptive_height=True, spacing=(0, 10), padding=(0, 10))
#                 for i in sub:
#                     icon_name = 'star-outline'
#                     if i in self.app_fav:
#                         icon_name = 'star'
#                     layout.add_widget(OneLineIconListItem(IconLeftWidget(icon=icon_name,
#                                                                          id = i ,
#                                                                          on_press=self.add_fav),
#                                                           text=i,
#                                                           on_press=self.go_app,
#                                                           ))
#
#                 obj = MDExpansionPanel(
#                     content=layout,
#                     panel_cls=MDExpansionPanelTwoLine(
#                         text=group,
#                         secondary_text=f"{num_of_sub} app",
#                     )
#                 )
#                 self.root.get_screen('add_scr').ids.content.add_widget(obj)
#             self.screen_loaded['add_screen'] = scr3
#         self.root.current = 'add_scr'
#
#     def add_fav(self , args):
#         app = args.id
#         if app not in self.app_fav:
#             self.app_fav.append(app)
#             args.icon = 'star'
#             self.notification(f"{app} app add to favorite menu")
#         else:
#             self.app_fav.remove(app)
#             args.icon = 'star-outline'
#             self.notification( f"{app} app remove from favorite menu")
#         self.floating_update()


# class FocusWidget(MDBoxLayout, RectangularElevationBehavior, FocusBehavior):
#     pass

# class CustomSnackbar(BaseSnackbar):
#     text = StringProperty(None)
#     icon = StringProperty(None)
#     font_size = NumericProperty("11sp")


# noinspection PyTypeChecker
class MedFunc(MedUser, LoadingScreen,HomeScreen,):
    pre_build_file = '../med_kivy.kv'
    data = DictProperty()

    def __init__(self, **kwargs):
        super(MedFunc, self).__init__(**kwargs)

    def get_root_size(self):
        self.size = (300, 500)
        Window.size = self.size

    def build(self):
        self.theme_cls = ThemeManager()
        self.theme_cls.colors = self.colors
        self.theme_cls.material_style = "M2"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.theme_style = "Dark"

        self.data = {
            'Python': 'language-python',
            'JS': [
                'language-javascript',
                "on_press", lambda x: print("pressed JS"),
                "on_release", lambda x: print(
                    "stack_buttons",
                    self.root.ids.speed_dial.stack_buttons
                )
            ],
            'PHP': [
                'language-php',
                "on_press", lambda x: print("pressed PHP"),
                "on_release", self.callback
            ],
            'C++': [
                'language-cpp',
                "on_press", lambda x: print("pressed C++"),
                "on_release", lambda x: self.callback()
            ],
        }
        pre_build = Builder.load_file(self.pre_build_file)

        return pre_build

    def on_start(self):
        self.loading_screen()

    def callback(self, *args):
        print(args)

    def go_to_screen(self, screen):
        if screen == 'load':
            self.load_screen()
        if screen == 'log':
            self.log_screen()
        if screen == 'login':
            self.login_screen()
        if screen == 'home':
            self.home_screen()
    #
    # def show_dialog(self, title=None, dialog_text=None, args=None):
    #     if not self.dialog:
    #         self.dialog = MDDialog(
    #             title=title,
    #             text=dialog_text,
    #             opacity=.8,
    #             md_bg_color=self.theme_cls.bg_normal,
    #             pos_hint={'center_x': .5, 'center_y': .5},
    #             buttons=args
    #         )
    #     self.dialog.open()
    #
    # def close_dialog(self, touch):
    #     # print(touch)
    #     self.dialog.dismiss()
    #     self.dialog = None

    # def tap_target_start(self, button, title, desc, pos):
    #     if self.tap_target_view.state == "open":
    #         if self.tap_target_view.widget == button:
    #             self.tap_target_view.stop()  # stop this if opened when screen change
    #     elif self.tap_target_view.state == "close":
    #         self.tap_target_view.widget = button
    #         self.tap_target_view.title_text = title
    #         self.tap_target_view.description_text = desc
    #         self.tap_target_view.widget_position = pos
    #         self.tap_target_view.start()

    # noinspection PyTypeChecker
    # def floating_drawer(self):
    #     pass
        # self.float_action_button = MDFloatingActionButtonSpeedDial(
        #     data=self.floating_data,
            # bg_color_root_button=self.theme_cls.bg_light,
            # bg_color_stack_button=self.theme_cls.bg_light,
            # icon="star",
            # label_bg_color=self.theme_cls.bg_normal,
            # label_text_color=self.theme_cls.primary_color,
            # color_icon_stack_button=self.theme_cls.primary_color,
            # color_icon_root_button=self.theme_cls.primary_color,
            # opacity=1,
            # id="speeddial",
            # size_hint=[1, 2],
            # label_radius=[3, 0, 0, 3],
            # opening_time=.5,
            # closing_time=.5,
            # closing_time_button_rotation=.5,
            # opening_time_button_rotation=.5,
            # root_button_anim=True ,
        # )
        # self.root.get_screen('home_scr').ids.screen1.add_widget(self.float_action_button)
        # self.screen_loaded['speed_dial'] = self.float_action_button
        # self.floating_update()

    # def floating_update(self):
    #     print(self.float_action_button.data)
    #     self.float_action_button.data = {
    #         'cbc': ['account', "on_press", lambda x: self.go_app(self.clean_str('v'))] ,
    #         'i': ['account', "on_press", lambda x: self.go_app(self.clean_str('v'))]
    #     }
    #     # self.float_action_button.bg_color_root_button = self.theme_cls.bg_light
    #     # self.float_action_button.bg_color_stack_button = self.theme_cls.bg_light
    #     # # self.float_action_button.label_bg_color = self.theme_cls.bg_normal
    #     # self.float_action_button.label_text_color = self.theme_cls.primary_color
    #     # self.float_action_button.color_icon_stack_button = self.theme_cls.primary_color
    #     # self.float_action_button.color_icon_root_button = self.theme_cls.primary_color
    #     # all_apps = []
    #     # self.floating_data ={}
    #     #
    #     # for k , v in self.apps_assortment.items():
    #     #     for i in v:
    #     #         all_apps.append(i)
    #     # for i in self.app_fav:
    #     #     if i not in all_apps:
    #     #         self.app_fav.remove(i)
    #     #     else:
    #     #         self.floating_data.update({i:['account' ,"on_press", lambda x: self.go_app(self.clean_str(i))]})
    #     #         self.float_action_button.data=self.floating_data
    # #
    # # def clean_str(self, varStr):
    # #     return re.sub(r'\W+|^(?=\d)', '_', varStr)
    # #
    # # def go_app(self, args):
    # #     print(args, 'arge')


# class MedSuiteApp(MedFunc):
#
#     def __init__(self, **kwargs):
#         super(MedSuiteApp, self).__init__(**kwargs)
#         self.snackbar =None
#         self.more = ''
#     # def test(self, *args):
#     #     print('test')
#     #     # print(args.lbl_ic.badge_icon)
#     #     # args.lbl_ic.badge_icon = 'numeric-10'
#     #     # print(args.lbl_ic.badge_icon)
#     #     #
#     #     # print(self.root.get_screen('home_scr').get_hero_from_widget())
#     # def notification(self,args):
#     #     if not self.snackbar:
#     #
#     #         # self.snackbar = Snackbar(text = args , font_size =10 , icon= 'information')
#     #         # self.snackbar.open()
#     #         self.snackbar = CustomSnackbar(
#     #             text=args,
#     #             icon="information",
#     #             snackbar_x="2dp",
#     #             snackbar_y="2dp",
#     #             buttons=[MDFlatButton(text="More" ,on_press = self.more_func)]
#     #         )
#     #         self.snackbar.size_hint_x = 1
#     #         self.more = args
#     #         #(
#     #         #     Window.width - (self.snackbar.snackbar_x * 2)/ Window.width
#     #         # )
#     #         self.snackbar.open()
#     #     self.snackbar =None
#     #
#     # def more_func(self , arge):
#     #     self.show_dialog(title ='more' ,
#     #                      dialog_text=self.more ,
#     #                      args = [MDFlatButton(text='Exit',on_press=self.close_dialog)])
#     # def pass_check_box(self, *args):
#     #     # print('pass_check_box function', args)
#     #     if args[0] == 'down':
#     #         self.root.get_screen('login_scr').ids.pass_check.state = 'normal'
#     #     elif args[0] == 'normal':
#     #         self.root.get_screen('login_scr').ids.pass_check.state = 'down'
#     #     elif args[0][1]:
#     #         self.root.get_screen('login_scr').ids.pass_check.text_color = self.theme_cls.primary_color
#     #     elif not args[0][1]:
#     #         self.root.get_screen('login_scr').ids.pass_check.text_color = self.theme_cls.primary_light
#     #
#     # def label1_change(self, args):
#     #     self.root.get_screen('home_scr').ids.label1.text = args
#     #
#     # def change_theme(self, theme):
#     #     if theme == 'Light':
#     #         self.theme_cls.primary_palette = "Cyan"
#     #         self.theme_cls.accent_palette = "Blue"
#     #         self.theme_cls.theme_style = "Light"
#     #     elif theme == 'Dark':
#     #         self.theme_cls.primary_palette = "Teal"
#     #         self.theme_cls.accent_palette = "Red"
#     #         self.theme_cls.theme_style = "Dark"


if __name__ == '__main__':
    app = MedFunc()
    app.run()
