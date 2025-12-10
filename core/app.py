import pygame
import stk
import utils

class App(stk.Game):
    """主程序管理"""
    def __init__(self , log:utils.LogSystem) -> None:
        """初始化应用"""
        self.log = log
        super().__init__()
        self.window.update_window((1000,1000))
        self.window.update_title(title="flowsheet")
        self.window.add_checks(pygame.QUIT,self._exit)
        self.log.log_info("pygame及应用属性初始化成功")
        self._keyboard_init()
        self._stk_init()
        self._eventsystem_init()

    def _keyboard_init(self) -> None:
        """初始化KeyboardHelper"""
        self.keyer = utils.KeyboardHelper()
        self.keyer.start()
        self.keyer.add_combo_handler('ctrl','q',handler=self._exit)
        self.log.log_info("keyboardHelper初始化成功")

    def _eventsystem_init(self) -> None:
        """初始化装饰器系统"""
        utils.EventSystem.bind_app(self)
        utils.EventSystem.bind_keyboard(self.keyer)
        utils.EventSystem.bind_log(self.log)
        utils.EventSystem.register_button('l',self.l)
        utils.EventSystem.register_menu_buttons('manu',self.menu.buttons)
        self.log.log_info("装饰器系统绑定成功")

    def _stk_init(self) -> None:
        """初始化各项组件"""
        self.l = stk.Button(
            self.window,
            "exit",
            50,
            30,
            500,
            500,
            annotation='exit'
        )
        self.menu = stk.Manu(
            win=self.window,
            height=50,
            button_num=2,
            button_text=["文件", "退出"],
            button_width=100,
            fontname="Microsoft YaHei",
            fontsize=20,
            annotations=['file(Ctrl+F)','exit(Ctrl+Q)']
        )
        self.log.log_info("stk组件初始化成功")
        self.stks = [self.l,self.menu]
        self.window.stk_event(self.stks)

    def run(self) -> None:
        """开始程序"""
        super().run()
        self._exit()
    
    @utils.on_button('l',"按下按钮“exit”")
    @utils.on_combo('ctrl','q',log_message="按下Ctrl+Q键")
    @utils.on_menu_button('manu',1,"按下按钮“退出”")
    def _exit(self) -> None:
        """退出程序"""
        self.running = False
        self.keyer.stop()

    # def _draw(self) -> None:
    #     """绘制屏幕"""
    #     self.l.draw()
    #     self.menu.draw()
    #     super()._draw()

    # def _check(self) -> None:
    #     """检测事件"""
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             self._exit()
    #         self.l.check(event)
    #         self.menu.check(event)