# Import 
from sys import argv
from time import sleep
from rich.console import Console
from rich.markdown import Markdown
from pathlib import Path, PurePath
from mistletoe import markdown
import http.server
from socketserver import TCPServer

VERSION = "0.1.0"

# Create rich console
console = Console()

def help():
    helpMsg = f"""
python3 main.py [command] [options]

Commands:
    compile: compiles markdown in the content dir into html in the app dir
    serve: servers the app dir [--port: specify the port]

    heatherdom v{VERSION}. Located at {__file__} 
    """
    print(helpMsg)

def compile():
    for child in Path('./content').iterdir():
        if child.is_file():
            md = Markdown(f"# {child}")
            console.print(md)
            try:
                out = f"\nCompiled {child} to html\n"
                with open(child, 'rt') as f:
                    rendered = markdown(f.read())
                    filename = PurePath(child)
                    filename_no_ext = filename.stem
                    with open(f'app/{filename_no_ext}.html', "wt") as f:
                        f.write(rendered)
                sleep(1)
            except:
                out = f'\nFailed to compile {child} to html'
                sleep(1)
            if out == f'\nFailed to compile {child} to html':
                console.print(out, style="red") 
            else:
                console.print(out, style="green")
        else:
            console.print(f'{child} is a directory', style="red")


def serve(PORT):
    DIRECTORY = "app"
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)
        def send_error(self, code, message=None):
            if code == 404:
                self.error_message_format = "<h1 style='text-align: center'>404<h1/>"
                http.server.SimpleHTTPRequestHandler.send_error(self, code, message)

    with TCPServer(("", PORT), Handler) as httpd:
        console.print(f"Serving at port {PORT}", style="blue")
        httpd.serve_forever()

try: 
    if argv[1] == "compile":
        compile()
    elif argv[1] == "serve":
        if argv[2] == "--port":
            serve(int(argv[3]))
        elif len(argv) != 2:
            console.print('Error! Extra arguments passed\n', style="red")
            help()
        else:
            serve(3000)

    elif argv[1] == "--help":
        help()
    else:
        help()
except IndexError:
    help()
except KeyboardInterrupt:
    pass