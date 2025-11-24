import pygame
import sys

import stk

class Code:
    def __init__(self) -> None:
        """初始化"""
        pygame.init()
        self.screen = pygame.display.set_mode((1000,1000))
        pygame.display.set_caption(title="flowsheet")
        self.clock = pygame.time.Clock()
        self.l = stk.Label(self.screen,"hello",(0,0,0),(100,100,255),50,25,100,100,border=2)
    
    def run(self) -> int:
        """开始程序"""
        try:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 0
                
                self.screen.fill((200,200,200))
                self.l.draw()

                pygame.display.flip()
                self.clock.tick(100)
        except Exception:
            return 1


if __name__ == "__main__":
    m = Code()
    t = Code.run(m)
    print(t)
    pygame.quit()
    sys.exit(0)