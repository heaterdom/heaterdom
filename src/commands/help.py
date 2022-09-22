from rich.console import Console

console = Console()
# Version constant
VERSION = "0.2.0"


# Help function
def help():
    # The help message
    helpMsg = f"""
python3 main.py [command] [options]

Commands:
    compile: compiles markdown in the content dir into html in the app dir
    serve: servers the app dir [--port: specify the port]

    heatherdom v{VERSION}. Located at {__file__}
    """
    # Print the help message
    console.print(helpMsg, style="green")