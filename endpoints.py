from response import Response
from datetime import datetime

def index(req):
    response_body = open("template/index.html").read()
    return Response(req.version, 200, "Ok", create_headers(response_body), response_body)

def about(req):
    response_body = open("template/index.html").read()
    return Response(req.version, 200, "Ok", create_headers(response_body), response_body)

def create_headers(body):
    headers = {
        "Content-Type": "text/html",
        "Content-Length": get_length(body),
        "Connection": "close",
        "Cache-Control": "no-cache",
        "Server": "Really cool server",
        "Date": datetime.now().strftime("%c")
    }
    return headers

def get_length(body):
    return len(body)