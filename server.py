import socket
from datetime import datetime
from request import Request
from response import Response
from endpoints import index, about, info, not_found, experience, projects

endpoint_dict = {
    "/":index,
    "/index":index,
    "/info":info,
    "/about":about,
    "/experience":experience,
    "/projects":projects
}

#Logs important request and response information
def logging_factory(next):
    def logging(req):  
        print("Request Received:")
        print(req.method)
        print(req.uri)

        res = next(req)
        print("Response Sent:")
        print(res.code)
        print(res.reason)
        return res
        
    return logging

#Creates the headers for a response object
def create_headers_factory(next):
    def create_headers(req):
        headers = {
        "Connection": "close",
        "Cache-Control": "max-age=20",
        "Server": "Really Cool Server",
        "Date": datetime.now().strftime('%c')
    }
        return next(req, headers)
    return create_headers

#Gets files that are specifically requested
def get_static_file_factory(next):
    def get_static_file(req, headers):
        uri = req.uri
        if "." in uri:
            try:
                headers = static_response_helper(headers, uri)
                file = open(f"static/{uri}").read()
                return Response("HTTP/1.1", 200, "Ok", headers, file)
            except FileNotFoundError:
                return next(req, headers)
            
        return next(req, headers)
    return get_static_file

#Just helps the get_static_file function get the correct header
def static_response_helper(header, uri):
    static_type = uri.split(".")[1] #Gets the file type
    if static_type == "css":
        content = "text/css"
    elif static_type == "js":
        content = "text/javascript"
    else:
        content = None
    header["Content-Type"] = content
    return header

#Turns a http request object into a more manageable request object
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

#Turns a response object into a proper http response
def encoder(res):
    headers = res.headers
    response = f"{res.version} {res.code} {res.reason}"

    for header in headers.keys():
        response += f"\n{header}: {headers[header]}"
    response += "\n\n"
    response += res.body

    return response

def router(req, headers):
    try:
        response = endpoint_dict[req.uri](headers) #Access a dict that holds the proper endpoint info
    except KeyError:
        response = not_found(headers)
    return response

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

            request = decoder(data) 
            response_chain = get_static_file_factory(router)
            response_chain = create_headers_factory(response_chain)
            response_chain = logging_factory(response_chain)
            res = response_chain(request) #Returns a response object
            res = encoder(res)

            # log_chain = logging_factory(encoder)
            # res = log_chain(res)
            connection.send(bytes(res, "UTF-8"))

