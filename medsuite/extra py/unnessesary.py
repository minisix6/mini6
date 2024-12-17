from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.font_definitions import theme_font_styles
# from kivymd.uix.screen import MDScreen, MDHeroTo
# from kivymd.uix.screenmanager import MDScreenManager
# from kivymd.uix.transition import MDSlideTransition, MDSwapTransition, MDFadeSlideTransition
# from kivymd.uix.taptargetview import MDTapTargetView
# from kivy.core.text import Label
# from kivy.core.text import LabelBase
# from kivymd import fonts_path


fonts = [
    {
        "name": "Roboto",
        "fn_regular": fonts_path + "Roboto-Regular.ttf",
        "fn_bold": fonts_path + "Roboto-Bold.ttf",
        "fn_italic": fonts_path + "Roboto-Italic.ttf",
        "fn_bolditalic": fonts_path + "Roboto-BoldItalic.ttf",
    },
    {
        "name": "RobotoThin",
        "fn_regular": fonts_path + "Roboto-Thin.ttf",
        "fn_italic": fonts_path + "Roboto-ThinItalic.ttf",
    },
    {
        "name": "RobotoLight",
        "fn_regular": fonts_path + "Roboto-Light.ttf",
        "fn_italic": fonts_path + "Roboto-LightItalic.ttf",
    },
    {
        "name": "RobotoMedium",
        "fn_regular": fonts_path + "Roboto-Medium.ttf",
        "fn_italic": fonts_path + "Roboto-MediumItalic.ttf",
    },
    {
        "name": "RobotoBlack",
        "fn_regular": fonts_path + "Roboto-Black.ttf",
        "fn_italic": fonts_path + "Roboto-BlackItalic.ttf",
    },
    {
        "name": "Icons",
        "fn_regular": fonts_path + "materialdesignicons-webfont.ttf",
    },
]

for font in fonts:
    LabelBase.register(**font)
#
theme_font_styles = [
    "H1",
    "H2",
    "H3",
    "H4",
    "H5",
    "H6",
    "Subtitle1",
    "Subtitle2",
    "Body1",
    "Body2",
    "Button",
    "Caption",
    "Overline",
    "Icon",
]

class Tab(MDTabs, MDTabsBase):
    pass


# Label.register(
#     name="NPIGhalam-1",
#     fn_regular="NPIGhalam-1.ttf")
#
#     theme_font_styles.append('NPIGhalam-1')
#     self.theme_cls.font_styles["NPIGhalam-1"] = [
#     "NPIGhalam-1",
#     16,
#     True,
#     0.25,
#     ]
#     theme_font_styles.append('RobotoLight')
#     self.theme_cls.font_styles["RobotoLight"] = [
#     "RobotoLight",
#     16,
#     True,
#     0.25,
#     ]
#     theme_font_styles.append('Icons')
#     self.theme_cls.font_styles["Icons"] = [
#             "Icons",
#             10,
#             True,
#             0.25,
#
#         ]

#
# def on_tab_switch(self, instance_tabs=None, instance_tab=None, instance_tab_label=None, tab_text=None):
#     if len(self.add_widget_list) > 0:
#         self.root.get_screen('add_scr').ids.content.remove_widget(self.add_widget_list[0])
#         self.add_widget_list.clear()
#     scr = Builder.load_file(f'./screens/tab/{tab_text}.kv')
#     self.root.get_screen('add_scr').ids.content.add_widget(scr)
#     self.add_widget_list.append(scr)
#     self.root.get_screen('add_scr').ids.new_top.title = tab_text


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


def floating_drawer(self):
    self.float_action_button = self.root.ids.speed_dial
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

    # [
    # 'language-php',
    # "on_press", lambda x: print("pressed PHP"),
    # "on_release", self.callback
    # ], }

    # self.root.ids.speed_dial.bg_color_root_button = self.theme_cls.bg_light
    # self.root.ids.speed_dial.bg_color_root_button = self.theme_cls.bg_light
    # self.root.ids.speed_dial.bg_color_stack_button = self.theme_cls.bg_light
    # self.root.ids.speed_dial.label_bg_color = self.theme_cls.bg_normal
    # self.root.ids.speed_dial.label_text_color = self.theme_cls.primary_color
    # self.root.ids.speed_dial.color_icon_stack_button = self.theme_cls.primary_color
    # self.root.ids.speed_dial.color_icon_root_button = self.theme_cls.primary_color

    # all_apps = []
    # self.floating_data ={}
    #
    # for k , v in self.apps_assortment.items():
    #     for i in v:
    #         all_apps.append(i)
    # for i in self.app_fav:
    #     if i not in all_apps:
    #         self.app_fav.remove(i)
    #     else:
    #         self.floating_data.update({i:['account' ,"on_press", lambda x: self.go_app(self.clean_str(i))]})
    #         self.float_action_button.data=self.floating_data


def open_item(self, screen_name):
    # title_list = ['ABG', 'VBG', 'Advance', 'Ventilator', 'Auto Set']
    # apps_assortment = {'Medical Terminology Dictionary': ['Medical Terminology Dictionary'],
    #                    'Scales': ['MORSE', 'BRADEN', 'BMI', 'Clearance', 'GCS', 'WELLS', 'ForeScore', 'NGASR'],
    #                    'Drugs': ['Iran Generic Pharmacy', 'Drug Interactions', 'Pharmaceutical Calculations'],
    #                    'Laboratory': ['ABG', 'CBC']}
    self.add_screen()
    # self.root.current = 'add_scr'
    # add_screen = self.root.get_screen('add_scr')
    # for group, sub in apps_assortment.items():
    #     add_screen.ids.content.add_widget(OneLineIconListItem(text=group))

    # if len(self.add_tab_list) > 0:
    #     for i in self.add_tab_list:
    #         self.root.get_screen('add_scr').ids.tabs.remove_widget(i)
    # for item in title_list:
    #     tab = Tab(tab_label_text=item)
    #     self.root.get_screen('add_scr').ids.tabs.add_widget(tab)
    #     self.add_tab_list.append(tab)
    # self.root.get_screen('add_scr').ids.new_top.title = 'ABG'