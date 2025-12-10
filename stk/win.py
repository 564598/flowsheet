import pygame
from typing import Tuple, Dict, Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .button import Button
    from .manu import Manu
    from .label import Label

class Windows:
    """管理pygame窗口"""
    def __init__(
            self,
            mode:Tuple[int,int] = (1,1),
            title:str = "stk",
            checks:Dict[Any,Callable[[],Any]] = {}
        ) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(size=mode)
        pygame.display.set_caption(title=title)
        self.mode = mode
        self.title = title
        self.clock = pygame.time.Clock()
        self.checks:Dict[Any,Callable[[],Any]] = checks
    
    def get_mode(self) -> Tuple[int,int]:
        """返回窗口大小"""
        return self.mode
    
    def get_title(self) -> str:
        """返回窗口标题"""
        return self.title
    
    def get_checks(self) -> Dict[Any,Callable[[],Any]]:
        """返回已存在事件"""
        return self.checks
    
    def get_window(self) -> pygame.Surface:
        """返回窗口对象"""
        return self.screen
    
    def update_window(self,mode:Tuple[int,int]):
        """修改尺寸"""
        self.screen = pygame.display.set_mode(size=mode)

    def update_title(self,title:str):
        """修改标题"""
        pygame.display.set_caption(title=title)
    
    def add_checks(self,check:Any,func:Callable[[],Any]) -> None:
        """添加事件"""
        if check in self.checks.keys():
            raise TypeError("此键已存在，请用方法update_check")
        self.checks[check] = func

    def remove_checks(self,check:Any) -> None:
        """删除事件"""
        del self.checks[check]

    def update_check(self,check:Any,func:Callable[[],Any]) -> None:
        """修改事件"""
        self.checks[check] = func

    def stk_event(self, func:'list[Button|Manu|Label]'):
        """绑定组件们的检测"""
        self.stk_check = func
    
    def running(self) -> bool:
        """保持运行并检测"""
        for event in pygame.event.get():
            if event.type in list(self.checks.keys()):
                self.checks[event.type]
            if event.type == pygame.QUIT:
                return False
            for tk in self.stk_check:
                tk.check(event)
        self.clock.tick(60)
        return True

class Game:
    """pygame游戏基类"""
    def __init__(self) -> None:
        self.window = Windows()
        self.running = True
        self.color = (200,200,200)
        self.stks:'list[Button|Manu|Label]' = []
    
    def _draw(self) -> None:
        self.window.get_window().fill((200,200,200))
        for i in self.stks:
            i.draw()
        pygame.display.flip()
        
    def _exit(self) -> None:
        """退出程序"""
        self.running = False
    
    def _check(self) -> None:
        if self.window.running():
            pass
        else:
            self._exit()

    def run(self) -> None:
        while self.running:
            self._draw()
            self._check()
