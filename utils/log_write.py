import time
import _io

def log_info(file:_io.TextIOWrapper , info:str) -> None:
    file.write(f"[{time.strftime("%Y.%m.%d-%H.%M.%S")}] [INFO] {info}\n")

def log_error(file:_io.TextIOWrapper , error:str) -> None:
    file.write(f"[{time.strftime("%Y.%m.%d-%H.%M.%S")}] [INFO] {error}\n")