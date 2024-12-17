import time
from kivy.uix.screenmanager import ScreenManager, Screen
from concurrent.futures import ThreadPoolExecutor as process
from kivymd.uix.button import MDTextButton, MDIconButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivy.lang import Builder
from edited_chip import MyChip
from kivymd.utils import asynckivy
from kivy.animation import Animation
from kivymd.uix.dialog import MDDialog
from kivy.metrics import sp , dp

class MyChip1(MyChip):
    icon_check_color = (0, .5, 1, .8)
    text_color = (.2, .2, .52, 0.8)
    _no_ripple_effect = True

    def on_long_touch(self, *args) -> None:
        pass

    def on_press(self, *args):
        if self.active:
            return
        self.active = True if not self.active else False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(active=self.set_chip_bg_color)
        self.bind(active=self.set_chip_text_color)
        self.icon_check_color = self.theme_cls.bg_light
        self.text_color = self.theme_cls.bg_normal

    def set_chip_bg_color(self, instance_chip, active_value: int):
        '''
        Will be called every time the chip is activated/deactivated.
        Sets the background color of the chip.
        '''

        self.md_bg_color = (
            self.theme_cls.primary_light
            if active_value
            else (
                self.theme_cls.bg_light
                if self.theme_cls.theme_style == "Light"
                else (
                    self.theme_cls.bg_light
                    if not self.disabled
                    else self.theme_cls.primary_dark
                )
            )
        )

    def set_chip_text_color(self, instance_chip, active_value: int):
        Animation(
            color=(0, 0, 0, 1) if active_value else (0, 0, 0, 0.5), d=0.2
        ).start(self.ids.label)


class ToolbarIconButton(MDIconButton):
    pass


class OneLineList(OneLineIconListItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # OneLineIconListItem._txt_bot_pad = '14dp'
        OneLineIconListItem._txt_left_pad = '58dp'
        # print(OneLineList.BaseListItem)


class ExpansionPanel(MDExpansionPanelTwoLine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # MDExpansionPanelTwoLine._txt_bot_pad = '20dp'
        # MDExpansionPanelTwoLine._txt_left_pad = '15dp'


class Sm(ScreenManager):
    pass


class SubSm(ScreenManager):
    pass


class LoadingScreen(Screen):
    def loading_screen(self):
        self.root.current = 'loading_scr'
        for scr in self.root.screen_names:
            if scr != 'loading_scr':
                self.root.remove_widget(self.root.get_screen(scr))
        process1 = process()
        process1.submit(self.try_load)

    def try_load(self):
        return_screen = None
        try:
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


class LoadScreen(Screen):
    def load_screen(self):
        if 'load_scr' not in self.root.screen_names:
            scr = Builder.load_file('screens/load_screen.kv')
            self.root.add_widget(scr)
        self.root.current = 'load_scr'


class LogScreen(Screen):

    def log_screen(self):
        if 'log_scr' not in self.root.screen_names:
            scr = Builder.load_file('./screens/log_screen.kv')
            self.root.add_widget(scr)
        self.root.current = 'log_scr'


class LoginScreen(Screen):
    def login_screen(self):
        if 'login_scr' not in self.root.screen_names:
            scr = Builder.load_file('screens/login_screen.kv')
            self.root.add_widget(scr)
        self.root.current = 'login_scr'
        if bool(self.primary_data['userName']) is True:
            self.root.get_screen('login_scr').ids.user_name_field.text = self.primary_data['userName']
            if bool(self.primary_data['savePass']) is True:
                self.root.get_screen('login_scr').ids.pass_field.text = self.primary_data['pass']


class SignupScreen(Screen):
    def signup_screen(self):
        if 'signup_scr' not in self.root.screen_names:
            scr = Builder.load_file('screens/signup_screen.kv')
            self.root.add_widget(scr)
        self.root.current = 'signup_scr'


class HomeScreen(Screen):
    def home_screen(self):
        if 'home_scr' not in self.root.screen_names:
            scr = Builder.load_file('screens/home_screen.kv')
            self.root.add_widget(scr)
        self.root.current = 'home_scr'
        self.root.get_screen('home_scr').ids.sm_sub.current = 'home_s'
        self.change_top_icon('home_s')
        self.update_speed_dial()

    def update_speed_dial(self):
        self.refresh_app_list()
        self.floating_data = {}
        for i in self.app_fav:
            self.floating_data[i] = ['arrow-left', "on_press", lambda x: self.go_app(x.id)]
        self.root.get_screen('home_scr').ids.speed_dial.data = self.floating_data
        self.root.get_screen('home_scr').ids.speed_dial.elevation = 0
        self.root.get_screen('home_scr').ids.speed_dial._update_pos_buttons(
            self.root.get_screen('home_scr').ids.speed_dial, 300, 500)

    def change_top_icon(self, scr):
        top_icon_list = [
            ['help', lambda x: self.go_to_screen('help_s')],
        ]
        if scr == 'home_s':
            top_icon_list.append(['autorenew', lambda x: self.go_to_screen('refresh_s')])
            top_icon_list.append(['chat', lambda x: self.go_to_screen('chat_s')])
            top_icon_list.append(['apps', lambda x: self.go_to_screen('apps_s')])
            self.root.get_screen('home_scr').ids.top_app.title = 'MedSuite'
        elif scr == 'apps_s':
            top_icon_list.append(['home', lambda x: self.go_to_screen('home_s')])
            self.root.get_screen('home_scr').ids.top_app.title = 'Apps'
        elif scr == 'setting_s':
            top_icon_list.append(['home', lambda x: self.go_to_screen('home_s')])
            self.root.get_screen('home_scr').ids.top_app.title = 'Setting'
        elif scr == 'calculator_s':
            top_icon_list.append(['home', lambda x: self.go_to_screen('home_s')])
            self.root.get_screen('home_scr').ids.top_app.title = 'Calculator'
        self.root.get_screen('home_scr').ids.top_app.right_action_items = top_icon_list


class SettingScreen(Screen):
    def setting_screen(self):
        if 'setting_s' not in self.root.get_screen('home_scr').ids.sm_sub.screen_names:
            scr = Builder.load_file('screens/setting_screen.kv')
            self.root.get_screen('home_scr').ids.sm_sub.add_widget(scr)
        self.change_top_icon('setting_s')
        self.apply_changes()
        self.root.get_screen('home_scr').ids.sm_sub.current = 'setting_s'

    def on_leave(self, *args):
        pass

    def language_chips(self, selected_instance_chip):
        for instance_chip in self.root.get_screen('home_scr').ids.sm_sub.get_screen('setting_s').ids.language.children:
            if instance_chip != selected_instance_chip:
                instance_chip.active = False

    def theme_chips(self, selected_instance_chip):
        for instance_chip in self.root.get_screen('home_scr').ids.sm_sub.get_screen('setting_s').ids.theme.children:
            if instance_chip != selected_instance_chip:
                instance_chip.active = False

    def size_chips(self, selected_instance_chip):
        for instance_chip in self.root.get_screen('home_scr').ids.sm_sub.get_screen(
                'setting_s').ids.app_text_size.children:
            if instance_chip != selected_instance_chip:
                instance_chip.active = False

    def setting_exit(self, args=None):
        if args:
            if args.text == 'Exit without saving':
                self.apply_changes()
                self.go_screen(self.next_screen)
            elif args.text == 'Save and exit':
                # print(self.setting_screen_data)
                for k in self.setting_screen_data:
                    if k == 'notification':
                        self.setting_screen_data[k] = self.root.get_screen('home_scr').ids.sm_sub.get_screen(
                            'setting_s').ids.notification.active
                    else:
                        for child in eval(
                                f" self.root.get_screen('home_scr').ids.sm_sub.get_screen('setting_s').ids."
                                f"{k}.children"):

                            if eval(
                                    f" self.root.get_screen('home_scr').ids.sm_sub.get_screen('setting_s').ids."
                                    f""f"{child.text}").active:
                                self.setting_screen_data[k] = child.text
                self.data_update('app_theme', self.setting_screen_data)
                self.apply_changes()
                self.reload_theme()
                self.loading_screen()
                self.go_screen(self.next_screen)
                # print(self.setting_screen_data)
        else:
            print('else')
        if self.dialog:
            # print(self.dialog)
            self.dialog.dismiss()
            self.dialog = None

    def apply_changes(self, args=None):
        for k, v in self.setting_screen_data.items():
            if k == 'notification':
                self.root.get_screen('home_scr').ids.sm_sub.get_screen(
                    'setting_s').ids.notification.active = v
            else:
                for child in eval(
                        f" self.root.get_screen('home_scr').ids.sm_sub.get_screen('setting_s').ids."
                        f"{k}.children"):
                    eval(
                        f" self.root.get_screen('home_scr').ids.sm_sub.get_screen('setting_s').ids."
                        f"{child.text}").active = False
                    if child.text == v:
                        eval(
                            f" self.root.get_screen('home_scr').ids.sm_sub.get_screen('setting_s').ids."
                            f"{child.text}").active = True

    def check_setting_changes(self):
        print(self.setting_screen_data)
        print(str(self.root.get_screen('home_scr').ids.sm_sub.get_screen(
                        'setting_s').ids.notification.active))
        for k, v in self.setting_screen_data.items():
            if k == 'notification':
                if str(self.root.get_screen('home_scr').ids.sm_sub.get_screen(
                        'setting_s').ids.notification.active) != v:
                    # print('return1')
                    return 'not_allowed_exit_setting'
            else:
                for child in eval(
                        f" self.root.get_screen('home_scr').ids.sm_sub.get_screen('setting_s').ids."
                        f"{k}.children"):
                    if eval(
                            f" self.root.get_screen('home_scr').ids.sm_sub.get_screen('setting_s').ids."
                            f"{child.text}").active:
                        if child.text != v:
                            # print('return2')
                            return 'not_allowed_exit_setting'


class AppsScreen(Screen):
    def apps_screen(self):
        if 'apps_s' not in self.root.get_screen('home_scr').ids.sm_sub.screen_names:
            scr = Builder.load_file('screens/apps_screen.kv')
            self.root.get_screen('home_scr').ids.sm_sub.add_widget(scr)
            for group, sub in self.apps_assortment.items():
                num_of_sub = len(sub)
                layout = MDBoxLayout(orientation='vertical', adaptive_height=True, spacing=10, padding=(10, 5))
                for i in sub:
                    icon_name = 'star-outline'
                    if i in self.app_fav:
                        icon_name = 'star'
                    layout.add_widget(OneLineList(IconLeftWidget(icon=icon_name,
                                                                 id=i,
                                                                 on_press=self.add_fav,
                                                                 icon_size='15dp'),
                                                  text=i,
                                                  on_press=self.go_app,

                                                  ))

                obj = MDExpansionPanel(
                    content=layout,
                    panel_cls=ExpansionPanel(
                        text=group,
                        secondary_text=f"{num_of_sub} app",
                    )
                )
                obj.opacity = .9
                obj.panel_cls._txt_left_pad = '10dp'
                self.root.get_screen('home_scr').ids.sm_sub.get_screen('apps_s').ids.content.add_widget(obj)
        self.change_top_icon('apps_s')
        self.root.get_screen('home_scr').ids.sm_sub.current = 'apps_s'

    def add_fav(self, args):
        app = args.id
        if app not in self.app_fav:
            self.app_fav.append(app)
            args.icon = 'star'
        else:
            self.app_fav.remove(app)
            args.icon = 'star-outline'
        self.update_speed_dial()


class CalculatorScreen(Screen):
    def calculator_screen(self):
        if 'calculator_s' not in self.root.get_screen('home_scr').ids.sm_sub.screen_names:
            scr = Builder.load_file('screens/calculator_screen.kv')
            self.root.get_screen('home_scr').ids.sm_sub.add_widget(scr)
        self.change_top_icon('calculator_s')
        self.root.get_screen('home_scr').ids.sm_sub.current = 'calculator_s'

    def calculate(self, button):
        if button == 'C':
            self.root.get_screen('home_scr').ids.sm_sub.get_screen('calculator_s').ids.label.text = '0'
        elif button == 'B':
            self.root.get_screen('home_scr').ids.sm_sub.get_screen('calculator_s').ids.label.text \
                = self.root.get_screen('home_scr').ids.sm_sub.get_screen(
                'calculator_s').ids.label.text[:-1]
        elif button == '=':
            try:
                self.root.get_screen('home_scr').ids.sm_sub.get_screen('calculator_s').ids.label.text = str(
                    eval(self.root.get_screen('home_scr').ids.sm_sub.get_screen('calculator_s').ids.label.text)
                )
            except:
                self.root.get_screen('home_scr').ids.sm_sub.get_screen('calculator_s').ids.label.text = 'Error'
        else:
            if self.root.get_screen('home_scr').ids.sm_sub.get_screen('calculator_s').ids.label.text == '0':
                self.root.get_screen('home_scr').ids.sm_sub.get_screen('calculator_s').ids.label.text = ''
            self.root.get_screen('home_scr').ids.sm_sub.get_screen('calculator_s').ids.label.text += button
