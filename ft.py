#!/bin/python3

import re
import sys
import typing
import argparse


type UpdatingColors = list[tuple[str, str]]


HEX = '#[0-9a-fA-F]{6}'


# Process of editing consists of three steps.
#
#
# 1) Create HTML file with all unique colors:
#
# Run `./ft.py  ~/.config/flow/themes/<theme-name>.json --make-html`
#   
# This step will produce the HTML file `~/.config/flow/themes/<theme-name>.json.html`,
# containing a simple grid with colors: now and new.
# 
# 2) Open it in browser `file:///home/<your-user>/.config/flow/themes/<theme-name>.json.html`.
# Change the color by clicking on the `new` color (native input color picker) or directly
# by editing hex-code (this value is not validating).
#
# After modifications simply save the page with the same name, to the same location,
# overwriting previous file (without changes).
#
#
# 3) Update the customizable theme using values from 
# `~/.config/flow/themes/<theme-name>.json.html` of first step.
#
# Run `./ft.py  ~/.config/flow/themes/<theme-name>.json --update-theme`


def args_parser():
        
    parser = argparse.ArgumentParser(description="VSCode theme editor helper script for the Flow")
    group = parser.add_mutually_exclusive_group()

    parser.add_argument("path", type=str, help="The absolute path to customizable theme")

    group.add_argument("--make-html", action="store_true", help="Make updating HTML file at the same directory")

    group.add_argument("--update-theme", action="store_true", help="Update the customizable theme with values from corresponding HTML")

    return parser


def main():
    parser = args_parser()    
    args = parser.parse_args()

    if args.make_html:
        make_updating_html(args.path)
    elif args.update_theme:
        update_theme(args.path)
    else:
        print("Incorrect usage, see --help")



# 1 step: generate updating html to open it in a browser,
# change colors and save as html again
def make_updating_html(theme_path):
    colors = parse_theme_colors(read(theme_path))

    html = colors_to_html(colors)
    
    write(updating_html_path(theme_path), html)


# 2 step: read updating html from step-1, read original theme,
# replace now colors in it by new, save with the same name.
def update_theme(theme_path):
    updating_html = read(updating_html_path(theme_path))
    original_theme = read(theme_path)
    
    colors = parse_updating_colors(updating_html)

    updated_theme = update_theme_colors(original_theme, colors)

    write(theme_path, updated_theme)


def updating_html_path(theme_path):
    return f"{theme_path}.html"


def parse_theme_colors(text):
    return sorted([c.upper() for c in set( re.findall(HEX, text))])


def parse_updating_colors(text) -> UpdatingColors:

    def parse(now_or_new: typing.Literal["now","new"]):
        return list(map(
                        lambda val: val.strip().upper(),
                        re.findall(f'data-{now_or_new}="([0-9a-fA-F#]+)"', text)
                    ))

    now = parse("now")
    
    new = parse("new")
    
    return [(c, n) for c, n in zip(now, new)]


def update_theme_colors(theme: str, colors: UpdatingColors) -> str:
    for now, new in colors:
        if now == new:
            continue
        
        print(f"replaced: {now} -> {new}")
        theme = theme.replace(now, new)
    return theme


def color_to_html(color):
    return f'''
<div class="pair">
    <div style="background-color: {color};"></div>
    <div>
        <input
            onchange=onColor(event)
            type="color"
            style="background-color: {color}"
            value="{color}"
            >
    </div>
    <div data-now="{color}">
        <div>now</div>
        <div>{color}</div>
    </div>
    <div data-new="{color}">
        <div>new</div>
        <div onblur=onBlur(event) contenteditable>{color}</div>
    </div>
</div>
'''

    
def colors_to_html(colors):

    grid = "\n".join([color_to_html(c) for c in colors])

    return f'''
<!DOCTYPE html>
<html>
<head>
{style()}
{script()}

</head>
<body class="s">

{grid}

</body>
</html>
'''


def script():
    return '''
<script>
function onBlur(e) {
    const val = e.target.textContent.trim().toLocaleUpperCase();

    e.target.textContent = val;

    e.target.parentElement.dataset["new"] = val;

    const color = e.target.parentElement.previousElementSibling.previousElementSibling.firstElementChild;

    color.style.backgroundColor = val;

    color.value = val;
}

function onColor(e) {
    const el = e.target.parentElement.nextElementSibling.nextElementSibling;

    const val = e.target.value.trim().toLocaleUpperCase();
    
    el.dataset["new"] = val;

    el.lastElementChild.textContent = val;
}
</script>
    '''


def style():
    return '''
<style>
input[type="color"] {
  -webkit-appearance: none;
  border: none;
  cursor: pointer;
  background: none;
  padding: 0;
}


input[type="color"]::-moz-color-swatch {
  border: none;
  border-radius: 0;
}


body {
    background-color: #a96f92;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    row-gap: 40px;
}

body > div {
    width: 520px;
    height: 300px;
    display: grid;
    grid-template-columns: 3fr 1fr;
    grid-template-rows: 1fr 1fr;

    > div {
        height: 100%;
        align-content: center;
    }

    > div:nth-child(1) {
        grid-column: 1 / 2;
        grid-row: 1 / 2;
        position: relative;
    }

    > div:nth-child(2) {
        grid-column: 1 / 2;
        grid-row: 2 / 3;

        > input {
            display: flex;
            width: 100%;
            height: 100%;
            border: none;
            outline: none;
        }
    }

    > div:nth-child(2), div:nth-child(2) {
        // width: 50%;
    }

}}
</style>
'''


def read(path):
    with open(path, "r") as fd:
        return fd.read()


def write(path, data):
    with open(path, "w") as fd:
        return fd.write(data)



    

if __name__ == "__main__":
    main()

