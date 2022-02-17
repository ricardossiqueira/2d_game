WIDTH = 1280
HEIGHT = 720
FPS = 60
TILE_SIZE = 64

# ui
BAR_HEIGHT = 20
HP_BAR_WIDTH = 200
STA_BAR_WIDTH = 140
MP_BAR_WIDTH = 180
ITEM_BOX_SIZE = 50
UI_FONT = 'src/graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HP_COLOR = 'red'
STA_COLOR = 'yellow'
MP_COLOR = 'blue'
UI_ACTIVE_COLOR = '#444444'

# weapons
WEAPON_DATA = {
    'sword': {
        'cd': 100,
        'pow': 15,
        'graphic': 'src/graphics/weapons/sword/full.png'
    },
    'lance': {
        'cd': 400,
        'pow': 30,
        'graphic': 'src/graphics/weapons/lance/full.png'
    },
    'axe': {
        'cd': 300,
        'pow': 20,
        'graphic': 'src/graphics/weapons/axe/full.png'
    },
    'rapier': {
        'cd': 50,
        'pow': 8,
        'graphic': 'src/graphics/weapons/rapier/full.png'
    },
    'sai': {
        'cd': 80,
        'pow': 10,
        'graphic': 'src/graphics/weapons/sai/full.png'
    }
}

# spells
SPELL_DATA = {
    'flame': {
        'pow': 5,
        'mp': 20,
        'graphic': 'src/graphics/particles/flame/fire.png'
    },
    'heal': {
        'pow': 20,
        'mp': 10,
        'graphic': 'src/graphics/particles/heal/heal.png'
    }
}
