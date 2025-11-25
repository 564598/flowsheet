"""label模块"""
import pygame

class Label:
    """文本显示框"""
    def __init__(self,
                 win: pygame.Surface, 
                 text: str,
                 width: int,
                 height: int,
                 x: int,
                 y: int,
                 border: int = 1,
                 foreground: tuple[int, int, int] = (0,0,0),
                 background: tuple[int, int, int] = (200,200,200),
                 bordercolor: tuple[int, int, int] = (0, 0, 0),
                 fontname: str|None = None,
                 fontsize: int = 32
                 ) -> None:
        """初始化各项参数"""
        self.win = win
        self.text = text
        self.foreground = foreground
        self.background = background
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.border = border
        self.bordercolor = bordercolor
        self.font = pygame.font.SysFont(fontname, fontsize)
        
        self.border_rect = pygame.Rect(x - border,  y - border, width + 2 * border, height + 2 * border)

    def draw(self):
        """绘制文本框"""
        if self.border > 0:
            pygame.draw.rect(self.win, color=self.bordercolor, rect=self.border_rect)
        
        pygame.draw.rect(
            self.win, 
            color=self.background, 
            rect=self.rect
        )

        text_surf = self.font.render(self.text, True, self.foreground)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.win.blit(text_surf, text_rect)
    
    def goto(self,position:tuple[int,int]) -> None:
        self.x = position[0]
        self.y = position[1]