# Imports
from os import system # Import os for system commands. This is needed to compile sass 
from os.path import exists
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

class IsSass(Exception):
    pass

class IsGlobal(Exception):
    pass


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
            sleep(1)
            try:
                out = f"\nCompiled {child} to html\n"
                console.print(out, style="green")
                sleep(1)
                with open(child, 'rt') as f:
                    rendered = markdown(f.read())
                    filename = PurePath(child)
                    filename_no_ext = filename.stem
                    with open(f'app/{filename_no_ext}.html', "wt") as f:
                        f.write(f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{filename_no_ext}</title>
    </head>
    <body>   
                    """)
                    css = ''
                    if exists("./styles"):
                        with open(f'app/{filename_no_ext}.html', "at") as f:
                            f.write("""
        <style>
                            """)
                        for childCSS in Path('./styles').iterdir():
                            css = ''
                            if childCSS.is_file():
                                filenameCss = PurePath(child)
                                filenameCss_no_ext = filenameCss.stem
                                fullFileNameCss = PurePath(childCSS)
                                system('sass --no-source-map styles/:styles/')
                                try:
                                    if fullFileNameCss.suffix == '.sass' or fullFileNameCss.suffix == '.scss':
                                        raise IsSass()
                                    elif fullFileNameCss.stem == '*':
                                        with open('styles/*.css', "rt") as f:
                                            css = f.read()
                                        raise IsGlobal()
                                    else:
                                        with open(f'styles/{filenameCss_no_ext}.css', "rt") as f:
                                            css = f.read()
                                        console.print(f'\nCss {childCSS} injected into {filename_no_ext}.html', style="green")
                                except FileNotFoundError:
                                    console.print(f'\nNo css to inject in {filename_no_ext}.html', style="red")
                                except IsSass:
                                    console.print(f'\nFound sass, skipping', style="blue")
                                except IsGlobal:
                                    console.print('Found global styles. Injecting', style='green')
                                with open(f'app/{filename_no_ext}.html', "at") as f:
                                    f.write(f'''
{css}
                                            ''')
                        sleep(1)            
                    else:
                        console.print('No styles directory, skipping', style="blue") 
                    with open(f'app/{filename_no_ext}.html', "at") as f:
                        f.write("""
        </style>                        
                        """)

                    with open(f'app/{filename_no_ext}.html', "at") as f:
                        f.write(f"""
        { rendered }
                        """)
                    with open(f'app/{filename_no_ext}.html', "at") as f:
                        f.write('''
    </body>
</html>
                        ''')
            except:
                out = f'\nFailed to compile {child} to html'
                console.print(out, style="red") 
                sleep(1)
            
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