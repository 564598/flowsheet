import pygame

class Label:
    def __init__(self,
                 win: pygame.Surface, 
                 text: str,
                 foreground: tuple[int, int, int],
                 background: tuple[int, int, int],
                 width: int,
                 height: int,
                 x: int,
                 y: int,
                 border: int = 1,
                 bordercolor: tuple[int, int, int] = (0, 0, 0)
                 ) -> None:
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
        self.font = pygame.font.SysFont(None, 32)
        
        self.border_rect = pygame.Rect(x - border,  y - border, width + 2 * border, height + 2 * border)

    def draw(self):
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