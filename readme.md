# Heaterdom

Minimal and transparent static site generator.

## Features

- Minimal. Compiles your html and css in under 300 lines of code.
- Transparent. The cli is not hidden, it's the heaterdom.py file. You can use and modifying it to your liking.

## Installation

Use the install.sh to bootstrap a new project. Curl, Python3 and git is required.

```bash
bash <(curl -sL https://gist.githubusercontent.com/micziz/6f280cfaa32fae4ed865d5bd49cbf500/raw/09a002b84d3f9cbd2ee0ab65f9e60b40f7b152a7/install.sh)
```

## Usage

Write some markdown in the content directory

Then, once you have finished writing, run:

```bash
python3 heaterdom.py compile
```

This will compile the Markdown to HTML.

Then to serve it run:

```bash
python3 heaterdom.py serve
```

This will serve it at `localhost::3000`

If you want to customize the port, just add the --port option followed by the port number.

```bash
python3 heaterdom.py serve --port 8080
```

## Styling

To add css, create a directory called `styles`. Then, write your css with the same name as the html file you want to customize.

If you prefer to use sass, just change the file extension to `.scss` or `.sass`. Heaterdom will compile them automatically.

## TODO

- [x] More options to the cli
- [ ] Add folders
- [ ] Add templates with jinga or another template engine
- [ ] Proper documentation

## License

Copyright 2022 micziz and contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License
