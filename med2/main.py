from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
medkv = """
MDScreen:
    MDFlatButton:
        text: "MDFlatButton"  
        theme_text_color: "Custom"
        text_color: "orange"
        pos_hint: {'center_x':.5, 'center_y':.5}
           
    MDRaisedButton:
        text: "MDRaisedButton"
        md_bg_color: "red"
    """
class MedApp(MDApp):

    def build(self):
        Window.maximize()
        return Builder.load_string(medkv)


if __name__ == '__main__':
    app = MedApp()
    app.run()