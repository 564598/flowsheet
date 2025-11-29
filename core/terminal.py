import pygame
import sys
import colorama
import time
import os

from .app import App
from utils import LogSystem

class Terminal:
    """终端系统加日志系统"""
    def __init__(self) -> None:
        self.logs_huan = 'logs文件夹已存在'
        if not os.path.exists("logs"):
            os.mkdir("logs")
            self.logs_huan = "logs文件夹不存在，已自动创建"
        self.log_file =  open(f"logs/{time.strftime("%Y.%m.%d-%H.%M.%S")}.log",'a',encoding="utf-8")
        self.log = LogSystem(self.log_file)
        self.log.log_info(self.logs_huan)
        try:
            colorama.init(autoreset=True)
            self.log.log_info("colorama库加载成功")
        except:
            print("colorama初始化失败，将没有彩色提示")
            self.log.log_error("colorama库加载失败")
            self.status = False
            self.Yellow = ''
        else:
            self.status = True
            self.Yellow = colorama.Fore.YELLOW
    
    def terminal_logs(self) -> None:
        print(self.Yellow + "此为Flow Sheet的执行终端窗口，请勿关闭，关闭则无法运行")
        self.log.log_info("终端运行成功")
        try:
            m = App(self.log)
            self.log.log_info("实例创建成功")
            m.run()
            pygame.quit()
            self.log.log_info("程序安全退出")
            sys.exit(0)
        except Exception as e:
            if self.status:
                print(colorama.Fore.RED + f"ERROR:{e}")
            else:
                print(f"ERROR:{e}")
            self.log.log_error(f"发生错误：{e}")
        sys.exit(0)