import pygame

from stk import Button
from utils import LogSystem,KeyboardHelper

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
        self.keyer = KeyboardHelper()
        self.keyer.start()
        self.keyer.add_key_handler('q', self._on_q_press)
        self.log.log_info("keyboardHelper初始化成功")
        self.l = Button(self.screen,"exit",50,30,500,500,executed=self._button_l_down)
        self.running = True

    def _exit(self) -> None:
        """退出程序"""
        self.running = False
        self.keyer.stop()

    def _on_q_press(self, char: str) -> None:
        """Q键按下时的处理"""
        self.log.log_info("按下Q键")
        self._exit()
    
    def _button_l_down(self):
        self.log.log_info("按下按钮“exit”")
        self._exit()

    def _draw(self) -> None:
        """绘制屏幕"""
        self.screen.fill((200,200,200))
        self.l.draw()
        pygame.display.flip()

    def _check(self) -> None:
        """检测事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit()
            self.l.check_event(event)

    def run(self) -> None:
        """开始程序"""
        while self.running:
            self._draw()
            self._check()
            self.clock.tick(100)