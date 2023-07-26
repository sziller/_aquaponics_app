import os
import sys

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


class AppObjScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(AppObjScreenManager, self).__init__(**kwargs)
        self.statedict = {
            "screen_status": {
                "seq": 0,
                'inst': 'button_nav_status',
                'down': ['button_nav_status'],
                'normal': ["button_nav_control"]},
            "screen_control":  {
                "seq": 1,
                'inst': 'button_nav_control',
                'down': ['button_nav_control'],
                'normal': ["button_nav_status"]}
            }


class OperationAreaBox(BoxLayout):
    pass


class OpAreaStatus(OperationAreaBox):
    def __init__(self, **kwargs):
        super(OpAreaStatus, self).__init__(**kwargs)

    def on_release_update(self, instance):
        for key, value in App.get_running_app().status_last_update.items():
            lbl_txt = App.get_running_app().status_fillin_code[key]["lbl"]
            keycode = App.get_running_app().status_fillin_code[key]["assign"]
            if keycode:
                self.ids[lbl_txt].text = keycode[value]
            else:
                self.ids[lbl_txt].text = value


class NavBar(BoxLayout):
    """=== Class name: NavBar ==========================================================================================
    This Layout can be used across all screens. Class handles complications of not-yet-drawn instances.
    It sets appearance for instances only appearing on screen.
    ============================================================================================== by Sziller ==="""

    @ staticmethod
    def on_release_navbar(inst):
        """=== Method name: on_toggle_navbar ===========================================================================
        Method manages multiple screen selection by Toggle button set.
        All Toggle Buttons call this same function. Their Class names are stored in the <buttons> list.
        Only one button of the entire set is down at a given time. Function is extendable.
        Once a given button is 'down', it becomes inactive, all other buttons are activated and set to "normal" state.
        The reason of the logic is as follows:
        Screen manager is the unit taking care of actual screen swaps, also it stores actually shown screen name.
        However, at the itme of instantiation of the Screen Manager's ids are still not accessible.
        So we refer to ScreenManager's id's only on user action.
        :var inst: - the instance (button) activating the Method.
        ========================================================================================== by Sziller ==="""
        old_seq: int = 0
        for k, v in App.get_running_app().root.statedict.items():
            if k == App.get_running_app().root.current_screen.name:
                old_seq = v["seq"]
                break
        new_seq = App.get_running_app().root.statedict[inst.target]["seq"]

        App.get_running_app().change_screen(screen_name=inst.target, screen_direction={True: "left", False: "right"}
        [old_seq - new_seq < 0])
        for buttinst in App.get_running_app().root.current_screen.ids.navbar.ids:
            if buttinst in App.get_running_app().root.statedict[inst.target]['normal']:
                App.get_running_app().root.current_screen.ids.navbar.ids[buttinst].disabled = False
                App.get_running_app().root.current_screen.ids.navbar.ids[buttinst].state = "normal"
            if buttinst in App.get_running_app().root.statedict[inst.target]['down']:
                App.get_running_app().root.current_screen.ids.navbar.ids[buttinst].disabled = True
                App.get_running_app().root.current_screen.ids.navbar.ids[buttinst].state = "down"


class AppAquaManager(App):
    """=== Class name: AppObj ========================================================================================
    Child of built in class: App
    This is the Parent application for a project.
    Instantiation should - contrary to what is used on the net - happen by assigning it to a variable name.
    :param window_content:
    ============================================================================================== by Sziller ==="""
    def __init__(self,
                 window_content: str,
                 app_title: str = "Sziller's App",
                 app_icon: str = "./icon.png",
                 csm: float = 1.0):
        super(AppAquaManager, self).__init__()
        self.title                      = app_title
        self.icon                       = app_icon
        self.window_content             = window_content
        self.content_size_multiplier    = csm
        self.external_var: list         = []

        self.status_last_update: dict   = {"system_on": True,
                                           "last_waterstream": "00:00",
                                           "last_feeding": "00:00",
                                           "last_shade_raise": "00:00",
                                           "last_shade_lower": "00:00",
                                           "lights-01": False,
                                           "lights-02": False,
                                           "air_circulation": False,
                                           "ventillation": False}
        self.status_fillin_code: dict   = {
            "system_on":         {"lbl": "labelval_system", "assign": {True: "on", False: "off"}},
            "last_waterstream":  {"lbl": "labelval_waterstream", "assign": {}},
            "last_feeding":      {"lbl": "labelval_feeding", "assign": {}},
            "last_shade_raise":  {"lbl": "labelval_shade_up", "assign": {}},
            "last_shade_lower":  {"lbl": "labelval_shade_down", "assign": {}},
            "lights-01":         {"lbl": "labelval_light1", "assign": {True: "on", False: "off"}},
            "lights-02":         {"lbl": "labelval_light2", "assign": {True: "on", False: "off"}},
            "air_circulation":   {"lbl": "labelval_circulation", "assign": {True: "on", False: "off"}},
            "ventillation":      {"lbl": "labelval_ventillation", "assign": {True: "on", False: "off"}}}


    def change_screen(self, screen_name, screen_direction="left"):
        """=== Method name: change_screen ==============================================================================
        Use this screen-changer instead of the built-in method for more customizability and to enable further
        actions before changing the screen.
        Also, if screen-changing first needs to be validated, use this method!
        ========================================================================================== by Sziller ==="""
        smng = self.root  # 'root' refers to the only one root instance in your App. Here it is the actual ROOT
        smng.current = screen_name
        smng.transition.direction = screen_direction

    def build(self):
        return self.window_content


if __name__ == "__main__":
    from kivy.lang import Builder  # to freely pick kivy files

    # use presets to
    display_settings = {0: {'fullscreen': False,    'run': Window.maximize},   # cover screen with titlebar accessible
                        1: {'fullscreen': True,     'run': Window.maximize},   # Full-screen mode
                        2: {'fullscreen': False,    'size': (480, 640)},       # Portrait  Raspberry Display
                        3: {'fullscreen': False,    'size': (640, 480)},       # Landscape Raspberry Display
                        4: {'fullscreen': False,    'size': (480, 960)},       # Portrait  Cellphone
                        5: {'fullscreen': False,    'size': (960, 480)},       # Landscape Cellphone
                        6: {'fullscreen': False,    'size': (800, 800)},       # Qubic layout
                        }
    style_code = 4

    Window.fullscreen = display_settings[style_code]['fullscreen']
    if 'size' in display_settings[style_code].keys(): Window.size = display_settings[style_code]['size']
    if 'run' in display_settings[style_code].keys(): display_settings[style_code]['run']()

    Window.top = 40
    Window.left = 40

    try:
        content = Builder.load_file(str(sys.argv[1]))
    except IndexError:
        content = Builder.load_file("app_aquamanager.kv")

    application_title_in_window_head    = "AquaManager"
    application_window_icon             = "./icons/caution.png"
    content_size_multiplier             = 1

    application = AppAquaManager(window_content=content,
                                 app_title=application_title_in_window_head,
                                 app_icon=application_window_icon,
                                 csm=content_size_multiplier)

    data_from_app = application.external_var
    application.run()
