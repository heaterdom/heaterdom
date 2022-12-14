#!/usr/bin/env python3

# Standard Library Imports
from os import (
    mkdir,
    system,
)  # Import os for system commands. This is needed to compile sass
from os.path import exists  # Import exists from path to check if styles exists
from sys import argv  # Import argv for arguments
from time import sleep  # Import time to slow down a bit
from pathlib import (
    Path,
    PurePath,
)  # Import Path for iterating in directory and PurePath for some string manipulation
import http.server  # Import http.server to serve the application
from socketserver import TCPServer  # Import socketserver for creating a server.
from src.utils.Errors import IsGlobal, IsSass
from src.commands.help import help

# External imports
from rich.console import Console  # Import Console for printing colored output
from rich.markdown import Markdown  # Import Markdown for printing markdown
from mistletoe import markdown as mr  # Import markdown from mistletoe

# Version constant
VERSION = "0.2.0"

# Create rich console
console = Console()


# Compile function
def compile(dir, outDir):
    # For every file in the ./content directory
    for child in Path(f"./{dir}").iterdir():
        # If it's a file (directory's are not supported)
        if child.is_file():
            # Print the name of the file in markdown
            md = Markdown(f"# {child}")
            console.print(md)
            # Sleep for 1 second
            sleep(1)
            # Try:
            try:
                # Open the child
                with open(child, "rt") as f:
                    # Render markdown using mistletoe
                    markdown = mr(f.read())
                    # Get the filename
                    filename = PurePath(child)
                    # Remove the extension
                    filename_no_ext = filename.stem
                    # Open the html and write an initial boilerplate
                    with open(f"{outDir}/{filename_no_ext}.html", "wt") as f:
                        f.write(
                            f"""
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
                    """
                        )
                    # Declare css in case it does not exist
                    css = ""
                    # If the css directory exists
                    if exists("./styles"):
                        # Open the html and write the initial style tag
                        with open(f"{outDir}/{filename_no_ext}.html", "at") as f:
                            f.write(
                                """
        <style>
                            """
                            )
                        # For every file in ./styles
                        for childCSS in Path("./styles").iterdir():
                            # Clean the css
                            css = ""
                            # If the css is a file
                            if childCSS.is_file():
                                # Get the filename
                                filenameCss = PurePath(child)
                                # Remove extension
                                filenameCss_no_ext = filenameCss.stem
                                # Get the css name
                                fullFileNameCss = PurePath(childCSS)
                                # Compile sass
                                system("sass --no-source-map styles/:styles/")
                                # Try catch
                                try:
                                    # If the filename.suffix is = sass or scss
                                    if (
                                        fullFileNameCss.suffix == ".sass"
                                        or fullFileNameCss.suffix == ".scss"
                                    ):
                                        # Skip it because its sass
                                        raise IsSass()
                                    # If the filename without the extension is * (global, applied to every html file)
                                    elif fullFileNameCss.stem == "*":
                                        # Read it
                                        with open("styles/*.css", "rt") as f:
                                            css = f.read()
                                        # Raise an error to skip it
                                        raise IsGlobal()
                                    # Else
                                    else:
                                        # Open the corresponding filename
                                        with open(
                                            f"styles/{filenameCss_no_ext}.css", "rt"
                                        ) as f:
                                            # and read the css
                                            css = f.read()
                                        # Print that the css is getting injected
                                        console.print(
                                            f"\nCss {childCSS} injected into {filename_no_ext}.html",
                                            style="green",
                                        )
                                # If no file is found
                                except FileNotFoundError:
                                    # Print that is there is no css
                                    console.print(
                                        f"\nNo css to inject in {filename_no_ext}.html",
                                        style="red",
                                    )
                                # If it's sass
                                except IsSass:
                                    # Say it's sass
                                    console.print(
                                        "\nFound sass, skipping", style="blue"
                                    )
                                # If it's global styles
                                except IsGlobal:
                                    # Say it's global styles
                                    console.print(
                                        "Found global styles. Injecting", style="green"
                                    )
                                # Open the corresponding html file
                                with open(f"{outDir}/{filename_no_ext}.html", "at") as f:
                                    # And write the css
                                    f.write(
                                        f"""
{css}
                                        """
                                    )
                        # Sleep for 1 second
                        sleep(1)
                    # Else:
                    else:
                        # Print that there is no style directory
                        console.print("\nNo styles directory, skipping", style="blue")
                    # Close style tags
                    with open(f"{outDir}/{filename_no_ext}.html", "at") as f:
                        f.write(
                            """
        </style>
                        """
                        )
                    # Open the html file to write the rendered markdown
                    with open(f"{outDir}/{filename_no_ext}.html", "at") as f:
                        f.write(
                            f"""
        {markdown}
                            """
                        )
                    # Close body and html tags
                    with open(f"{outDir}/{filename_no_ext}.html", "at") as f:
                        f.write(
                            """
    </body>
</html>
                        """
                        )
                # Print out that it has compiled
                console.print(f"\nCompiled {child} to html", style="green")
                # Sleep
                sleep(1)
            # Except control c, abort
            except KeyboardInterrupt:
                console.print("USER ABORTED", style="red")
            # Except
            except:
                # It failed to compile
                console.print(f"\nFailed to compile {child} to html", style="red")
                sleep(1)
        # Else, print that it's a directory
        else:
            console.print(f"\n{child} is a directory", style="red")


# Create function
def create(name):
    # Open a new file with the name and write some content
    with open(f"content/{name}.md", "wt") as f:
        f.write("# Generated with the CLI")


# Create css function
def createCss(name, isItSass):
    # Check if it's sass
    if isItSass:
        # If yes
        try:
            # Open a new file with scss
            f = open(f"styles/{name}.scss", "xt")
        # If the styles directory does not exist
        except FileNotFoundError:
            # Create styles dir
            mkdir("styles")
            # Open a new file with scss
            f = open(f"styles/{name}.scss", "xt")
    # else
    else:
        try:
            # Open a new file with scss
            f = open(f"styles/{name}.css", "xt")
        # If the styles directory does not exist
        except FileNotFoundError:
            # Create styles dir
            mkdir("styles")
            # Open a new file with scss
            f = open(f"styles/{name}.css", "xt")


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


# CLI Arguments
try:
    # If argv[1] == "compile"
    if argv[1] == "compile":
        try:
            if argv[2] == "--dir":
                try:
                    if argv[4] == "--outdir":
                        compile(argv[3], argv[5])
                    else:
                        compile(argv[3], "app")
                except IndexError:
                    pass
            elif argv[2] == "--outdir":
                try:
                    if argv[4] == "--dir":
                        compile(argv[5], argv[3])
                    else:
                        compile("content", argv[3])
                except IndexError:
                    pass
            else:
            # Run the compile function
                compile("content", "app")
        except IndexError:
                compile("content", "app")
    # Else if the command is serve
    elif argv[1] == "serve":
        try:
            # Check if the --port argument is provided
            if argv[2] == "--port":
                # Serve with the port argument
                serve(int(argv[3]))
        except IndexError:
            serve(3000)
    # If the first argument is help
    elif argv[1] == "--help":
        # Print help
        help()
    # If the argument is --version
    elif argv[1] == "--version":
        # Print version and location of the file
        console.print(
            f"""
    heaterdom v{VERSION}, found at {__file__},
        """,
            style="green",
        )
    # If the argument is create
    elif argv[1] == "create":
        # If the second argument is sass
        if argv[2] == "sass":
            # Create css using sass
            createCss(argv[3], True)
        # If the second argument is css
        elif argv[2] == "css":
            # Create css using plain normal css
            createCss(argv[3], False)
        # If there is no css passed, create a new file
        else:
            create(argv[2])
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
 