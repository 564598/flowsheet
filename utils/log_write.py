import time
import _io

class LogSystem:
    def __init__(self , file:_io.TextIOWrapper) -> None:
        self.file = file

    def log_info(self,info:str) -> None:
        self.file.write(f"[{time.strftime("%Y.%m.%d-%H.%M.%S")}] [INFO] {info}\n")
    def log_error(self,error:str) -> None:
        self.file.write(f"[{time.strftime("%Y.%m.%d-%H.%M.%S")}] [ERROR] {error}\n")