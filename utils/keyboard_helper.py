"""
Keyboard Helper - 解决Pygame键盘输入问题的辅助库
使用 keyboard 库提供可靠的键盘输入检测，不依赖Pygame的文本输入系统

此文件在AI辅助下生成，由项目作者进行修改、整合与发布。

新增功能：组合键支持，统一接口
"""

import threading
import time
from typing import Dict, Set, Callable, Optional, List, Any, Tuple#, Union
import keyboard
from keyboard import KeyboardEvent

class KeyboardHelper:
    """
    键盘辅助类，使用 keyboard 库提供可靠的键盘输入检测
    支持组合键处理（如 Ctrl+C, Alt+F4 等）
    """
    
    def __init__(self) -> None:
        self._keys_pressed: Set[str] = set()
        self._key_handlers: Dict[str, List[Callable[[], Any]]] = {}
        
        # 新增：组合键处理
        self._combo_handlers: Dict[Tuple[str, ...], List[Callable[[], Any]]] = {}
        self._combo_check_interval: float = 0.05  # 检查组合键的时间间隔（秒）
        self._combo_check_thread: Optional[threading.Thread] = None
        self._combo_keys_buffer: List[Tuple[str, float]] = []  # 记录按键和时间戳
        
        self._running = False
        self._thread: Optional[threading.Thread] = None
        
        # 键名到字符的映射（用于其他用途，不作为参数传递）
        self._key_char_map = self._create_key_char_map()
        
        # 用于跟踪已注册的 keyboard 钩子
        self._keyboard_hooks: List[Any] = []
        
        # 修饰键列表
        self._modifier_keys: Set[str] = {
            'ctrl', 'left ctrl', 'right ctrl',
            'shift', 'left shift', 'right shift',
            'alt', 'left alt', 'right alt',
            'windows', 'left windows', 'right windows',
            'menu'  # 添加menu键
        }
        
        # 组合键中键之间的最大时间间隔（秒）
        self._combo_max_interval: float = 0.5
        
        # 创建按键名标准化映射表
        self._key_normalization_map = self._create_key_normalization_map()
    
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
            'plus': '+',  # 添加加号键
        })
        
        return key_char_map
    
    def _create_key_normalization_map(self) -> Dict[str, str]:
        """创建按键名标准化映射表"""
        normalization_map: Dict[str, str] = {}
        
        # 修饰键标准化
        normalization_map.update({
            'left ctrl': 'ctrl',
            'right ctrl': 'ctrl',
            'left shift': 'shift',
            'right shift': 'shift',
            'left alt': 'alt',
            'right alt': 'alt',
            'left windows': 'windows',
            'right windows': 'windows',
        })
        
        # 特殊键标准化（小键盘键）
        normalization_map.update({
            'num +': 'plus',  # 小键盘加号
            'num -': 'minus',  # 小键盘减号
            'num *': 'multiply',  # 小键盘乘号
            'num /': 'divide',  # 小键盘除号
            'num enter': 'enter',  # 小键盘回车
            'num .': 'period',  # 小键盘点
            'num 0': '0',
            'num 1': '1',
            'num 2': '2',
            'num 3': '3',
            'num 4': '4',
            'num 5': '5',
            'num 6': '6',
            'num 7': '7',
            'num 8': '8',
            'num 9': '9',
        })
        
        # 功能键标准化
        normalization_map.update({
            'page up': 'pageup',
            'page down': 'pagedown',
            'caps lock': 'capslock',
            'scroll lock': 'scrolllock',
            'num lock': 'numlock',
            'print screen': 'printscreen',
            'insert': 'ins',
            'delete': 'del',
        })
        
        # 方向键标准化
        normalization_map.update({
            'up': 'up',
            'down': 'down',
            'left': 'left',
            'right': 'right',
        })
        
        return normalization_map
    
    def start(self) -> None:
        """启动键盘监听"""  
        if self._running:
            return
            
        self._running = True
        
        # 注册 keyboard 事件处理器
        self._setup_keyboard_hooks()
        
        # 启动组合键检查线程
        self._start_combo_check_thread()
        
        # print("KeyboardHelper 已启动")
    
    def _setup_keyboard_hooks(self) -> None:
        """设置 keyboard 库的事件钩子"""
        # 按键按下事件
        def on_press(event: KeyboardEvent) -> None:
            # 检查 event.name 是否为 None
            if event.name is None:
                return
                
            key_name = self._normalize_key_name(event.name)
            
            # 将按键记录到缓冲区（用于组合键检测）
            self._combo_keys_buffer.append((key_name, time.time()))
            
            # 保留最近20个按键记录，防止内存泄漏
            if len(self._combo_keys_buffer) > 20:
                self._combo_keys_buffer.pop(0)
            
            # 忽略过长的按键名（通常是特殊功能键），但允许修饰键
            if (len(key_name) > 1 and 
                key_name not in self._key_char_map and 
                key_name not in self._modifier_keys and
                key_name not in self._key_normalization_map.values()):
                return
                
            if key_name not in self._keys_pressed:
                self._keys_pressed.add(key_name)
                self._trigger_key_handlers(key_name)
        
        # 按键释放事件
        def on_release(event: KeyboardEvent) -> None:
            # 检查 event.name 是否为 None
            if event.name is None:
                return
                
            key_name = self._normalize_key_name(event.name)
            
            # 忽略过长的按键名，但允许修饰键
            if (len(key_name) > 1 and 
                key_name not in self._key_char_map and 
                key_name not in self._modifier_keys and
                key_name not in self._key_normalization_map.values()):
                return
                
            if key_name in self._keys_pressed:
                self._keys_pressed.remove(key_name)
        
        # 注册钩子
        self._keyboard_hooks.append(keyboard.on_press(on_press))
        self._keyboard_hooks.append(keyboard.on_release(on_release))
    
    def _normalize_key_name(self, key_name: str) -> str:
        """标准化键名"""
        key_name = key_name.lower()
        
        # 首先检查映射表
        if key_name in self._key_normalization_map:
            return self._key_normalization_map[key_name]
        
        # 处理左右修饰键（如果不在映射表中）
        if key_name in ['left ctrl', 'right ctrl']:
            return 'ctrl'
        elif key_name in ['left shift', 'right shift']:
            return 'shift'
        elif key_name in ['left alt', 'right alt']:
            return 'alt'
        elif key_name in ['left windows', 'right windows']:
            return 'windows'
        
        # 处理小键盘加号键（额外处理）
        if key_name == 'num +':
            return 'plus'
            
        return key_name
    
    def _start_combo_check_thread(self) -> None:
        """启动组合键检查线程"""
        if self._combo_check_thread and self._combo_check_thread.is_alive():
            return
            
        def combo_checker():
            while self._running:
                try:
                    self._check_combos()
                except Exception as e:
                    print(f"组合键检查错误: {e}")
                
                time.sleep(self._combo_check_interval)
        
        self._combo_check_thread = threading.Thread(
            target=combo_checker,
            daemon=True,
            name="ComboChecker"
        )
        self._combo_check_thread.start()
    
    def _check_combos(self) -> None:
        """检查是否有组合键被按下"""
        if not self._combo_handlers or not self._keys_pressed:
            return
        
        # 清理过时的按键记录（超过最大间隔的）
        current_time = time.time()
        self._combo_keys_buffer = [
            (key, timestamp) for key, timestamp in self._combo_keys_buffer
            if current_time - timestamp <= self._combo_max_interval
        ]
        
        # 获取当前按下的所有键
        pressed_keys = frozenset(self._keys_pressed)
        
        # 检查每个注册的组合键
        for combo_keys, handlers in self._combo_handlers.items():
            # 如果组合键的所有键都在当前按下的键集合中
            if all(key in pressed_keys for key in combo_keys):
                # 检查按键顺序是否匹配（在时间窗口内按正确顺序按下）
                if self._check_combo_sequence(combo_keys):
                    # 触发所有处理函数
                    for handler in handlers:
                        try:
                            handler()
                        except Exception as e:
                            print(f"组合键处理函数错误: {e}")
    
    def _check_combo_sequence(self, combo_keys: Tuple[str, ...]) -> bool:
        """
        检查按键序列是否匹配组合键要求
        返回True如果按键按正确顺序在时间窗口内按下
        """
        if not self._combo_keys_buffer:
            return False
        
        # 查找组合键中每个键的最近按下时间
        key_times = {}
        for key, timestamp in reversed(self._combo_keys_buffer):
            if key in combo_keys and key not in key_times:
                key_times[key] = timestamp
        
        key_times:Dict[str,float]
        # 确保所有键都被按下过
        if len(key_times) != len(combo_keys):
            return False
        
        # 检查按键是否在时间窗口内按正确顺序按下
        times = [key_times[key] for key in combo_keys]
        
        # 按键应该按顺序越来越新（时间戳越来越大）
        for i in range(1, len(times)):
            if times[i] < times[i-1]:
                return False
            
            # 检查时间间隔是否超过最大值
            if times[i] - times[i-1] > self._combo_max_interval:
                return False
        
        return True
    
    def stop(self) -> None:
        """停止键盘监听"""
        self._running = False
        
        # 移除所有 keyboard 钩子
        for hook in self._keyboard_hooks:
            keyboard.unhook(hook)
        self._keyboard_hooks.clear()
        
        # 清空按键状态
        self._keys_pressed.clear()
        self._combo_keys_buffer.clear()
        
        # 等待组合键检查线程结束
        if self._combo_check_thread and self._combo_check_thread.is_alive():
            self._combo_check_thread.join(timeout=1.0)
        
        # print("KeyboardHelper 已停止")
    
    def _trigger_key_handlers(self, key_name: str) -> None:
        """触发按键处理函数"""
        if key_name in self._key_handlers:
            for handler in self._key_handlers[key_name]:
                try:
                    handler()
                except Exception as e:
                    print(f"按键处理函数错误: {e}")
    
    def add_key_handler(self, key_name: str, handler: Callable[[], Any]) -> None:
        """
        添加按键处理函数（普通键）
        
        Args:
            key_name: 
                按键名称，如 'a', 'b', 'space', 'plus' 等
            handler: 
                处理函数，不接受参数
        """            
        key_name = key_name.lower()
        
        # 检查是否为组合键格式（包含'+'）
        if '+' in key_name:
            raise ValueError("请使用 add_combo_handler 或 on_combo_press 注册组合键")
        
        # 检查处理函数类型
        if not callable(handler):
            raise TypeError("handler必须是一个可调用对象")
        
        # 检查处理函数是否接受参数
        import inspect
        sig = inspect.signature(handler)
        params = list(sig.parameters.values())
        
        if len(params) > 0 and params[0].default == inspect.Parameter.empty:
            print(f"警告：按键处理函数 '{key_name}' 不应该接受参数")
        
        # 注册按键处理函数
        if key_name not in self._key_handlers:
            self._key_handlers[key_name] = []
        self._key_handlers[key_name].append(handler)
    
    def add_combo_handler(self, *keys: str, handler: Callable[[], Any]) -> None:
        """
        添加组合键处理函数
        
        Args:
            *keys: 组合键的各个部分，如 'ctrl', 'c'
            handler: 处理函数，不接受参数
        """
        # 类型检查
        if not callable(handler):
            raise TypeError("handler必须是一个可调用对象")
        
        # 检查处理函数是否接受参数
        import inspect
        sig = inspect.signature(handler)
        params = list(sig.parameters.values())
        
        if len(params) > 0 and params[0].default == inspect.Parameter.empty:
            print(f"警告：组合键处理函数不应该接受参数")
        
        # 标准化键名
        normalized_keys = []
        normalized_keys:List[str]
        for key in keys:
            norm_key = self._normalize_key_name(key.strip().lower())
            normalized_keys.append(norm_key)
        
        combo_keys = tuple(normalized_keys)
        
        # 确保至少有两个键
        if len(combo_keys) < 2:
            raise ValueError("组合键必须至少包含两个键")
        
        if combo_keys not in self._combo_handlers:
            self._combo_handlers[combo_keys] = []
        self._combo_handlers[combo_keys].append(handler)
    
    def remove_key_handler(self, key_name: str, handler: Callable[[], Any]) -> None:
        """移除按键处理函数"""   
        key_name = key_name.lower()
        
        # 检查是否为组合键格式
        if '+' in key_name:
            raise ValueError("请使用 remove_combo_handler 移除组合键处理函数")
        
        if key_name in self._key_handlers and handler in self._key_handlers[key_name]:
            self._key_handlers[key_name].remove(handler)
    
    def remove_combo_handler(self, *keys: str, handler: Callable[[], Any]) -> None:
        """移除组合键处理函数"""
        normalized_keys = []
        normalized_keys:List[str]
        for key in keys:
            norm_key = self._normalize_key_name(key.strip().lower())
            normalized_keys.append(norm_key)
        
        combo_keys = tuple(normalized_keys)
        
        if combo_keys in self._combo_handlers and handler in self._combo_handlers[combo_keys]:
            self._combo_handlers[combo_keys].remove(handler)
            # 如果该组合键没有处理函数了，删除整个条目
            if not self._combo_handlers[combo_keys]:
                del self._combo_handlers[combo_keys]
    
    def is_key_pressed(self, key_name: str) -> bool:
        """检查按键是否被按下"""
        return self._normalize_key_name(key_name) in self._keys_pressed
    
    def is_combo_pressed(self, *keys: str) -> bool:
        """
        检查组合键是否被按下
        
        Args:
            *keys: 组合键的各个部分，如 'ctrl', 'c'
            
        Returns:
            bool: 如果所有键都按下且符合按键顺序则返回True
        """
        normalized_keys = []
        normalized_keys:List[str]
        for key in keys:
            norm_key = self._normalize_key_name(key.strip().lower())
            normalized_keys.append(norm_key)
        
        combo_keys = tuple(normalized_keys)
        pressed_keys = frozenset(self._keys_pressed)
        
        # 检查所有键是否都按下
        if not all(key in pressed_keys for key in combo_keys):
            return False
        
        # 检查按键顺序
        return self._check_combo_sequence(combo_keys)
    
    def get_all_pressed_keys(self) -> List[str]:
        """获取当前按下的所有键"""
        return list(self._keys_pressed)
    
    def get_key_char(self, key_name: str) -> Optional[str]:
        """获取键名对应的字符（不用于处理函数参数）"""   
        return self._key_char_map.get(key_name.lower())
    
    def get_last_key(self) -> Optional[str]:
        """获取最近按下的键"""
        if not self._combo_keys_buffer:
            return None
        return self._combo_keys_buffer[-1][0]
    
    def set_combo_max_interval(self, interval: float) -> None:
        """
        设置组合键的最大时间间隔
        
        Args:
            interval: 最大时间间隔（秒），默认0.5秒
        """
        if interval <= 0:
            raise ValueError("时间间隔必须大于0")
        self._combo_max_interval = interval
    
    def clear_combo_buffer(self) -> None:
        """清空组合键缓冲区"""
        self._combo_keys_buffer.clear()

# 全局实例
_keyboard_helper = KeyboardHelper()

# 便捷函数
def start_keyboard_helper() -> None:
    """启动键盘助手"""
    _keyboard_helper.start()

def stop_keyboard_helper() -> None:
    """停止键盘助手"""
    _keyboard_helper.stop()

def on_key_press(key_name: str, handler: Callable[[], Any]) -> None:
    """
    注册按键处理函数（普通键）
    
    Args:
        key_name: 按键名称，如 'a', 'space', 'plus' 等
        handler: 处理函数，不接受参数
    """
    _keyboard_helper.add_key_handler(key_name, handler)

def on_combo_press(*keys: str, handler: Callable[[], Any]) -> None:
    """
    注册组合键处理函数
    
    Args:
        *keys: 组合键的各个部分，如 'ctrl', 'c'
        handler: 处理函数，不接受参数
    """
    _keyboard_helper.add_combo_handler(*keys, handler=handler)

def is_key_pressed(key_name: str) -> bool:
    """检查按键是否被按下"""
    return _keyboard_helper.is_key_pressed(key_name)

def is_combo_pressed(*keys: str) -> bool:
    """检查组合键是否被按下"""
    return _keyboard_helper.is_combo_pressed(*keys)

def get_pressed_keys() -> List[str]:
    """获取当前按下的所有键"""
    return _keyboard_helper.get_all_pressed_keys()

def get_last_key() -> Optional[str]:
    """获取最近按下的键"""
    return _keyboard_helper.get_last_key()

def set_combo_max_interval(interval: float) -> None:
    """设置组合键的最大时间间隔"""
    _keyboard_helper.set_combo_max_interval(interval)

# 移除键处理函数
def remove_key_handler(key_name: str, handler: Callable[[], Any]) -> None:
    """移除按键处理函数"""
    _keyboard_helper.remove_key_handler(key_name, handler)

def remove_combo_handler(*keys: str, handler: Callable[[], Any]) -> None:
    """移除组合键处理函数"""
    _keyboard_helper.remove_combo_handler(*keys, handler=handler)