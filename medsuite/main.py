from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from concurrent.futures import ThreadPoolExecutor as process
import time
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.core.window import Window
from concurrent.futures import ThreadPoolExecutor as process
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar # BaseSnackbar
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors.focus_behavior import FocusBehavior
import re
from kivy.utils import platform
from kivy.animation import Animation
from kivymd.uix.widget import MDWidget
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, DictProperty
from kivymd.uix.scrollview import MDScrollView
from screen_module import SubSm, Sm, LoadingScreen, LoginScreen, SignupScreen, AppsScreen, HomeScreen, LoadScreen, \
    LogScreen, SettingScreen, CalculatorScreen, OneLineList, IconLeftWidget
from data_base import MedData
from kivymd.uix.textfield import MDTextField
# from win32api import GetSystemMetrics
from kivy.metrics import dp, sp
# from data_base import hint_font_size


class InputField(MDTextField):
    # hint_font_size = MedData.hint_font_size
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = (5,5,5,5)

    def on_focus(self, instance_text_field, focus: bool) -> None:
        # TODO: See `cancel_all_animations_on_double_click` method.
        from data_base import hint_font_size
        self._icon_left_label.font_size = hint_font_size * 1.2
        if focus:
            if self.mode == "rectangle":
                self.set_notch_rectangle()
            self.set_static_underline_color([0, 0, 0, 0])
            if (
                    self.helper_text_mode in ("on_focus", "persistent")
                    and self.helper_text
            ):
                self.set_helper_text_color(self.helper_text_color_focus)
            if self.mode == "fill":

                self.set_fill_color(self.fill_color_focus)
            self.set_active_underline_width(self.width)

            self.set_pos_hint_text(
                (dp(28) if self.mode != "line" else dp(18))
                if self.mode != "rectangle"
                else dp(10)
            )
            self.set_hint_text_color(focus)
            self.set_hint_text_font_size(sp(hint_font_size - 3))

            if self.max_text_length:
                self.set_max_length_text_color(self.max_length_text_color)
            if self.icon_right:
                self.set_icon_right_color(self.icon_right_color_focus)
            if self.icon_left:
                self.set_icon_left_color(self.icon_left_color_focus)

            if self.error:
                if self.hint_text:
                    self.set_hint_text_color(focus, self.error)
                if self.helper_text:
                    self.set_helper_text_color(self.error_color)
                if self.max_text_length:
                    self.set_max_length_text_color(self.error_color)
                if self.icon_right:
                    self.set_icon_right_color(self.error_color)
                if self.icon_left:
                    self.set_icon_left_color(self.error_color)
        else:
            self.set_helper_text_color([0,0,0,0])
            if self.helper_text_mode == "persistent" and self.helper_text:
                self.set_helper_text_color(self.helper_text_color_normal)
            if self.mode == "rectangle" and not self.text:
                self.set_notch_rectangle(joining=True)
            if not self.text:
                if self.mode == "rectangle":
                    y = dp(38)
                elif self.mode == "fill":
                    y = dp(36)
                else:
                    y = dp(34)

                self.set_pos_hint_text(y)
                self.set_hint_text_font_size(sp(hint_font_size))
            if self.icon_right:
                self.set_icon_right_color(self.icon_right_color_normal)
            if self.icon_left:
                self.set_icon_left_color(self.icon_left_color_normal)
            if self.hint_text:
                self.set_hint_text_color(focus, self.error)

            self.set_active_underline_width(0)
            self.set_max_length_text_color([0, 0, 0, 0])

            if self.mode == "fill":
                self.set_fill_color(self.fill_color_normal)

            self.error = self._get_has_error() or self.error
            if self.error:
                self.set_static_underline_color(self.error_color)
            else:
                self.set_static_underline_color(self.line_color_normal)


class FocusWidget(MDBoxLayout, RectangularElevationBehavior, FocusBehavior):
    pass


class LineText(MDLabel):
    pass


class TitleText(MDLabel):
    pass


class CustomSnackbar(Snackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("11sp")


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
                    MDFlatButton(text='close', theme_text_color='Custom', text_color=self.theme_cls.accent_dark,
                                 on_press=self.close_dialog, size_hint=(.5, .5)),
                    MDFlatButton(text='forget password', theme_text_color='Custom',
                                 text_color=self.theme_cls.accent_dark,
                                 on_press=self.forget_password, size_hint=(.5, .5))])
        else:
            self.show_dialog(title='invalid username', dialog_text='invalid username', args=[
                MDFlatButton(text='close', theme_text_color='Custom', text_color=self.theme_cls.accent_dark,
                             on_press=self.close_dialog, size_hint=(.5, .5)),
                MDFlatButton(text='sign up', theme_text_color='Custom',
                             text_color=self.theme_cls.accent_dark,
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


class MedFunc(MedUser, LoadingScreen, LoginScreen, SignupScreen, AppsScreen, HomeScreen, LoadScreen, LogScreen,
              SettingScreen, CalculatorScreen):

    def __init__(self, **kwargs):
        super(MedFunc, self).__init__(**kwargs)
        self.snackbar = None
        self.more = ''
        self.dialog = None

    def get_root_size(self):
        # print(platform)
        if platform == 'android':
            Window.maximize()
        else:
            Window.size = (self.window_width, self.window_height)
        # self.theme_font_size = self.window_width * .04

    def callback(self, *args):
        print(args)

    def go_to_screen(self, scr):

        go_screen = 'allowed'
        self.next_screen = scr
        if 'home_scr' in self.root.screen_names:
            if self.root.get_screen('home_scr').ids.sm_sub.current is 'setting_s':
                go_screen = self.check_setting_changes()
                # print('return = ' , go_screen)
        if go_screen is 'not_allowed_exit_setting':
            self.show_dialog(title='Setting changes not saved !', dialog_text='do you want save changes or eject it?',
                             args=[
                                 MDFlatButton(text='Exit without saving', theme_text_color='Custom',
                                              text_color=self.theme_cls.accent_dark,
                                              on_press=self.setting_exit, size_hint=(.5, .5)),
                                 MDFlatButton(text='Save and exit', theme_text_color='Custom',
                                              text_color=self.theme_cls.accent_dark,
                                              on_press=self.setting_exit, size_hint=(.5, .5))])
        else:
            self.go_screen(scr)

    def go_screen(self ,scr):
        screen_list = [
            'loading_scr', 'load_scr', 'log_scr', 'login_scr', 'signup_scr', 'home_s', 'apps_s', 'setting_s',
            'calculator_s'
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
        # print(type(args))
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



class MedApp(MedFunc):

    def __init__(self, **kwargs):
        super(MedApp, self).__init__(**kwargs)

    def build(self):
        self.get_root_size()
        return Builder.load_file('med_kivy.kv')

    def on_start(self):
        self.loading_screen()
        self.load_screen()

    def test(self, *args):
        print('test')


if __name__ == '__main__':
    app = MedApp()
    app.run()
