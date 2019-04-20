import pickle
from pathlib import Path

ROOM_COORDS_RPD1F = {
    'OFFSET': (0, 40),
    'MAIN HALL': [(1140, 960),
                  (1130, 1100),
                  (1060, 500),
                  (None, None),
                  (1080, 800)],
    'RECEPTION': [(770, 1120),
                  (840, 1060)],
    'OPERATIONS ROOM': [(370, 470)],
    'WESTERN AREA 1F': [(470, 440),
                        (720, 390),
                        (790, 420)],
    'WEST OFFICE': [(610, 920),
                    (530, 970),
                    (530, 1090),
                    (750, 920)],
    'DARK ROOM': [(720, 470),
                  (820, 530),
                  (760, 670)],
    'SAFETY DEPOSIT ROOM': [(2080, 230),
                            (2080, 170),
                            (2080, 100),
                            (2080, 30),
                            (1900, 180),
                            (1900, 60),
                            (540, 370),
                            (600, 370)],
    'PRESS ROOM': [(1580, 630)],
    'EAST CLOSET AMBUSH': [(1430, 790),
                           (1410, 740)],
    'BATHROOM': [(1800, 780)],
    'DETONATOR ROOM': [(270, 710),
                       (400, 710),
                       (350, 660),
                       (300, 780)],
    'RECORDS ROOM': [(330, 860),
                     (285, 1090),
                     (370, 920)],
    'EAST OFFICE': [(1680, 1100),
                    (1550, 1100),
                    (1600, 1150),
                    (1560, 970),
                    (1450, 1140),
                    (1370, 1140),
                    (1440, 1000)],
    'FIRE ESCAPE': [(1980, 1080),
                    (2030, 1160),
                    (1910, 1120)],
    'OUTSIDE BREAK ROOM': [(1930, 460),
                           (1970, 920)],
    'BREAK ROOM': [(1910, 650),
                   (1910, 730),
                   (1980, 800),
                   (1920, 790),
                   (1980, 690)],
    'BOILER ROOM': [(1390, 280),
                    (1480, 170)],
    'INTERROGATION ROOM': [(1360, 530)],
    'OUTSIDE OBSERVATION ROOM': [(1430, 620)],
    'OBSERVATION ROOM': [(1350, 630),
                         (1290, 590)],
    'ROOF AREA': [(None, None),
                  (None, None),
                  (2020, 320),
                  (1940, 320)]
}

ROOM_COORDS_RPD2F = {
    'MAIN HALL': [(None, None),
                  (None, None),
                  (1110, 440),
                  (900, 1190),
                  (None, None)],
    'WAITING ROOM': [(1430, 1040),
                     (1510, 1050)],
    'WESTERN AREA 2F': [(820, 450),
                        (450, 420),
                        (550, 280),
                        (630, 280),
                        (630, 340)],
    'LIBRARY': [(620, 520),
                (620, 870),
                (810, 880)],
    'LOUNGE': [(550, 1100),
               (670, 1100)],
    'CHOPPER CRASH AREA': [(1590, 710),
                           (1860, 1130)],
    'ART ROOM': [(1740, 890),
                 (1670, 1050),
                 (1740, 1050)],
    'STARS OFFICE': [(430, 680),
                     (310, 630),
                     (320, 810),
                     (480, 750),
                     (480, 850),
                     (420, 930),
                     (460, 510)],
    'LINEN ROOM': [(310, 990),
                   (390, 1030)],
    'ROOF AREA': [(2060, 820),
                  (2110, 740)]
}

ROOM_COORDS_RPD3F = {
    'WESTERN AREA 3F': [(850, 430),
                        (600, 430),
                        (680, 290)],
    'WEST STORAGE ROOM': [(300, 850),
                          (370, 700),
                          (300, 600),
                          (420, 900)],
    'MAIDEN STATUE AREA': [(480, 1070)],
    'MAIN HALL 3F': [(1000, 1220)],
    'CLOCK TOWER': [(620, 1160),
                    (750, 1140)],
    'EAST STORAGE ROOM': [(1670, 500),
                          (1670, 580),
                          (1810, 620)],
    'BALCONY': [(1930, 830)],
    'EAST AREA 3F': [(1970, 470),
                     (1880, 570),
                     (2040, 590)]
}

ROOM_COORDS_RPD1B = {
    'PARKING GARAGE': [(1100, 900)],
    'JAIL ENTRANCE': [(800, 1140)],
    'JAIL': [(250, 1220),
             (360, 1240),
             (360, 1170)],
    'OUTSIDE KENNEL': [(1620, 1000)],
    'KENNEL': [(1560, 940)],
    'MORGUE': [(1900, 980),
               (2020, 980),
               (1950, 870)],
    'FIRING RANGE': [(1610, 500),
                     (1490, 580)],
    'FIRING RANGE LOCKERS': [(1570, 390),
                             (1510, 360)],
    'GENERATOR ROOM': [(1880, 600),
                       (2010, 680),
                       (1950, 730)],
    'OUTSIDE RPD': [(1000, 400)],
    'GUN SHOP': [(960, 200),
                 (1040, 200),
                 (1120, 200)],
    'SEWER ENTRANCE': [(1200, 200),
                       (1280, 200),
                       (1360, 200)]
}

ROOM_COORDS_UNDERGROUND = {
    'SECRET ROOM': [(1080, 310),
                    (1010, 360)],
    'UNDERGROUND STAIRS': [(1480, 200),
                           (1570, 200)],
    'MACHINERY ROOM': [(1210, 760),
                       (1270, 780),
                       (1270, 840),
                       (1110, 1160),
                       (1170, 1160),
                       (1620, 1050),
                       (1570, 1140),
                       (800, 460),
                       (890, 400)],
    'OPERATORS ROOM': [(780, 1160)],
    'RPD ACCESS ROOM': [(1750, 200)]
}

ROOM_COORDS_SEWER_UPPER = {
    'ROOK BRIDGE AREA': [(1700, 1030),
                         (1400, 550)],
    'WORKERS BREAK ROOM': [(1620, 700),
                           (1610, 800)],
    'WATER INJECTION CHAMBER': [(1540, 250),
                                (1450, 250)],
    'WORKROOM': [(1270, 520),
                 (1200, 520),
                 (1230, 620)],
    'CONTROL ROOM': [(500, 600),
                     (400, 460)]
}

ROOM_COORDS_SEWER_MID = {
    'UPPER WATERWAY': [(1300, 1300),
                       (1900, 780)],
    'LOWER WATERWAY PRE-SLIDE': [(2050, 500)],
    'MONITOR ROOM': [(580, 330),
                     (300, 520),
                     (300, 600),
                     (370, 520)],
    'TREATMENT POOL ROOM': [(850, 400),
                            (900, 200),
                            (800, 850),
                            (940, 870)],
    'OUTSIDE GARBAGE ROOM': [(640, 920),
                             (520, 970)],
    'MAIN POWER ROOM': [(550, 1200)],
    'G2 FIGHT ROOM': [(50, 1150),
                      (20, 1060),
                      (10, 980),
                      (70, 950)]
}

ROOM_COORDS_SEWER_LOWER = {
    'WORKROOM LIFT': [(1880, 940)],
    'BOTTOM WATERWAY': [(1100, 860),
                        (850, 1070)],
    'SUPPLIES STORAGE ROOM': [(420, 1000),
                              (80, 940),
                              (140, 970),
                              (120, 1050),
                              (370, 900)],
    'BOTTOM WATERWAY OVERPASS': [(1180, 1100),
                                 (1460, 740),
                                 (1300, 550)],
    'LOWER WATERWAY': [(1700, 670),
                       (2000, 840)]
}

ROOM_COORDS_NEST_NORTH = {
    'SECURITY ROOM': [(1600, 880)],
    'CAFETERIA': [(1040, 750),
                  (880, 680),
                  (880, 760)],
    'KITCHEN': [(800, 630),
                (800, 750)],
    'NAP ROOM': [(460, 750),
                 (480, 870),
                 (530, 750),
                 (600, 750)]
}

ROOM_COORDS_NEST_EAST = {
    'LOBBY': [(600, 500),
              (660, 400)],
    'FIRST PLANT ROOM': [(750, 160)],
    'GREENHOUSE CONTROL ROOM': [(960, 300),
                                (1040, 170)],
    'GREENHOUSE': [(1150, 400),
                   (1020, 700),
                   (900, 530)],
    'DRUG TESTING LAB': [(1240, 240),
                         (1150, 100)],
    'UNDERNEATH GREENHOUSE': [(1460, 790)],
    'LOUNGE (LAB)': [(1700, 790),
                     (1830, 840),
                     (1700, 900)],
    'SERVER ROOM': [(1720, 450),
                    (1740, 570),
                    (1830, 550)],
    'LOW-TEMP TESTING LAB': [(1600, 1100)],
    'MODULATOR ROOM': [(700, 800),
                       (590, 840),
                       (500, 800)]
}

ROOM_COORDS_NEST_WEST = {
    'BIOTESTING LAB': [(1970, 300),
                       (1900, 300),
                       (1660, 430),
                       (1480, 350)],
    'P-4 LEVEL TESTING LAB': [(340, 300),
                              (280, 250),
                              (280, 180)],
    'BIOREACTORS ROOM': [(1200, 680),
                         (1140, 760),
                         (1140, 1000),
                         (1200, 1120),
                         (1240, 1030),
                         (1360, 1060),
                         (1500, 1180),
                         (1650, 680),
                         (1650, 1000),
                         (1720, 940)]
}

MAP_COORDS = {
    'rpd1f.jpg': ROOM_COORDS_RPD1F,
    'rpd2f.jpg': ROOM_COORDS_RPD2F,
    'rpd3f.jpg': ROOM_COORDS_RPD3F,
    'rpd1b.jpg': ROOM_COORDS_RPD1B,
    'underground.jpg': ROOM_COORDS_UNDERGROUND,
    'sewer_upper.jpg': ROOM_COORDS_SEWER_UPPER,
    'sewer_middle.jpg': ROOM_COORDS_SEWER_MID,
    'sewer_lower.jpg': ROOM_COORDS_SEWER_LOWER,
    'nest_north.jpg': ROOM_COORDS_NEST_NORTH,
    'nest_east.jpg': ROOM_COORDS_NEST_EAST,
    'nest_west.jpg': ROOM_COORDS_NEST_WEST
}

with (Path.cwd() / 'resources' / 'icons.archive').open(mode='rb') as file_object:
    ITEM_IMGS = pickle.load(file_object)
