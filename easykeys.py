from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import Property, ListProperty as ListProp, DictProperty as DictProp

from itertools import chain

from typing import Iterable, Dict, Callable, Tuple, Any, List, Optional

key_callback = Callable[[bool, int, str, List[str]], Any]
key_bindings = Dict[str, key_callback]
keycode_tup = Tuple[int, str]

class KBInter(EventDispatcher):
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

    def bind_key(self, trigger: Optional[bool], key: str, func: key_callback):
        self._key_binds.append({
            "key": key,
            "func": func,
            "trigger": trigger
        })
    
    def bind_keys(self, trigger: Optional[bool], **kwargs):
        for key, func in kwargs.items():
            self.bind_key(trigger, key, func)

if __name__ == "__main__":
    from kivy.base import runTouchApp
    from kivy.uix.label import Label

    root = Label(text="Nothing yet")
    setter = root.setter("text")

    kb = KBInter(root, full_binds = {
        "shift": lambda *args: setter("a", str(args))
    })

    runTouchApp(root)