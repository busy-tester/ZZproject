from django.utils.deprecation import MiddlewareMixin


class MyCors(MiddlewareMixin):
    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = "*"
        if request.method == "OPTIONS":
            # 复杂请求会先发预检
            response["Access-Control-Allow-Headers"] = "Content-Type, AUTHENTICATE"
            # 对其他方法的请求也不做拦截
            response["Access-Control-Allow-Methods"] = "DELETE, PUT, POST"
        return response
