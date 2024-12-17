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
