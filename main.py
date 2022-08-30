from os import mkdir
from os.path import exists
from time import sleep
from rich.console import Console
from rich.markdown import Markdown
from pathlib import Path, PurePath
from mistletoe import markdown

# Create rich console
console = Console()

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
