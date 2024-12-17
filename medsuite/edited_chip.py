import os

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, ColorProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import (
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ScaleBehavior,
    TouchBehavior,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDIcon
path = os.path.dirname(__file__)
with open(
    os.path.join(path, "edited_chip.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class MyChip(
    MDBoxLayout,
    ThemableBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    CommonElevationBehavior,
    TouchBehavior,
):
    text = StringProperty()
    """
    Chip text.

    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    icon_left = StringProperty()
    """
    Chip left icon.

    .. versionadded:: 1.0.0

    :attr:`icon_left` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    icon_right = StringProperty()
    """
    Chip right icon.

    .. versionadded:: 1.0.0

    :attr:`icon_right` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    text_color = ColorProperty(None)
    """
    Chip's text color in (r, g, b, a) or string format.

    :attr:`text_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    icon_right_color = ColorProperty(None)
    """
    Chip's right icon color in (r, g, b, a) or string format.

    .. versionadded:: 1.0.0

    :attr:`icon_right_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    icon_left_color = ColorProperty(None)
    """
    Chip's left icon color in (r, g, b, a) or string format.

    .. versionadded:: 1.0.0

    :attr:`icon_left_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    icon_check_color = ColorProperty(None)
    """
    Chip's check icon color in (r, g, b, a) or string format.

    .. versionadded:: 1.0.0

    :attr:`icon_check_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    active = BooleanProperty(False)
    """
    Whether the check is marked or not.

    .. versionadded:: 1.0.0

    :attr:`active` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_long_touch(self, *args) -> None:
        if self.active:
            return
        self.active = True if not self.active else False

    def on_active(self, instance_check, active_value: bool) -> None:
        if active_value:
            self.do_animation_check((0, 0, 0, 0.4), 1)
        else:
            self.do_animation_check((0, 0, 0, 0), 0)

    def do_animation_check(self, md_bg_color: list, scale_value: int) -> None:
        Animation(md_bg_color=md_bg_color, t="out_sine", d=0.1).start(
            self.ids.icon_left_box
        )
        Animation(
            scale_value_x=scale_value,
            scale_value_y=scale_value,
            scale_value_z=scale_value,
            t="out_sine",
            d=0.1,
        ).start(self.ids.check_icon)

        if not self.icon_left:
            if scale_value:
                self.ids.check_icon.x = -dp(4)
                Animation(size=(dp(24), dp(24)), t="out_sine", d=0.1).start(
                    self.ids.relative_box
                )
            else:
                self.ids.check_icon.x = 0
                Animation(size=(0, 0), t="out_sine", d=0.1).start(
                    self.ids.relative_box
                )

    def on_press(self, *args):
        if self.active:
            self.active = False


class MDScalableCheckIcon(MDIcon, ScaleBehavior):
    """ change setting for pos_hint keyerror"""    # edited
    # pos_hint = {"center_y": 0.5}
