from utils import LogSystem

def test_info() -> None:
    test = open("logs/test.log",'w')
    testlog = LogSystem(test)
    testlog.log_info("test")
    test.close()
    del testlog
    test = open("logs/test.log",'r')
    assert test.read()[-5:].strip() == 'test'