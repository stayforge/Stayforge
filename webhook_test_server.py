from http.server import SimpleHTTPRequestHandler, HTTPServer


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8085):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting http server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
