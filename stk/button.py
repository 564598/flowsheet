import pygame
from typing import Callable, Any

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
                 executed: Callable[[], Any] = kong,
                 annotation: str|None = None,
                 border: int = 2,
                 foreground: tuple[int, int, int] = (0, 0, 0), 
                 background: tuple[int, int, int] = (180, 180, 180), 
                 hover_background: tuple[int, int, int] = (160, 160, 160),
                 press_background: tuple[int, int, int] = (140, 140, 140),
                 bordercolor: tuple[int, int, int] = (0, 0, 0),
                 fontname: str = "Arial", 
                 fontsize: int = 32
                ) -> None:
        super().__init__(win, 
                         text, 
                         width, 
                         height, 
                         x, 
                         y, 
                         border, 
                         foreground, 
                         background, 
                         bordercolor, 
                         fontname, 
                         fontsize
                        )
        self.executed = executed
        self.hover_background = hover_background
        self.press_background = press_background
        self.original_background = background
        self.is_hovered = False
        self.is_pressed = False
        self.original_border = border
        self.annotation = annotation
        self.fontsize = fontsize
        self.fontname = fontname
        self.time = 0
        
    def _collidepoint(self, pos: tuple[int, int]) -> bool:
        """检测是否碰撞"""
        return self.rect.collidepoint(pos)
    
    def check_event(self, event: pygame.event.Event) -> None:
        """处理按钮事件"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self._collidepoint(event.pos)
            self.pos = event.pos
            if self.is_hovered and self.annotation:
                self.label = Label(
                    self.win,
                    self.annotation,
                    len(self.annotation) * 8,
                    16, 
                    self.pos[0], 
                    self.pos[1],
                    background=(255,255,245),
                    bordercolor=(150,150,150),
                    fontname=self.fontname,
                    fontsize=16
                )
                self.time += 1
            else:
                self.time = 0
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._collidepoint(event.pos):
                self.is_pressed = True
                self.border = self.original_border + 2  
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self._collidepoint(event.pos):
                self.executed()
            self.is_pressed = False
            self.border = self.original_border
    
    def draw(self) -> None:
        """绘制按钮"""
        if self.is_pressed:
            current_bg = self.press_background
        elif self.is_hovered:
            current_bg = self.hover_background
        else:
            current_bg = self.original_background
        
        self.background = current_bg
        self.border_rect = pygame.Rect(
            self.x - self.border, 
            self.y - self.border, 
            self.width + 2 * self.border, 
            self.height + 2 * self.border
        )
        super().draw()

        if self.is_pressed:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 50))
            self.win.blit(overlay, (self.x, self.y))
        self.label_draw()

    def label_draw(self) -> None:
        """绘制标签"""
        if self.is_hovered and self.time >= 3:
            self.label.draw()