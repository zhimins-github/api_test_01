from setting import BASE_URL, LOGIN_INFO
import requests
from loguru import logger
from cacheout import Cache
cache = Cache()


class Base(object):

    #实现url的拼接
    def get_url(self, path, params=None):
       #返回一个完整的url
        if params:
            full_url = BASE_URL + path + params
            return full_url
        return BASE_URL + path

    #重写get方法
    def get(self, url):
        result = None
        response = requests.get(url, headers=self.get_headers())
        try:
            result = response.json()
            logger.success("请求url: {}, 返回结果：{}".format(url, result))
            return result
        except Exception as e:
            logger.error("请求get方法异常。返回数据为：{}".format(result))

    #重写post方法
    def post(self, url, data):
        result = None
        response = requests.post(url, json=data, headers=self.get_headers())
        try:
            result = response.json()
            logger.success("请求url: {},请求参数：{}， 返回结果：{}".format(url, data, result))
            return result
        except Exception as e:
            logger.error("请求post方法异常。返回数据为：{}".format(result))
    #实现所有头部信息的处理
    def get_headers(self):
        headers = {"Content-Type": "application/json"}
        token = cache.get("token")
        if token:
            headers.update({"X-Litemall-Admin-Token":token})
            return headers
        return headers

    #实现登录功能
    def login(self):
        login_path = "/admin/auth/login"
        login_url = self.get_url(login_path)
        result = self.post(login_url, LOGIN_INFO)
        try:
            if 0 == result.get("errno"):
                logger.info("请求登录接口成功")
                token = result.get("data").get("token")
                cache.set("token", token)
            else:
                logger.error("登录失败：{}".format(result))
                return None
        except Exception as e:
            logger.error("请求登录接口返回异常，异常数据{}".format(e))
            logger.error("报错信息：{}".format(e))
if __name__ == '__main__':
    base = Base()
    # print(base.get_url("/admin/admin/update"))
    # print(base.get_url("/admin/admin/list", "page=1&limit=20&sort=add_time&order=desc"))
    login_url = base.get_url("/admin/auth/login")
    # # print(login_url)
    login_data = {"username": "admin123", "password": "admin123"}
    print(base.post(login_url, login_data))
