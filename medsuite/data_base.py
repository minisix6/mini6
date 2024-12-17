from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker
import time
from kivymd.app import MDApp
from kivymd.theming import ThemeManager

hint_font_size = 14

Base = declarative_base()


class AppTheme(Base):
    __tablename__ = 'app_theme'
    id = Column(Integer, primary_key=True)
    theme = Column(String(10), nullable=False)
    language = Column(String(10), nullable=False)
    app_text_size = Column(String(10), nullable=False)
    notification = Column(String(10), nullable=False)
    # def __repr__(self):
    #     return "no"


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
            data_return['screen'] = 'load_scr'
        else:
            # save time
            data_return['screen'] = f"{dic_data['statue']}_scr"
            if dic_data['statue'] == 'signIn':
                data_return['screen'] = 'login_scr'
                data_return['userName'] = dic_data['userName']
                data_return['pass'] = dic_data['pass']
                data_return['savePass'] = dic_data['savePass']
                if dic_data['logOut'] == 'n':
                    # if dic_data['access'] == 'deny':
                    #     data_return['screen'] = 'login_error'
                    #     data_return['error'] = 'an error check payment'
                    # else:
                    data_return['screen'] = 'home_scr'
        return data_return

    def return_data_to_save(self, dic):
        if dic is True:
            self.api_user_allow.append(dic)


class SqlReceive:
    def __init__(self):
        self.engine = create_engine('sqlite:///app_data')
        Base.metadata.create_all(self.engine)
        DBsession = sessionmaker(bind=self.engine)
        self.session = DBsession()
        self.result = self.session.query(AppTheme).all()
        sql_first_time = 0  # =>open the first screen => change to '0' in second time and open the second screen

    def create_table(self):
        # if table_name == 'app_theme':
        theme1 = AppTheme(
            theme='Dark',
            language='Persian',
            app_text_size='Medium',
            notification='False')
        self.session.add(theme1)
        self.session.commit()

    def update_table(self, kwargs):
        print(kwargs)
        query1 = self.session.query(AppTheme).first()
        query1.theme = kwargs['theme']
        query1.language = kwargs['language']
        query1.app_text_size = kwargs['app_text_size']
        query1.notification = kwargs['notification']
        self.session.commit()

    def load_sql_data(self):
        dict1 = {}
        query1 = self.session.query(AppTheme).first()
        dict1['theme'] = query1.theme
        dict1['language'] = query1.language
        dict1['app_text_size'] = query1.app_text_size
        dict1['notification'] = query1.notification
        return dict1


class MedData(MDApp):
    mac_con = '18'  # get mac adress and ip
    apps_assortment = {'Medical Terminology Dictionary': ['Medical Terminology Dictionary'],
                       'Scales': ['MORSE', 'BRADEN', 'BMI', 'Clearance', 'GCS', 'WELLS', 'ForeScore', 'NGASR'],
                       'Drugs': ['Iran Generic Pharmacy', 'Drug Interactions', 'Pharmaceutical Calculations'],
                       'Laboratory': ['ABG', 'CBC']}
    pass_check = 'crop-square'
    install = 'install'  # and 'reinstall' , 'None'
    colors = {
        "Teal": {"200": "#fffad4", "500": "#fff2b3", "700": "#99916b", 'A700': '#666147'},
        "Red": {"200": "#ffea80", "500": "#578994", "700": "#27484f", "A700": "#d13d5a"},
        "Cyan": {"200": "#b85171", "500": "#b56780", "700": "#c4879b", 'A700': '#fff066'},
        "Blue": {"200": "#ed6f99", "500": "#ed93b1", "700": "#ffadc9", "A700": "#fff066"},
        "Dark": {"StatusBar": "#ffffff", "AppBar": "#162426", "Background": "#304e54", "CardsDialogs": "#436d75"},
        "Light": {"StatusBar": "#bdf0f0", "AppBar": "#fff5db", "Background": "#fffee5", "CardsDialogs": "#fff1d4"},
    }

    setting_screen_data = {'language': 'English', 'theme': 'Dark', 'app_text_size': 'Medium', 'notification': 'True'}

    def __init__(self, **kwargs):
        super(MedData, self).__init__(**kwargs)
        self.primary_data = {}
        self.theme_cls = ThemeManager()
        self.api = ApiReceive()
        self.sql = SqlReceive()
        if len(self.sql.result) == 0:
            self.sql.create_table()
        self.statue = ''
        # self.default_theme = self.sql.default_theme
        # self.colors = self.sql.colors
        self.window_width = 324
        self.window_height = 702
        self.theme_font_size = self.window_width * .04
        self.next_screen = None
        self.theme_font_style1 = 'Button'
        self.theme_font_style2 = 'Caption'
        self.theme_font_style3 = 'Subtitle1'
        self.theme_cls.colors = self.colors
        self.theme_cls.widget_style = 'desktop'
        self.theme_cls.opposite_colors = True
        self.add_tab_list = []
        self.add_widget_list = []
        self.float_action_button = object
        self.app_list = []
        self.app_fav = ['MORSE', 'BMI', 'GCS']
        self.floating_data = {}
        self.primary_data = self.check_con()

    def reload_theme(self):
        global hint_font_size
        self.theme_cls.theme_style = self.setting_screen_data['theme']
        if self.theme_cls.theme_style == 'Dark':
            self.theme_cls.primary_palette = "Teal"
            self.theme_cls.accent_palette = "Red"
        else:
            self.theme_cls.primary_palette = "Cyan"
            self.theme_cls.accent_palette = "Blue"
        if self.setting_screen_data['app_text_size'] == 'Small':
            self.theme_font_size = self.window_width * .03
            self.theme_font_style1 = 'Caption'
            self.theme_font_style2 = 'Overline'
            self.theme_font_style3 = 'Subtitle2'
            hint_font_size = self.window_width * .04
        elif self.setting_screen_data['app_text_size'] == 'Medium':
            self.theme_font_size = self.window_width * .04
            self.theme_font_style1 = 'Button'
            self.theme_font_style2 = 'Caption'
            self.theme_font_style3 = 'Subtitle1'
            hint_font_size = self.window_width * .05
        elif self.setting_screen_data['app_text_size'] == 'Large':
            self.theme_font_size = self.window_width * .05
            self.theme_font_style1 = 'Subtitle1'
            self.theme_font_style2 = 'Subtitle2'
            self.theme_font_style3 = 'Button'
            hint_font_size = self.window_width * .06
        self.theme_cls.material_style = 'M2'
        self.theme_cls.primary_dark_hue = '700'
        self.theme_cls.primary_hue = '500'
        self.theme_cls.primary_light_hue = '200'
        self.theme_cls.accent_hue = '500'
        self.theme_cls.accent_light_hue = '200'
        self.theme_cls.accent_dark_hue = '700'

    def load_primary_data(self):
        self.setting_screen_data = self.sql.load_sql_data()
        self.reload_theme()
        time.sleep(2)
        # return self.primary_data['screen']
        return 'log_scr'

    def refresh_app_list(self):
        for k, v in self.apps_assortment.items():
            for i in v:
                self.app_list.append(i)
        for i in self.app_fav:
            if i not in self.app_list:
                self.app_fav.remove(i)

    def check_con(self):
        dic = self.api.primary_api_check(mac_con=self.mac_con)
        # if error dic[screen] = error and [error] = exception
        # dic['screen']='error'
        # dic['error']='check connection and retry'
        return dic

    def data_update(self, table, kwargs):
        if table == 'app_theme':
            self.sql.update_table(kwargs)
