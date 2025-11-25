import pygame
from typing import Callable,Any

from .label import Label

def kong():
    pass

class Button(Label):
    """按钮类"""
    def __init__(self, 
                 win: pygame.Surface, 
                 text: str, 
                 width: int, 
                 height: int, 
                 x: int, 
                 y: int, 
                 executed: Callable[[],Any] = kong,
                 border: int = 1, 
                 foreground: tuple[int, int, int] = (0,0,0), 
                 background: tuple[int, int, int] = (180,180,180), 
                 bordercolor: tuple[int, int, int] = (0,0,0), 
                 fontname: str | None = None, 
                 fontsize: int = 32
                ) -> None:
        super().__init__(win, text, width, height, x, y, border, foreground, background, bordercolor, fontname, fontsize)
        self.executed = executed

    def _is_collidepoint(self,pos: tuple[int,int]) -> bool:
        """检测是否碰撞"""
        return self.rect.collidepoint(pos)
    
    def check_event(self,event: pygame.event.Event):
        """执行按钮按下操作"""
        if event.type == pygame.MOUSEBUTTONDOWN and self._is_collidepoint(event.pos):
            self.executed()