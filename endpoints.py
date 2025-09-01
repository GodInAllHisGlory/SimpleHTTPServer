from response import Response
from datetime import datetime

def index(req):
    response_body = open("template/index.html").read()
    return Response(req.version, 200, "OK", create_header(response_body), response_body)

def create_header(body):
    headers = {
        "Content-Type": "text/html",
        "Content-Length": get_length(body),
        "Connection": "close",
        "Cache-Control": "no-cache",
        "Server": "Really cool server",
        "Date": datetime.now().strftime("%c")
    }

def get_length(body):
    return len(body)