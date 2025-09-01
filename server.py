import socket
from request import Request
from response import Response
from endpoints import index

# endpoint_dict = {
#     "/":index,
#     "index":index,
#     "/info":about,
#     "/about":about
# }

#Logs important request and response information
def logging_factory(next):
    def logging(protocol): 
        print(protocol.method)
        print(protocol.uri)
        return next(protocol.uri)
        
    return logging

def get_static_file_factory(next):
    def get_static_file(uri):
        
        return next(file)
    
    return get_static_file

def decoder(data):
    request_parts = data.decode("UTF-8").split("\n")
    request_line = request_parts.pop(0).split()
    body = request_parts.pop()
    headers = dict()

    request_parts.pop() #Gets rid of the last element which is just a empty string
    for header in request_parts:
        header_parts = header.split(": ")
        headers[header_parts[0]] = header_parts[1]
        print(header)
    request = Request(
        request_line[0],
        request_line[1],
        request_line[2],
        body,
        headers
    )
    return request

def encoder():
    response = Response()
    return response

def router(req):
    response = endpoint_dict[req.uri]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 8000))
    s.listen()
    print("listening on port 8000")

    while True:
        connection, addr = s.accept()
        with connection:
            data = connection.recv(8192)
            if not data:
                connection.close()
                continue
            #TODO: parse the request, send through middleware and encode the response
            request = decoder(data)
            # middleware_chain = logging_factory()
            res = "HTTP/1.1 200 Ok\nConnection: close\n\n<h1>Hello, world!</h1>"
            connection.send(bytes(res, "UTF-8"))

