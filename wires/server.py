import time
import http.server

class RequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        page = '''<html><head><title>Wires Test</title></head>
        <body><p>The server is up!</p>
        <p>You accessed path: {0}</p>
        </body></html>'''.format(s.path)
        s.wfile.write(bytes(page, 'UTF-8'))

if __name__ == '__main__':
    server = http.server.HTTPServer(("localhost", 8080), RequestHandler)
    print(time.asctime(), "Wires Server Start!")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print(time.asctime(), "Wires Server Stop")