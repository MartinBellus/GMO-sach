from http import server

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-"

# check if string contains only allowed characters
def check_string_content(s: str):
    for i in s:
        if i not in ALPHABET:
            return False
    return True


ALLOWED_SUBADDRESSES = ["genome", "preset"]


class Handler(server.BaseHTTPRequestHandler):
    def _set_headers(self, code: int = 200):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # returns content of the file ./<query>/<req>, if it exists, otherwise returns 404
    def do_GET(self):
        try:
            path = self.path.split("/")
            print(path)

            query = path[-2]

            if query not in ALLOWED_SUBADDRESSES:
                print(f"UNKNOWN GET QUERY TYPE: {query}")
                return

            req = path[-1]
            if not check_string_content(req):
                self._set_headers(400)
                return

            try:
                with open(f"./{query}/{req}") as f:
                    self._set_headers()
                    self.wfile.write(f.read().encode("utf-8"))
                    return
            except:
                self._set_headers(404)
                return

        except Exception as e:
            print(e)

    # writes content to the file ./<query>/<req>
    # if the file already exists, does nothing
    def do_POST(self):
        try:

            path = self.path.split("/")

            query = path[-2]

            if query not in ALLOWED_SUBADDRESSES:
                self._set_headers(400)
                print(f"UNKNOWN POST QUERY TYPE: {query}")
                return

            length = int(self.headers["Content-Length"])

            req = path[-1]

            if length > 500:
                return

            text = self.rfile.read(length).decode()

            if not check_string_content(req) or not check_string_content(text):
                self._set_headers(400)
                return

            self._set_headers()
            filename =f"./{query}/{req}"
            try:
                f=open(filename, "r")
                f.close()
                return
            except:
                with open(filename, "w") as f:
                    f.write(text)

        except Exception as e:
            print(e)


try:
    server = server.HTTPServer(('localhost', 5000), Handler)
    print('Started server')
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()
