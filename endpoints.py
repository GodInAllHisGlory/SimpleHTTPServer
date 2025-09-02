from response import Response

def index(headers):
    response_body = open("template/index.html").read()
    headers = set_length(headers,response_body)
    headers = set_mime_type(headers)
    return Response("HTTP/1.1", 200, "Ok", headers, response_body)

def about(headers):
    response_body = open("template/about.html").read()
    headers = set_length(headers, response_body)
    headers = set_mime_type(headers)
    return Response("HTTP/1.1", 200, "Ok", headers, response_body)

def info(headers):
    msg = "Redirecting..."
    headers["Location"] = "/about"
    return Response("HTTP/1.1", 301, "Moved Permanently", headers, msg)

def not_found(headers):
    response_body = "404 File Not Found :("
    return Response("HTTP/1.1", 404, "Not Found", headers, response_body)

# def static(headers, body):
#     return Response("HTTP/1.1", 200, "Ok", headers, body)

def set_length(headers, body):
    headers["Content-Length"] = len(body)
    return headers

def set_mime_type(headers):
    headers["Content-Type"] = "text/html"
    return headers