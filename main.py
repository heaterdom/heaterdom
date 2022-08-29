# Imports
# Import os for mostly path reasons
from os import listdir, path, system
from os.path import splitext, basename
from time import sleep
from rich.console import Console
from rich.markdown import Markdown
# Import mistletoe for markdown parsing
import mistletoe

console = Console()

# Write the initial flask app
with open("app.py", "wt") as f:
    f.write("""
from flask import Flask
from flask import render_template

app = Flask(__name__, template_folder='./app')
    """)

# For every filename in the /content direcotry:
for filename in listdir('content'):
    md = Markdown(f"# {filename}")
    console.print(md)
    console.print(f'\nCompiling {filename} to html', style="red")
    sleep(1)
    # Declare no css, as there may not be css for a specific file
    css = ''
    with open(f"content/{filename}", 'rt') as f:
        rendered = mistletoe.markdown(f.read())        
        filename = basename(filename)
        filename_without_ext = splitext(filename)[0]
        try:
            out = f'\nInjecting css into {filename}'
            for filenames in listdir('styles'):
                if filenames.endswith('.sass') or filenames.endswith('.scss'):
                    sleep(1)
                    system('sass styles/:styles/')
                else:
                    sleep(1)
                    if filenames == '*.css':
                        with open (f"styles/*.css", "rt") as f:
                            css = f.read()
                    else:
                        with open (f"styles/{filename_without_ext}.css", "rt") as f:
                            css = f.read()
        except FileNotFoundError:
            out = f'\nNo css to inject for {filename}'
        if out == f'\nNo css to inject for {filename}':
            console.print(out, style="red")
        else:
            console.print(out, style="blue")
        sleep(1)
        with open(f"app/{filename_without_ext}.html", "wt") as f:
            f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <style>
        { css }
    </style>

    { rendered }
</body>
</html>
            """)
        
        console.print(f"\nCreating routes for {filename}\n", style="green")
        sleep(1)
        if filename_without_ext == "index":
            with open(f"app.py", "at") as f:
                f.write(f"""
@app.route("/")
def {filename_without_ext}():
    return render_template('{filename_without_ext}.html')
                """)
        else:
            with open(f"app.py", "at") as f:
                f.write(f"""
@app.route("/{filename_without_ext}")
def {filename_without_ext}():
    return render_template('{filename_without_ext}.html')
                """)
