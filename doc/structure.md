**本文件为项目结构的记录**
``` ini
flowsheet/
    |-- README.md
    |-- .gitignore
    |-- main.py ; 程序入口
    |-- LICENSE
    |-- ATTRIBUTION.md
    |-- PURPOSE.md
    |-- .git/
    |   |-- ...
    |-- __pycache__/
    |   |-- ...
    |-- .venv/
    |   |-- ...
    |-- .vscode/
    |   |-- ...
    |-- .pytest_cache/
    |   |-- ...
    |-- logs/
    |   |-- ...
    |-- core/                  ; 核心游戏逻辑
    |   |-- __pycache__/
    |   |   |-- ...
    │   |-- __init__.py
    │   |-- app.py
    |-- stk/                    ; UI组件库
    |   |-- __pycache__/
    |   |   |-- ...
    │   |-- __init__.py
    │   |-- label.py
    │   |-- button.py
    |   |-- manu.py
    │   ; |-- widgets.py         ; 未来其他组件
    |-- config/                 ; 配置文件
    |   |-- __pycache__/
    |   |   |-- ...
    │   |-- __init__.py
    │   |-- settings.py
    |--tests/
    |   |-- __pycache__/
    |   |   |-- ...
    |   |-- __init__.py
    |   |-- test_stk.py
    |   |-- test_log.py
    |-- utils/                  ; 工具函数
    |   |-- __pycache__/
    |   |   |-- ...
    |   |-- __init__.py
    |   |-- log_write.py
    |   |-- keyboard_helper.py
    |   |-- event_decorators.py
    |-- doc/
    |   |-- structure.md
    |   |-- pyproject.toml
    |   |-- requirements.txt
    |   |-- requirements-test.txt
```