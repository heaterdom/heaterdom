import http.server  # Import http.server to serve the application
from socketserver import TCPServer  # Import socketserver for creating a server.
from rich.console import Console

console = Console()

# Serve function (Takes port as an argument)
def serve(PORT):
    # Get the directory (app)
    DIRECTORY = "app"

    # Handler class
    class Handler(http.server.SimpleHTTPRequestHandler):
        # Init method
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)

        # Custom 404 error if file not found
        def send_error(self, code, message=None):
            if code == 404:
                self.error_message_format = '<h1 style="text-align: center">404<h1/>'
                http.server.SimpleHTTPRequestHandler.send_error(self, code, message)

    # Tcp server starter with the PORT.
    with TCPServer(("", PORT), Handler) as httpd:
        # Print that it's serving and at witch port
        console.print(f"Serving at port {PORT}", style="blue")
        # Start server
        httpd.serve_forever()