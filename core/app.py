import pygame

from stk import Button

class App:
    """主程序管理"""
    def __init__(self) -> None:
        """初始化"""
        pygame.init()
        self.screen = pygame.display.set_mode((1000,1000))
        pygame.display.set_caption(title="flowsheet")
        self.clock = pygame.time.Clock()
        self.l = Button(self.screen,"exit",50,25,500,500,executed=self._exit)
        self.running = True

    def _exit(self) -> None:
        self.running = False
    
    def run(self) -> bool|None:
        """开始程序"""
        try:
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    self.l.check_event(event)
                
                self.screen.fill((200,200,200))
                self.l.draw()

                pygame.display.flip()
                self.clock.tick(100)
        except Exception as e:
            print(f"error:{e}")
            return