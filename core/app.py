import pygame

from stk import Button
from utils import LogSystem

class App:
    """主程序管理"""
    def __init__(self , log:LogSystem) -> None:
        """初始化"""
        self.log = log
        pygame.init()
        self.screen = pygame.display.set_mode((1000,1000))
        pygame.display.set_caption(title="flowsheet")
        self.clock = pygame.time.Clock()
        self.log.log_info("pygame初始化成功")
        self.l = Button(self.screen,"exit",50,25,500,500,executed=self._exit)
        self.running = True

    def _exit(self) -> None:
        self.running = False
    
    def run(self) -> None:
        """开始程序"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self._exit()
                self.l.check_event(event)
            
            self.screen.fill((200,200,200))
            self.l.draw()

            pygame.display.flip()
            self.clock.tick(100)