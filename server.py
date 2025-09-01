import socket
from request import Request
from response import Response
from endpoints import index, about

endpoint_dict = {
    "/":index,
    "index":index,
    "/info":about,
    "/about":about
}

#Logs important request and response information
def logging_factory(next):
    def logging(protocol): 
        print(protocol.method)
        print(protocol.uri)
        return next(protocol)
        
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
    request = Request(
        request_line[0],
        request_line[1],
        request_line[2],
        body,
        headers
    )
    return request

def encoder(res):
    headers = res.headers
    response = f"{res.version} {res.code} {res.reason}"
    for header in headers.keys():
        response += f"\n {header}: {headers[header]}"
    response += "\n\n"
    response += res.body
    return response

def router(req):
    try:
        response = endpoint_dict[req.uri](req)
    except KeyError:
        response = None
    return response

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 8001))
    s.listen()
    print("listening on port 8001")

    while True:
        connection, addr = s.accept()
        with connection:
            data = connection.recv(8192)
            if not data:
                connection.close()
                continue
            #TODO: parse the request, send through middleware and encode the response
            request = decoder(data)
            middleware_chain = logging_factory(router)
            res = middleware_chain(request) #Returns a response object
            res = encoder(res)
            # res = "HTTP/1.1 200 Ok\nConnection: close\n\n<h1>Hello, world!</h1>"
            connection.send(bytes(res, "UTF-8"))

