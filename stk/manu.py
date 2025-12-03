import pygame
from typing import Any,Callable
from .button import Button,kong

class Manu:
    def __init__(self,
                 win:pygame.Surface,
                 height: int, 
                 button_num:int,
                 button_text:list[str],
                 button_width:int = 20,
                 executeds: list[Callable[[], Any]] = [kong],
                 border: int = 2,
                 foreground: tuple[int, int, int] = (0, 0, 0), 
                 background: tuple[int, int, int] = (180, 180, 180), 
                 hover_background: tuple[int, int, int] = (160, 160, 160),
                 press_background: tuple[int, int, int] = (140, 140, 140),
                 bordercolor: tuple[int, int, int] = (0, 0, 0),
                 fontname: str = "Arial", 
                 fontsize: int = 32
                ) -> None:
        if button_num != len(button_text) or button_num != len(executeds):
            raise TypeError("传入参数不一致")
        self.win = win
        self.height = height
        self.button_num = button_num
        self.button_text = button_text
        self.button_width = button_width
        self.executeds = executeds
        self.border = border
        self.foreground = foreground
        self.background = background
        self.hover_backgroud = hover_background
        self.press_backgroud = press_background
        self.bordercolor = bordercolor
        self.fontname = fontname
        self.fontsize = fontsize

        self.font = pygame.font.SysFont(fontname, fontsize)
        self.buttons = []
        self.buttons:list[Button]
        for i in range(self.button_num):
            b = Button(win,
                        button_text[i],
                        width = self.button_width,
                        height = self.height,
                        x = i*self.button_width,
                        y = 0,
                        executed= self.executeds[i],
                        border = self.border,
                        foreground = self.foreground, 
                        background = self.background, 
                        hover_background=self.hover_backgroud,
                        press_background = self.press_backgroud,
                        bordercolor = self.bordercolor,
                        fontname = self.fontname, 
                        fontsize = self.fontsize
                        )
            self.buttons.append(b)
        
    def draw(self):
        pygame.draw.rect(
            self.win,
            self.background,
            pygame.Rect(
                0,
                0,
                self.win.get_size()[0],
                self.height
                )
            )
        for b in self.buttons:
            b.draw()

    def check(self,event:pygame.event.Event):
        for b in self.buttons:
            b.check_event(event=event)