

class BaseResponse(object):
    def __init__(self):
        self.code = 1000  # 登录成功的状态码
        self.error = ""  # 登录失败的提示
        self.data = ""  # 登录成功的提示

    @property
    def dict(self):  # 将上面的数据组成字典返回
        return self.__dict__