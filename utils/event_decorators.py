"""
事件装饰器系统 - 统一的按钮和键盘事件装饰器
支持自动日志记录、事件绑定、参数传递
"""

import functools
from typing import Callable, Any, Dict, Optional, List

# 全局事件注册表
_event_registry: Dict[str, Dict[str, Dict[str, Any]]] = {
    'button': {},      # 按钮事件注册表
    'key': {},         # 单键事件注册表
    'combo': {},       # 组合键事件注册表
    'mouse': {},       # 鼠标事件注册表
    'custom': {}       # 自定义事件注册表
}

# 用于存储事件处理器实例的全局变量
_event_handlers: Dict[str, Any] = {
    'buttons': {},     # 按钮实例
    'keyboard': None,  # 键盘助手实例
    'log': None,       # 日志系统实例
    'app': None        # 应用实例
}

# 菜单注册表
_menu_registry: Dict[str, Dict[int, Any]] = {}


def register_event_handler(type_name: str, handler: Any, name: Optional[str] = None) -> None:
    """注册事件处理器"""
    if type_name == 'button':
        if name is None:
            raise ValueError("按钮处理器必须指定名称")
        _event_handlers['buttons'][name] = handler
    elif type_name == 'keyboard':
        _event_handlers['keyboard'] = handler
    elif type_name == 'log':
        _event_handlers['log'] = handler
    elif type_name == 'app':
        _event_handlers['app'] = handler


def register_menu(menu_name: str) -> None:
    """注册菜单实例"""
    if menu_name not in _menu_registry:
        _menu_registry[menu_name] = {}


def register_menu_button(menu_name: str, button_index: int, button_instance: Any) -> None:
    """注册菜单中的按钮"""
    if menu_name not in _menu_registry:
        _menu_registry[menu_name] = {}
    _menu_registry[menu_name][button_index] = button_instance
    
    # 为这个按钮创建一个唯一的ID，并注册到按钮注册表
    button_id = f"{menu_name}_{button_index}"
    _event_handlers['buttons'][button_id] = button_instance
    
    # 检查是否有已注册的事件需要绑定到这个按钮
    if button_id in _event_registry['button']:
        event_info = _event_registry['button'][button_id]
        original_func = event_info['original']
        decorator = event_info['decorator']
        app_instance = _event_handlers['app']
        
        button_instance.executed = lambda: decorator._execute_with_context(
            original_func, app_instance
        )


class EventDecorator:
    """事件装饰器基类"""
    
    def __init__(self, log_message: Optional[str] = None, 
                 event_type: str = 'custom',
                 target: Optional[str] = None) -> None:
        """
        初始化事件装饰器
        
        Args:
            log_message: 日志消息，支持格式化字符串
            event_type: 事件类型 ('button', 'key', 'combo', 'mouse', 'custom')
            target: 目标标识符（按钮名称、按键名称等）
        """
        self.log_message = log_message
        self.event_type = event_type
        self.target = target
        
    def _log_event(self, func_name: str, *args: Any, **kwargs: Any) -> None:
        """记录事件日志"""
        if _event_handlers['log'] and self.log_message:
            log_system = _event_handlers['log']
            try:
                # 构建日志上下文
                context: Dict[str, Any] = {
                    'func_name': func_name,
                    'args': args,
                    'kwargs': kwargs,
                    'target': self.target,
                    'event_type': self.event_type
                }
                
                # 格式化日志消息
                log_msg: Any = self.log_message
                if callable(log_msg):
                    log_msg = log_msg(*args, **kwargs)
                elif isinstance(log_msg, str):
                    log_msg = log_msg.format(**context)
                    
                log_system.log_info(log_msg)
            except Exception:
                # 如果格式化失败，使用默认消息
                default_msg = f"{self.event_type}事件触发: {func_name}"
                log_system.log_info(default_msg)
    
    def _execute_with_context(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """在上下文中执行函数"""
        # 记录日志
        self._log_event(func.__name__, *args, **kwargs)
        
        # 执行原始函数
        return func(*args, **kwargs)
    
    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """装饰器调用 - 返回原始函数，只注册事件"""
        # 注册事件
        self._register_event(func, func)
        
        # 返回原始函数，不包装
        return func
    
    def _register_event(self, original_func: Callable[..., Any], wrapped_func: Callable[..., Any]) -> None:
        """注册事件到全局注册表"""
        key = self._get_registry_key()
        if key:
            _event_registry[self.event_type][key] = {
                'original': original_func,
                'decorator': self
            }
    
    def _get_registry_key(self) -> Optional[str]:
        """获取注册表键"""
        return self.target


class ButtonEvent(EventDecorator):
    """按钮事件装饰器"""
    
    def __init__(self, button_name: str, log_message: Optional[str] = None, **kwargs: Any) -> None:
        """
        初始化按钮事件装饰器
        
        Args:
            button_name: 按钮名称标识符
            log_message: 日志消息
            **kwargs: 传递给基类的其他参数
        """
        log_msg = log_message or f"按钮 '{button_name}' 被点击"
        super().__init__(
            log_message=log_msg,
            event_type='button',
            target=button_name,
            **kwargs
        )
        
    def _register_event(self, original_func: Callable[..., Any], wrapped_func: Callable[..., Any]) -> None:
        super()._register_event(original_func, wrapped_func)
        
        # 立即绑定到按钮（如果按钮已注册）
        if self.target and self.target in _event_handlers['buttons']:
            button = _event_handlers['buttons'][self.target]
            app_instance = _event_handlers['app']
            # 绑定到按钮的executed回调
            button.executed = lambda: self._execute_with_context(original_func, app_instance)


class MenuButtonEvent(ButtonEvent):
    """菜单按钮事件装饰器"""
    
    def __init__(self, menu_name: str, button_index: int, log_message: Optional[str] = None, **kwargs: Any) -> None:
        """
        初始化菜单按钮事件装饰器
        
        Args:
            menu_name: 菜单名称
            button_index: 按钮在菜单中的索引
            log_message: 日志消息
            **kwargs: 传递给基类的其他参数
        """
        # 生成唯一的按钮ID
        button_id = f"{menu_name}_{button_index}"
        log_msg = log_message or f"菜单 '{menu_name}' 的第 {button_index} 个按钮被点击"
        
        super().__init__(
            button_name=button_id,
            log_message=log_msg,
            **kwargs
        )
        self.menu_name = menu_name
        self.button_index = button_index


class KeyEvent(EventDecorator):
    """键盘事件装饰器"""
    
    def __init__(self, key_name: str, log_message: Optional[str] = None, 
                 is_combo: bool = False, **kwargs: Any) -> None:
        """
        初始化键盘事件装饰器
        
        Args:
            key_name: 按键名称（或组合键，用'+'分隔）
            log_message: 日志消息
            is_combo: 是否为组合键
            **kwargs: 传递给基类的其他参数
        """
        log_msg = log_message or f"按键 '{key_name}' 被按下"
        event_type = 'combo' if is_combo else 'key'
        
        super().__init__(
            log_message=log_msg,
            event_type=event_type,
            target=key_name,
            **kwargs
        )
        self.is_combo = is_combo


# 事件系统管理器
class EventSystem:
    """事件系统管理器"""
    
    @staticmethod
    def bind_app(app_instance: Any) -> None:
        """绑定应用实例"""
        _event_handlers['app'] = app_instance
        
    @staticmethod
    def bind_log(log_system: Any) -> None:
        """绑定日志系统"""
        _event_handlers['log'] = log_system
        
    @staticmethod
    def bind_keyboard(keyboard_helper: Any) -> None:
        """绑定键盘助手"""
        _event_handlers['keyboard'] = keyboard_helper
        
    @staticmethod
    def register_button(button_name: str, button_instance: Any) -> None:
        """注册按钮实例"""
        _event_handlers['buttons'][button_name] = button_instance
        
        # 自动绑定已注册的按钮事件
        if button_name in _event_registry['button']:
            event_info = _event_registry['button'][button_name]
            original_func = event_info['original']
            decorator = event_info['decorator']
            app_instance = _event_handlers['app']
            
            button_instance.executed = lambda: decorator._execute_with_context(
                original_func, app_instance
            )
    
    @staticmethod
    def register_menu(menu_name: str) -> None:
        """注册菜单实例（只注册菜单名，不注册按钮）"""
        register_menu(menu_name)
    
    @staticmethod
    def register_menu_buttons(menu_name: str, buttons: List[Any]) -> None:
        """注册菜单中的所有按钮"""
        register_menu(menu_name)
        for i, button in enumerate(buttons):
            register_menu_button(menu_name, i, button)
    
    @staticmethod
    def bind_all(app_instance: Any, log_system: Any, keyboard_helper: Any, 
                 buttons: Optional[Dict[str, Any]] = None,
                 menus: Optional[Dict[str, List[Any]]] = None) -> None:
        """一键绑定所有处理器"""
        EventSystem.bind_app(app_instance)
        EventSystem.bind_log(log_system)
        EventSystem.bind_keyboard(keyboard_helper)
        
        if buttons:
            for name, button in buttons.items():
                EventSystem.register_button(name, button)
        
        if menus:
            for menu_name, menu_buttons in menus.items():
                EventSystem.register_menu_buttons(menu_name, menu_buttons)
    
    @staticmethod
    def get_registered_events() -> Dict[str, Dict[str, Dict[str, Any]]]:
        """获取所有已注册的事件"""
        return _event_registry
    
    @staticmethod
    def clear_registry() -> None:
        """清空事件注册表"""
        for event_type in _event_registry:
            _event_registry[event_type].clear()


# 便捷装饰器函数
def on_button(button_name: str, log_message: Optional[str] = None) -> ButtonEvent:
    """按钮事件装饰器工厂函数"""
    return ButtonEvent(button_name, log_message)


def on_menu_button(menu_name: str, button_index: int, log_message: Optional[str] = None) -> MenuButtonEvent:
    """菜单按钮事件装饰器工厂函数"""
    return MenuButtonEvent(menu_name, button_index, log_message)


def on_key(key_name: str, log_message: Optional[str] = None) -> 'KeyEvent':
    """键盘事件装饰器工厂函数"""
    is_combo = '+' in key_name
    return KeyEvent(key_name, log_message, is_combo=is_combo)


def on_combo(*keys: str, log_message: Optional[str] = None) -> KeyEvent:
    """组合键事件装饰器工厂函数"""
    key_name = '+'.join(keys)
    return KeyEvent(key_name, log_message, is_combo=True)


# 高级装饰器
def with_context(**context_kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """为事件处理函数添加上下文参数"""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            new_kwargs = kwargs.copy()
            new_kwargs.update(context_kwargs)
            
            for key, value in context_kwargs.items():
                if callable(value):
                    new_kwargs[key] = value()
            
            return func(*args, **new_kwargs)
        return wrapper
    return decorator


def when(condition_func: Callable[[], bool]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """条件执行装饰器"""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if condition_func():
                return func(*args, **kwargs)
            return None
        return wrapper
    return decorator


def retry_on_event(max_retries: int = 3, delay: float = 0.1) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """事件重试装饰器"""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            import time
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    log_system = _event_handlers['log']
                    if log_system:
                        log_system.log_info(f"事件处理失败，第{attempt+1}次重试: {str(e)}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator