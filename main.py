import re
import sys
import tkinter as tk
import random
from pathlib import Path
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar

from PIL import Image

from mappings import MAP_COORDS, ITEM_IMGS
from constants import *

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


def is_excluded(item):
    if exclude_healing_var.get():
        if item in HEALING_ITEMS:
            return True

    if exclude_ammo_var.get():
        if item in AMMO_ITEMS:
            return True

    if exclude_weapons_var.get():
        if item in WEAPONS_ITEMS:
            return True

    if exclude_progression_var.get():
        if item not in HEALING_ITEMS and item not in AMMO_ITEMS and item not in WEAPONS_ITEMS:
            return True


def draw_items(room_items, percentage: int):
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
                    if random.randint(1, 101) > percentage:
                        continue
                    if 'Upgrade Chip' not in item and 'Long Barrel' not in item:
                        item = item.split(' (')[0]
                    if is_excluded(item):
                        continue
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

    # INIT
    ####################################################################################################################

    root = tk.Tk()
    root.title('RE2R - Cheat Sheet Visualizer for randomizer 0.0.6')
    cs_file = None
    mode = None

    # GUI ELEMENTS
    ####################################################################################################################

    # Vars
    playthrough_var = tk.IntVar()
    spoiler_percentage_var = tk.StringVar()
    spoiler_percentage_var.set("100")
    exclude_healing_var = tk.BooleanVar()
    exclude_ammo_var = tk.BooleanVar()
    exclude_progression_var = tk.BooleanVar()
    exclude_weapons_var = tk.BooleanVar()
    # Outputs
    cs_label = tk.Label(root, height=2)
    spoiler_label = tk.Label(root, text='Spoiler percentage: ')
    spoiler_description = tk.Label(root, text=SPOILER_DESC)
    exclude_label = tk.Label(root, text='Exclude from spoiler:')
    exclude_healing_label = tk.Label(root, text=EXCLUDE_HEALING_DESC)
    exclude_ammo_label = tk.Label(root, text=EXCLUDE_AMMO_DESC)
    exclude_progression_label = tk.Label(root, text=EXCLUDE_PROGRESSION_DESC)
    exclude_weapons_label = tk.Label(root, text=EXCLUDE_WEAPONS_DESC)
    progressbar = Progressbar(root, orient=tk.HORIZONTAL, length=550, mode='determinate')
    # Inputs
    run_button = tk.Button(root, text='Generate maps', state=tk.DISABLED)
    leon_radio_button = tk.Radiobutton(root, text='Leon A', value=1, variable=playthrough_var)
    claire_radio_button = tk.Radiobutton(root, text='Claire A', value=2, variable=playthrough_var)
    cs_button = tk.Button(root, text='Select CheatSheet')
    credits_button = tk.Button(root, text='Credits')
    spoiler_percentage = tk.Spinbox(root, from_=0, to=100, width=5, textvariable=spoiler_percentage_var)
    exclude_cb_healing = tk.Checkbutton(root, text='Healing items', var=exclude_healing_var)
    exclude_cb_ammo = tk.Checkbutton(root, text='Ammunition', var=exclude_ammo_var)
    exclude_cb_weapons = tk.Checkbutton(root, text='Weapons', var=exclude_weapons_var)
    exclude_cb_progression = tk.Checkbutton(root, text='Progression items', var=exclude_progression_var)

    # LAYOUT
    ####################################################################################################################

    cs_label.grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
    cs_button.grid(row=0, column=0, sticky=tk.W + tk.E, padx=10, pady=5, columnspan=2)

    leon_radio_button.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
    claire_radio_button.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
    spoiler_percentage.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
    spoiler_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
    spoiler_description.grid(row=2, column=2, sticky=tk.W, padx=10, pady=5)

    exclude_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
    exclude_healing_label.grid(row=3, column=2, sticky=tk.W, padx=10, pady=5)
    exclude_ammo_label.grid(row=4, column=2, sticky=tk.W, padx=10, pady=5)
    exclude_progression_label.grid(row=5, column=2, sticky=tk.W, padx=10, pady=5)
    exclude_weapons_label.grid(row=6, column=2, sticky=tk.W, padx=10, pady=5)
    exclude_cb_healing.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
    exclude_cb_ammo.grid(row=4, column=1, sticky=tk.W, padx=10, pady=5)
    exclude_cb_weapons.grid(row=5, column=1, sticky=tk.W, padx=10, pady=5)
    exclude_cb_progression.grid(row=6, column=1, sticky=tk.W, padx=10, pady=5)

    run_button.grid(row=999, column=0, sticky=tk.W + tk.E, padx=10, pady=5, columnspan=2)
    progressbar.grid(row=999, column=2, columnspan=1, padx=10, pady=5, sticky=tk.W + tk.E)
    credits_button.grid(row=1000, column=2, sticky=tk.E, padx=10, pady=30)

    # CALLBACKS
    ####################################################################################################################

    def run_button_callback():

        if cs_file is None:
            return

        if (exclude_ammo_var.get() and exclude_healing_var.get() and
            exclude_progression_var.get() and exclude_weapons_var.get()) or spoiler_percentage_var.get() == "0":
            if messagebox.askokcancel(title='Warning: Everything excluded',
                                      message='Your settings would result in empty maps, since everything is excluded.'
                                              '\n\n'
                                              'Do you really want to continue?'):
                pass
            else:
                return

        # noinspection PyTypeChecker
        draw_items(cheat_sheet_to_dict(Path(cs_file)), percentage=int(spoiler_percentage_var.get()))
        progressbar['value'] = 100
        root.update_idletasks()
        root.update()
        messagebox.showinfo('Success', 'Done. Check out your new maps in the output folder.')
        sys.exit()


    def radio_callback():
        global mode
        mode = playthrough_var.get()
        if cs_file is not None:
            run_button.config(state='normal')


    def cs_button_callback():
        global cs_file
        cs_file = filedialog.askopenfilename(initialdir=Path.cwd(), title="Select cheat sheet file",
                                             filetypes=[("Text files", "*.txt")])
        if cs_file is not None:
            with Path(cs_file).open(mode='r') as cheat_sheet:
                pattern = "^Version [0-9]*\.[0-9]*\.[0-9]*.*"
                if not re.match(pattern=pattern, string=cheat_sheet.readline()):
                    messagebox.showerror(title='Unrecognized format',
                                         message='Could not recognize cheat sheet format. '
                                                 'Please check that you linked to a cheat sheet file.')
                    cs_file = None
                    return
            cs_label.configure(text=str(cs_file))
            if mode is not None:
                run_button.config(state='normal')


    def credit_button_callback():
        messagebox.showinfo('Credits', 'RE2R - Cheat Sheet Visualizer', detail=CREDIT_STR)


    # BIND CALLBACKS
    ####################################################################################################################

    run_button.config(command=run_button_callback)
    leon_radio_button.config(command=radio_callback)
    claire_radio_button.config(command=radio_callback)
    cs_button.config(command=cs_button_callback)
    credits_button.config(command=credit_button_callback)

    # RUN
    ####################################################################################################################

    claire_radio_button.config(state='disabled')
    center_window(root)
    tk.mainloop()
