from http import server


class Handler(server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        try:
            self._set_headers()
            path = self.path.split("/")[-1]
            print(path)
            
            if not path.isalnum():
                return

            try:
                with open(f"./data/{path}") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            except:
                self.wfile.write(b"GENOME HASH NOT FOUND!!!")
        except:
            pass

    def do_POST(self):
        try:
            self._set_headers()

            path = self.path.split("/")[-1]

            length = int(self.headers["Content-Length"])
            
            if length>500:
                return

            text = self.rfile.read(length).decode()
            
            if not path.isalnum() or not text.isalnum():
                return

            print(text, path)

            with open(f"./data/{path}", "w") as f:
                f.write(text)

            print(text, path)
        except:
            pass


try:
    server = server.HTTPServer(('localhost', 5000), Handler)
    print('Started server')
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()
