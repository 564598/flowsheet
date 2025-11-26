import pygame
import sys
import colorama
import time
import os

from .app import App
from utils import log_error,log_info

def terminal_logs() -> None:
    """终端系统加日志系统"""
    if not os.path.exists("logs"):
        os.mkdir("logs")
    with open(f"logs/{time.strftime("%Y.%m.%d-%H.%M.%S")}.log",'a',encoding="utf-8") as log:
        print("此为Flow Sheet的执行终端窗口，请勿关闭，关闭则无法运行")
        log_info(log,"终端运行成功")
        try:
            colorama.init(autoreset=True)
            log_info(log,"colorama库加载成功")
        except:
            print("colorama初始化失败，将没有彩色提示")
            log_error(log,"colorama库加载失败")
            status = False
        else:
            status = True
        try:
            m = App(log=log)
            log_info(log,"实例创建成功")
            m.run()
            pygame.quit()
            log_info(log,"程序安全退出")
            sys.exit(0)
        except Exception as e:
            if status:
                print(colorama.Fore.RED + f"ERROR:{e}")
            else:
                print(f"ERROR:{e}")
            log_error(log,f"发生错误：{e}")
    sys.exit(0)