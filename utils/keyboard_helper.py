"""
Keyboard Helper - 解决Pygame键盘输入问题的辅助库
使用 keyboard 库提供可靠的键盘输入检测，不依赖Pygame的文本输入系统

注意：此模块版权属于Deepseek大模型
"""

import threading
from typing import Dict, Set, Callable, Optional, List, Any
import keyboard
from keyboard import KeyboardEvent

KEYBOARD_AVAILABLE = True

class KeyboardHelper:
    """
    键盘辅助类，使用 keyboard 库提供可靠的键盘输入检测
    """
    
    def __init__(self) -> None:
        self._keys_pressed: Set[str] = set()
        self._key_handlers: Dict[str, List[Callable[[str], Any]]] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        
        # 键名到字符的映射
        self._key_char_map = self._create_key_char_map()
        
        # 用于跟踪已注册的 keyboard 钩子
        self._keyboard_hooks: List[Any] = []
    
    def _create_key_char_map(self) -> Dict[str, str]:
        """创建键名到字符的映射表"""
        key_char_map: Dict[str, str] = {}
        
        # 字母键
        for char in "abcdefghijklmnopqrstuvwxyz":
            key_char_map[char] = char
        
        # 数字键
        for char in "0123456789":
            key_char_map[char] = char
        
        # 符号键
        key_char_map.update({
            'space': ' ',
            'period': '.',
            'comma': ',',
            'slash': '/',
            'backslash': '\\',
            'minus': '-',
            'equals': '=',
            'left bracket': '[',
            'right bracket': ']',
            'semicolon': ';',
            'quote': "'",
            'backquote': '`',
            'enter': '\n',
            'tab': '\t',
        })
        
        return key_char_map
    
    def start(self) -> None:
        """启动键盘监听"""
        if not KEYBOARD_AVAILABLE:
            print("错误: keyboard 库不可用")
            return
            
        if self._running:
            return
            
        self._running = True
        
        # 注册 keyboard 事件处理器
        self._setup_keyboard_hooks()
        
        # print("KeyboardHelper 已启动")
    
    def _setup_keyboard_hooks(self) -> None:
        """设置 keyboard 库的事件钩子"""
        if not KEYBOARD_AVAILABLE:
            return
            
        # 按键按下事件
        def on_press(event: KeyboardEvent) -> None:
            # 检查 event.name 是否为 None
            if event.name is None:
                return
                
            key_name = event.name.lower()
            
            # 忽略过长的按键名（通常是特殊功能键）
            if len(key_name) > 1 and key_name not in self._key_char_map:
                return
                
            if key_name not in self._keys_pressed:
                self._keys_pressed.add(key_name)
                self._trigger_handlers(key_name, self._key_char_map.get(key_name, key_name))
        
        # 按键释放事件
        def on_release(event: KeyboardEvent) -> None:
            # 检查 event.name 是否为 None
            if event.name is None:
                return
                
            key_name = event.name.lower()
            
            # 忽略过长的按键名
            if len(key_name) > 1 and key_name not in self._key_char_map:
                return
                
            if key_name in self._keys_pressed:
                self._keys_pressed.remove(key_name)
        
        # 注册钩子
        self._keyboard_hooks.append(keyboard.on_press(on_press))
        self._keyboard_hooks.append(keyboard.on_release(on_release))
    
    def stop(self) -> None:
        """停止键盘监听"""
        if not KEYBOARD_AVAILABLE:
            return
            
        self._running = False
        
        # 移除所有 keyboard 钩子
        for hook in self._keyboard_hooks:
            keyboard.unhook(hook)
        self._keyboard_hooks.clear()
        
        # 清空按键状态
        self._keys_pressed.clear()
        
        # print("KeyboardHelper 已停止")
    
    def _trigger_handlers(self, key_name: str, char: str) -> None:
        """触发按键处理函数"""
        if key_name in self._key_handlers:
            for handler in self._key_handlers[key_name]:
                try:
                    handler(char)
                except Exception as e:
                    print(f"按键处理函数错误: {e}")
    
    def add_key_handler(self, key_name: str, handler: Callable[[str], Any]) -> None:
        """
        添加按键处理函数
        
        Args:
            key_name: 
                按键名称，如 'a', 'b', 'space' 等
            handler: 
                处理函数，接收一个字符参数
        """
        if not KEYBOARD_AVAILABLE:
            return
            
        key_name = key_name.lower()
        if key_name not in self._key_handlers:
            self._key_handlers[key_name] = []
        self._key_handlers[key_name].append(handler)
    
    def remove_key_handler(self, key_name: str, handler: Callable[[str], Any]) -> None:
        """移除按键处理函数"""
        if not KEYBOARD_AVAILABLE:
            return
            
        key_name = key_name.lower()
        if key_name in self._key_handlers and handler in self._key_handlers[key_name]:
            self._key_handlers[key_name].remove(handler)
    
    def is_key_pressed(self, key_name: str) -> bool:
        """检查按键是否被按下"""
        if not KEYBOARD_AVAILABLE:
            return False
            
        return key_name.lower() in self._keys_pressed
    
    def get_all_pressed_keys(self) -> List[str]:
        """获取当前按下的所有键"""
        if not KEYBOARD_AVAILABLE:
            return []
            
        return list(self._keys_pressed)
    
    def get_key_char(self, key_name: str) -> Optional[str]:
        """获取键名对应的字符"""
        if not KEYBOARD_AVAILABLE:
            return None
            
        return self._key_char_map.get(key_name.lower())

# 全局实例
_keyboard_helper = KeyboardHelper()

# 便捷函数
def start_keyboard_helper() -> None:
    """启动键盘助手"""
    _keyboard_helper.start()

def stop_keyboard_helper() -> None:
    """停止键盘助手"""
    _keyboard_helper.stop()

def on_key_press(key_name: str, handler: Callable[[str], Any]) -> None:
    """注册按键处理函数"""
    _keyboard_helper.add_key_handler(key_name, handler)

def is_key_pressed(key_name: str) -> bool:
    """检查按键是否被按下"""
    return _keyboard_helper.is_key_pressed(key_name)

def get_pressed_keys() -> List[str]:
    """获取当前按下的所有键"""
    return _keyboard_helper.get_all_pressed_keys()