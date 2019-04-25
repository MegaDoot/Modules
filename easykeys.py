from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import Property, ListProperty as ListProp, DictProperty as DictProp

from itertools import chain

from typing import Iterable, Dict, Callable, Tuple, Any, List, Optional

key_callback = Callable[[bool, int, str, List[str]], Any]
key_bindings = Dict[str, key_callback]
keycode_tup = Tuple[int, str]

class KBInter(EventDispatcher):
    """
    Interface for kivy keyboard manager
    Mostly designed for desktop
    Handles interfacing with keyboard
    All you have to do is add bindings
    """
    keys_down = ListProp()
    _key_binds = ListProp()

    def __init__(self, root,
        down_binds: key_bindings = {},
        up_binds: key_bindings = {},
        full_binds: key_bindings = {}
    ):  
        super().__init__()

        self.bind_keys(True, **down_binds, **full_binds)
        self.bind_keys(False, **up_binds, **full_binds)

        self._keyboard = Window.request_keyboard(self._close_keyboard, root)
        self._keyboard.bind(
            on_key_down = self._key_down,
            on_key_up = self._key_up
        )
    
    def _close_keyboard(self):
        self._keyboard.unbind(
            on_key_down = self.key_down,
            on_key_up = self.key_up
        )
        self._keyboard = None

    def _key_down(self, keyboard, keycode: keycode_tup, text: str, modifiers: List[str]):
        key = keycode[1]
        self._add_down_key(key)
        self._do_binds_for(keycode, True)

    def _key_up(self, keyboard, keycode: keycode_tup):
        self._remove_down_key(keycode[1])
        self._do_binds_for(keycode, False)

    def _do_binds_for(self, keycode, is_down_now):
        other_keys = self._current_keys_without(keycode[1])
        for func in self._binds_for(keycode[1], is_down_now):
            func(is_down_now, *keycode, other_keys)

    def _binds_for(self, key, trigger):
        return map(lambda bind_dict: bind_dict["func"], filter(lambda bind_dict: bind_dict["key"] == key and bind_dict["trigger"] == trigger, self._key_binds))

    def _add_down_key(self, key):
        begotten = set(self.keys_down)
        begotten.add(key)
        self.keys_down = begotten

    def _current_keys_without(self, key):
        begotten = set(self.keys_down)
        try:
            begotten.remove(key)
        except KeyError:
            pass
        return list(begotten)

    def _remove_down_key(self, key):
        self.keys_down = self._current_keys_without(key)

    def bind_key(self, key: str, func: key_callback, trigger: bool = True):
        """
        Binds a key to a function:
        If trigger is True, func is called when key goes down
        If trigger is False, func is called when key goes up
        """
        self._key_binds.append({
            "key": key,
            "func": func,
            "trigger": trigger
        })
    
    def bind_keys(self, trigger: bool = True, **kwargs):
        """
        Bind many keys and functions
        The keys of kwargs are key name and the vals are functions
        Trigger functions as in bind_key
        """
        for key, func in kwargs.items():
            self.bind_key(key, func, trigger)

if __name__ == "__main__":
    from kivy.base import runTouchApp
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.anchorlayout import AnchorLayout
    from utils import i_iter

    root = GridLayout(cols = 3)
    
    root.add_widget(Label(text = "Fully bound to 'a'"))

    full_disp = GridLayout(rows = 2)
    root.add_widget(full_disp)

    full_setters = []
    arg_names = ("Is key down?\nBool", "Key Number\nInt", "Key String\nStr", "Other keys down\nList of Strings")
    for name in arg_names:
        full_disp.add_widget(Label(text = name))
    for name in arg_names:
        out_label = Label(text = str(None))
        full_setters.append(out_label.setter("text"))
        full_disp.add_widget(out_label)
        
    def set_full_disp(*args):
        [full_setters[i](None, str(arg)) for arg, i  in i_iter(args)]
    
    button_anchor = AnchorLayout(anchor_x = "center", anchor_y = "center")
    button_anchor.add_widget(Button(text = "Reset", on_press = lambda *args: set_full_disp(*((None,) * len(arg_names))), size = (200, 100), size_hint = (None, None)))
    root.add_widget(button_anchor)

    root.add_widget(Label(text = "Keys down:"))
    keys_down = Label(text = "[]")
    root.add_widget(keys_down)

    kb = KBInter(root, full_binds = {
        "a": set_full_disp
    })
    kb.bind(keys_down = lambda obj, val: keys_down.setter("text")(obj, str(val)))
    runTouchApp(root)