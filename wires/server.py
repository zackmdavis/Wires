import time
import http.server

def run_server(domain, port, request_handler):
    server = http.server.HTTPServer((domain, port), request_handler)
    print(time.asctime(), "Wires Server Start!")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print(time.asctime(), "Wires Server Stop")
