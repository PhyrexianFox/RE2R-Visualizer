import re
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar

from PIL import Image

from mappings import MAP_COORDS, ITEM_IMGS

global root, progressbar

MAPS = ['rpd1f.jpg',
        'rpd2f.jpg',
        'rpd3f.jpg',
        'rpd1b.jpg',
        'underground.jpg',
        'sewer_upper.jpg',
        'sewer_middle.jpg',
        'sewer_lower.jpg',
        'nest_north.jpg',
        'nest_east.jpg',
        'nest_west.jpg']


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def cheat_sheet_to_dict(cs_path: Path):
    room_items = dict()
    pattern = "(^[1-9A-Z -]+)\n((^\t.*|\n)*)"
    with cs_path.open(mode='r') as cheat_sheet:
        raw_cs = cheat_sheet.read()
    matches = re.findall(pattern, raw_cs, re.MULTILINE)
    for m in matches:
        sub_pattern = "replaced with (.*)\n"
        sub_matches = re.findall(sub_pattern, m[1], re.MULTILINE)
        if m[0] == 'LOUNGE' and 'LOUNGE' in room_items:
            room_items['LOUNGE (LAB)'] = sub_matches
        elif m[0] == 'MONITOR ROOM' and 'MONITOR ROOM' in room_items:
            room_items['MONITOR ROOM (LAB)'] = sub_matches
        else:
            room_items[m[0]] = sub_matches
    return room_items


def draw_items(room_items):
    for progress, level_map in enumerate(MAPS):
        img = Image.open(Path.cwd() / 'maps' / level_map)
        tlist = list()
        dx, dy = (0, 0)
        if 'OFFSET' in MAP_COORDS[level_map]:
            dx, dy = MAP_COORDS[level_map]['OFFSET']

        for room in room_items:
            if room in MAP_COORDS[level_map]:
                coords = MAP_COORDS[level_map][room]
                for index, item in enumerate(room_items[room]):
                    if 'Upgrade Chip' not in item and 'Long Barrel' not in item:
                        item = item.split(' (')[0]
                    try:
                        x, y = coords[index]
                        if x is None:
                            continue
                    except IndexError:
                        continue
                    if item in ITEM_IMGS:
                        icon = ITEM_IMGS[item]
                        img.paste(icon, box=(x + dx, y + dy), mask=icon)
                    else:
                        pass
            else:
                for item in room_items[room]:
                    if item not in ITEM_IMGS and item not in tlist:
                        tlist.append(item)

        img.save(Path.cwd() / 'output' / level_map)
        progressbar['value'] = int(100 / 11 * progress)
        root.update_idletasks()
        root.update()


def build_tiles(image_path):
    tile_counter = 0
    dimension = 112
    image = Image.open(image_path)
    width, height = image.size

    for x in range(0, height, dimension):
        for y in range(0, width, dimension):
            box = (y, x, y + dimension, x + dimension)
            a = image.crop(box)

            try:
                a.save(Path.cwd() / 'resources' / 'icons' / ("IMG-%s.png" % tile_counter))
            except Exception:
                continue

            tile_counter += 1


if __name__ == '__main__':
    root = tk.Tk()
    root.title('RE2R - Cheat Sheet Visualizer for randomizer 0.0.6')
    cs_file = None

    cs_label = tk.Text(root, height=2)


    def run_button_callback():
        if cs_file is None:
            return
        # noinspection PyTypeChecker
        draw_items(cheat_sheet_to_dict(Path(cs_file)))
        progressbar['value'] = 100
        root.update_idletasks()
        root.update()
        messagebox.showinfo('Success', 'Done. Check out your new maps in the output folder.')
        sys.exit()


    run_button = tk.Button(root, text='Generate maps', command=run_button_callback, state=tk.DISABLED)


    def cs_button_callback():
        global cs_file
        cs_file = filedialog.askopenfilename(initialdir=Path.cwd(), title="Select cheat sheet file",
                                             filetypes=[("Text files", "*.txt")])
        if cs_file is not None:
            cs_label.delete(1.0, tk.END)
            cs_label.insert(tk.END, str(cs_file))
            run_button.config(state='normal')


    def credit_button_callback():
        credit_str = '''=============================
| Map backgrounds:
| rpd:\thttp://www.myfreetextures.com/excellent-old-brown-paper-texture-background/
|
| nest:\thttp://www.ianbarnard.co.uk/free-blueprint-style-background-vector/
|
| sewer:\thttp://bgfons.com/download/3891
=============================

=============================
| RE2 Map Components:
| https://www.reddit.com/r/residentevil/comments/ap3mj9/resident_evil_2_remake_map_textures/
=============================

=============================
| made by:
| \tPhyrexian Fox
=============================
        '''
        messagebox.showinfo('Credits', 'RE2R - Cheat Sheet Visualizer', detail=credit_str)


    cs_button = tk.Button(root, text='Select CheatSheet', command=cs_button_callback)
    credits_button = tk.Button(root, text='Credits', command=credit_button_callback)

    progressbar = Progressbar(root, orient=tk.HORIZONTAL, length=550, mode='determinate')

    cs_label.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
    cs_button.grid(row=0, column=0, sticky=tk.W + tk.E, padx=10, pady=5)
    run_button.grid(row=1, column=0, sticky=tk.W + tk.E, padx=10, pady=5)
    progressbar.grid(row=1, column=1, columnspan=1, padx=10, pady=5, sticky=tk.W + tk.E)
    credits_button.grid(row=2, column=1, sticky=tk.E, padx=10, pady=30)

    center_window(root)
    tk.mainloop()
