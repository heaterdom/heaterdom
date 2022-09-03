#!/usr/bin/env python3

# Standard Library Imports
from os import system  # Import os for system commands. This is needed to compile sass
from os.path import exists  # Import exists from path to check if styles exists
from sys import argv  # Import argv for arguments
from time import sleep  # Import time to slow down a bit
from pathlib import Path, PurePath  # Import Path for iterating in directory and PurePath for some string manipulation
import http.server  # Import http.server to serve the application
from socketserver import TCPServer  # Import socketserver for creating a server.

# External imports
from rich.console import Console   # Import Console for printing colored output
from rich.markdown import Markdown   # Import Markdown for printing markdown
from mistletoe import markdown as rm   # Import markdown from mistletoe

# Version constant
VERSION = '0.1.0-beta'

# Create rich console
console = Console()

# IsSass error that extends Exception. This is to stop multiple injection messages
class IsSass(Exception):
    pass


# IsGlobal error that extends Exception. This is to stop multiple injection messages
class IsGlobal(Exception):
    pass


# Help function
def help():
    # The help message
    helpMsg = f'''
python3 main.py [command] [options]

Commands:
    compile: compiles markdown in the content dir into html in the app dir
    serve: servers the app dir [--port: specify the port]

    heatherdom v{VERSION}. Located at {__file__}
    '''
    # Print the help message
    console.print(helpMsg, style="green")


# Compile function
def compile():
    # For every file in the ./content directory
    for child in Path('./content').iterdir():
        # If it's a file (directory's are not supported)
        if child.is_file():
            # Print the name of the file in markdown
            md = Markdown(f'# {child}')
            console.print(md)
            # Sleep for 1 second
            sleep(1)
            # Try:
            try:
                # Open the child
                with open(child, 'rt') as f:
                    # Render markdown using mistletoe
                    markdown = rm(f.read())
                    # Get the filename
                    filename = PurePath(child)
                    # Remove the extension
                    filename_no_ext = filename.stem
                    # Open the html and write an initial boilerplate
                    with open(f'app/{filename_no_ext}.html', 'wt') as f:
                        f.write(
                            f'''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" type="image/x-icon" href="../public/favicon.ico">
        <title>{filename_no_ext}</title>
    </head>
    <body>
                    '''
                        )
                    # Declare css in case it does not exist
                    css = ''
                    # If the css directory exists
                    if exists('./styles'):
                        # Open the html and write the initial style tag
                        with open(f'app/{filename_no_ext}.html', 'at') as f:
                            f.write(
                                '''
        <style>
                            '''
                            )
                        # For every file in ./styles
                        for childCSS in Path('./styles').iterdir():
                            # Clean the css
                            css = ''
                            # If the css is a file
                            if childCSS.is_file():
                                # Get the filename
                                filenameCss = PurePath(child)
                                # Remove extension
                                filenameCss_no_ext = filenameCss.stem
                                # Get the css name
                                fullFileNameCss = PurePath(childCSS)
                                # Compile sass
                                system('sass --no-source-map styles/:styles/')
                                # Try catch
                                try:
                                    # If the filename.suffix is = sass or scss
                                    if (
                                        fullFileNameCss.suffix == '.sass'
                                        or fullFileNameCss.suffix == '.scss'
                                    ):
                                        # Skip it because its sass
                                        raise IsSass()
                                    # If the filename without the extension is * (global, applied to every html file)
                                    elif fullFileNameCss.stem == '*':
                                        # Read it
                                        with open('styles/*.css', 'rt') as f:
                                            css = f.read()
                                        # Raise an error to skip it
                                        raise IsGlobal()
                                    # Else
                                    else:
                                        # Open the corresponding filename
                                        with open(
                                            f'styles/{filenameCss_no_ext}.css', 'rt'
                                        ) as f:
                                            # and read the css
                                            css = f.read()
                                        # Print that the css is getting injected
                                        console.print(
                                            f'\nCss {childCSS} injected into {filename_no_ext}.html',
                                            style='green',
                                        )
                                # If no file is found
                                except FileNotFoundError:
                                    # Print that is there is no css
                                    console.print(
                                        f'\nNo css to inject in {filename_no_ext}.html',
                                        style='red',
                                    )
                                # If it's sass
                                except IsSass:
                                    # Say it's sass
                                    console.print(
                                        '\nFound sass, skipping', style="blue"
                                    )
                                # If it's global styles
                                except IsGlobal:
                                    # Say it's global styles
                                    console.print(
                                        'Found global styles. Injecting', style="green"
                                    )
                                # Open the corresponding html file
                                with open(f'app/{filename_no_ext}.html', 'at') as f:
                                    # And write the css
                                    f.write(
                                        f'''
{css}
                                        '''
                                    )
                        # Sleep for 1 second
                        sleep(1)
                    # Else:
                    else:
                        # Print that there is no style directory
                        console.print('\nNo styles directory, skipping', style='blue')
                    # Close style tags
                    with open(f'app/{filename_no_ext}.html', 'at') as f:
                        f.write(
                            '''
        </style>
                        '''
                        )
                    # Open the html file to write the rendered markdown
                    with open(f'app/{filename_no_ext}.html', 'at') as f:
                        f.write(
                            f'''
        {markdown}
                            '''
                        )
                    # Close body and html tags
                    with open(f'app/{filename_no_ext}.html', 'at') as f:
                        f.write(
                            '''
    </body>
</html>
                        '''
                        )
                # Print out that it has compiled
                console.print(f'\nCompiled {child} to html', style='green')
                # Sleep
                sleep(1)
            # Except control c, abort
            except KeyboardInterrupt:
                console.print('USER ABORTED', style='red')
            # Except
            except:
                # It failed to compile
                console.print(f'\nFailed to compile {child} to html', style='red')
                sleep(1)
        # Else, print that it's a directory
        else:
            console.print(f'\n{child} is a directory', style='red')

# Serve function (Takes port as an argument)
def serve(PORT):
    # Get the directory (app)
    DIRECTORY = 'app'

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
        console.print(f'Serving at port {PORT}', style='blue')
        # Start server
        httpd.serve_forever()

# CLI Arguments
try:
    # If argv[1] == "compile"
    if argv[1] == 'compile':
        # Run the compile function
        compile()
    # Else if the command is serve
    elif argv[1] == 'serve':
        # Check if the --port argument is provided
        if argv[2] == '--port':
            # Serve with the port argument
            serve(int(argv[3]))
        # If there are not arguments
        elif len(argv) != 2:
            # Print an error
            console.print('Error! Extra arguments passed\n', style='red')
            # Print help
            help()
        # Else serve to port 3000
        else:
            serve(3000)
    # If the first argument is help
    elif argv[1] == '--help':
        # Print help
        help()
    # If the argument is --version
    elif argv[1] == '--version':
        # Print version and location of the file
        console.print(f'''
    heaterdom v{VERSION}, found at {__file__},
        ''', style='green')  
    # No arguments passed
    else:
        # Print help
        help()
# Except no arguments
except IndexError:
    help()
# Except control c
except KeyboardInterrupt:
    pass
