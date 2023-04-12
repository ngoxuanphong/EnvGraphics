from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import numpy as np
from setup import SHORT_PATH
from Base.StoneAge import _env
BUILDING_CARDS, CIV_CARDS = _env.BUILDING_CARDS, _env.CIV_CARDS
IMG_PATH = SHORT_PATH + "Base/StoneAge/playing_card_images/"
CARD_SIZE = (100, 140)
SIZE_BOARD = (1000, 1000)

tl = 3
BG_SIZE = (np.array([2585, 1821])/tl).astype(np.int64)
BUILDING_CARDS_SIZE =(np.array([263, 314])/3.4).astype(np.int64)
CIV_CARDS_SIZE =(np.array([335, 515])/3.4).astype(np.int64)

action_description = {
    0: "Dừng lấy công cụ",
    1: "Đặt 1 người",
    2: "Đặt 2 người",
    3: "Đặt 3 người",
    4: "Đặt 4 người",
    5: "Đặt 5 người",
    6: "Đặt 6 người",
    7: "Đặt 7 người",
    8: "Đặt 8 người",
    9: "Đặt 9 người",

    11: "Đặt người vào lúa",
    12: "Đặt vào ô công cụ",
    13: "Đặt vào ô sinh sản",
    14: "Đặt vào khu gỗ",
    15: "Đặt vào khu gạch",
    16: "Đặt vào khu bạc",
    17: "Đặt vào khu vàng",
    18: "Đặt vào khu lương thực",

    19: "Đặt người vào ô thẻ civ 0",
    20: "Đặt người vào ô thẻ civ 1",
    21: "Đặt người vào ô thẻ civ 2",
    22: "Đặt người vào ô thẻ civ 3",
    23: "Đặt người vào ô thẻ building 0",
    24: "Đặt người vào ô thẻ building 1",
    25: "Đặt người vào ô thẻ building 2",
    26: "Đặt người vào ô thẻ building 3",


    27: "Chọn trừ nguyên liệu (Khi đến hết vòng không đủ thức ăn)",
    28: "Chọn trừ điểm (Khi đến hết vòng không đủ thức ăn)",

    29: "Lấy người từ lúa",
    30: "Lấy người từ công cụ",
    31: "Lấy người từ sinh sản",
    32: "Lấy người từ gỗ",
    33: "Lấy người từ gạch",
    34: "Lấy người từ bạc",
    35: "Lấy người từ vàng",
    36: "Lấy người từ lương thực",

    37: "Dùng công cụ ở ô 1",
    38: "Dùng công cụ ở ô 1",
    39: "Dùng công cụ ở ô 1",

    40: "Trả nguyên liêu gỗ",
    41: "Trả nguyên liêu gạch",
    42: "Trả nguyên liêu bạc",
    43: "Trả nguyên liêu vàng",

    44: "Dùng công cụ một lần 1",
    45: "Dùng công cụ một lần 2",
    46: "Dùng công cụ một lần 3",

    47: "Dừng trả nguyên liệu khi mua thẻ build 1-7 (Thẻ build trả 1 đến 7 người để đổi ra điểm)",
    48: "Lấy người từ ô thẻ civ 0",
    49: "Lấy người từ ô thẻ civ 1",
    50: "Lấy người từ ô thẻ civ 2",
    51: "Lấy người từ ô thẻ civ 3",
    52: "Lấy người từ ô thẻ building 0",
    53: "Lấy người từ ô thẻ building 1",
    54: "Lấy người từ ô thẻ building 2",
    55: "Lấy người từ ô thẻ building 3",

    57: "Chọn xúc xắc số 1",
    58: "Chọn xúc xắc số 2",
    59: "Chọn xúc xắc số 3",
    60: "Chọn xúc xắc số 4",
    61: "Chọn xúc xắc số 5",
    62: "Chọn xúc xắc số 6",

    63: "Chọn dùng thẻ lấy thêm 2 nguyên liệu từ thẻ civ",
    64: "Trả nguyên liêu gỗ",
    65: "Trả nguyên liêu gạch",
    66: "Trả nguyên liêu bạc",
    67: "Trả nguyên liêu vàng",
    }

class Env_components:
    def __init__(self, env, winner, list_other) -> None:
        self.env = env
        self.winner = winner
        self.list_other = list_other


def get_description(action):
    if action < 0 or action >= _env.getActionSize():
        return ""
    return f"{action_description[action]}"


def get_env_components():
    env , all_build_card, all_civ_card = _env.initEnv(BUILDING_CARDS, CIV_CARDS)
    winner = _env.checkEnded(env)
    list_other = np.array([-1, 1, 2, 3])
    np.random.shuffle(list_other)
    env_components = Env_components(env, winner, list_other)
    return env_components


class Sprites:
    def __init__(self) -> None:
        self.background = Image.open(IMG_PATH+"board.webp").resize(BG_SIZE)
        self.cards_building = []
        for value in range(28):
            self.cards_building.append(Image.open(f"{IMG_PATH}building_card/{value}.png").resize(BUILDING_CARDS_SIZE))
        self.card_civilization = []
        for value in range(36):
            self.card_civilization.append(Image.open(f"{IMG_PATH}civ_card/{value}.png").resize(CIV_CARDS_SIZE))
        self.people = Image.open(f"{IMG_PATH}icon/people.png")
        self.font=ImageFont.truetype("Base/SushiGo/font/FreeMonoBoldOblique.ttf", 60)
        self.list_color = ['blue', 'green', 'red', 'white']


class Params:
    def __init__(self) -> None:

        x_0 = BG_SIZE[0] * 0.1
        x_1 = BG_SIZE[0] * 0.8
        y_0 = 0.1*BG_SIZE[1] - 0.25*CARD_SIZE[1]
        y_1 = 0.9*BG_SIZE[1] - 0.75*CARD_SIZE[1]
        self.list_coords_1 = [(x_0, y_1), (x_1, y_1), (x_1, y_0), (x_0, y_0)]
        self.score_coords = [(x_0, y_1*0.9), (x_1, y_1*0.9), (x_1, y_0*6), (x_0, y_0*6)]
            
        x = int(BG_SIZE[0]*0.27)
        y = int(BG_SIZE[1]*0.17)
        self.list_coords_forest = [(x, y), (x + _d_, y), (x + _d_, y + _d_), (x, y + _d_)]

        x = int(BG_SIZE[0]*0.49)
        y = int(BG_SIZE[1]*0.12)
        self.list_coords_rock = [(x, y), (x + _d_, y), (x + _d_, y + _d_), (x, y + _d_)]

        x = int(BG_SIZE[0]*0.88)
        y = int(BG_SIZE[1]*0.12)
        self.list_coords_silver = [(x, y), (x + _d_, y), (x + _d_, y + _d_), (x, y + _d_)]

        x = int(BG_SIZE[0]*0.75)
        y = int(BG_SIZE[1]*0.39)
        self.list_coords_gold = [(x, y), (x + _d_, y), (x + _d_, y + _d_), (x, y + _d_)]

        r_x = 33
        r_y = 23
        x = BG_SIZE[0]*0.25
        y = BG_SIZE[1]*0.57
        self.field = (x, y, x + r_x, y + r_y)

        x = BG_SIZE[0]*0.33
        y = BG_SIZE[1]*0.72
        self.hut = [(x, y, x + r_x, y + r_y), (int(x*1.1), y, int(x*1.1) + r_x, y + r_y)]

        x = BG_SIZE[0]*0.51
        y = BG_SIZE[1]*0.53
        self.tool_maker = (x, y, x + r_x, y + r_y)

        x = int(BG_SIZE[0]*0.04)
        y = int(BG_SIZE[1]*0.89)
        self.point_building = []
        for i in range(4):
            self.point_building.append((x, y, x + r_x, y + r_y))
            x += int(BG_SIZE[0]*0.112)

        x = int(BG_SIZE[0]*0.57)
        y = int(BG_SIZE[1]*0.84)
        self.point_civ = []
        for i in range(4):
            self.point_civ.append((x, y, x + r_x, y + r_y))
            x += int(BG_SIZE[0]*0.126)

    def draw_field(self, bg, color):
        ImageDraw.Draw(bg).ellipse(params.field, fill=color)
    def draw_hut(self, bg, color):
        for i in range(2):
            ImageDraw.Draw(bg).ellipse(params.hut[i], fill=color)
    def draw_tool_maker(self, bg, color):
        ImageDraw.Draw(bg).ellipse(params.tool_maker, fill=color)
    def draw_building(self, bg, color):
        for i in range(4):
            ImageDraw.Draw(bg).ellipse(params.point_building[i], fill=color)
    def draw_civ(self, bg, color):
        for i in range(4):
            ImageDraw.Draw(bg).ellipse(params.point_civ[i], fill=color)
    def draw_forest(self, bg, list_count_res):
        for i in range(4):
            ImageDraw.Draw(bg).text(self.list_coords_forest[i], str(list_count_res[i]), fill= sprites.list_color[i], font = sprites.font)
    def draw_rock(self, bg, list_count_res):
        for i in range(4):
            ImageDraw.Draw(bg).text(self.list_coords_rock[i], str(list_count_res[i]), fill= sprites.list_color[i], font = sprites.font)
    def draw_silver(self, bg, list_count_res):
        for i in range(4):
            ImageDraw.Draw(bg).text(self.list_coords_silver[i], str(list_count_res[i]), fill= sprites.list_color[i], font = sprites.font)
    def draw_gold(self, bg, list_count_res):
        for i in range(4):
            ImageDraw.Draw(bg).text(self.list_coords_gold[i], str(list_count_res[i]), fill= sprites.list_color[i], font = sprites.font)

_d_ = BG_SIZE[0] * 0.05
params = Params()
sprites = Sprites()

def draw_cards(bg):
    x = int(BG_SIZE[0]*0.018)
    y = int(BG_SIZE[1]*0.83)
    for i in range(4):
        bg.paste(sprites.cards_building[i], (x, y))
        x += int(BG_SIZE[0]*0.112)

    x = int(BG_SIZE[0]*0.5)
    y = int(BG_SIZE[1]*0.735)
    for i in range(4):
        bg.paste(sprites.card_civilization[i], (x, y))
        x += int(BG_SIZE[0]*0.126)

def get_state_image(state=None):
    background = sprites.background.copy()
    if state is None:
        return background
    draw_cards(background)
    # background.paste(sprites.people, (int(BG_SIZE[0]*0.5), int(BG_SIZE[1]*0.1)))

    # ImageDraw.Draw(background).ellipse(params.field, fill='red')
    color = 'white'
    params.draw_field(background, color)
    params.draw_hut(background, color)
    params.draw_tool_maker(background, color)
    params.draw_building(background, color)
    params.draw_civ(background, color)

    params.draw_forest(background, [1,2 ,3, 4])
    params.draw_rock(background, [1,2 ,3, 4])
    params.draw_silver(background, [1,2 ,3, 4])
    params.draw_gold(background, [1,2 ,3, 4])

    im = Image.new('RGB', SIZE_BOARD, (128, 128, 128))
    print(BG_SIZE)
    im.paste(background, (int((SIZE_BOARD[0]-BG_SIZE[0])/2), int((SIZE_BOARD[1]-BG_SIZE[1])/2)))
    return im

def get_main_player_state(env_components: Env_components, list_agent, list_data, action=None):
    win = -1
    state = _env.getAgentState(env_components.env)
    return win, state, env_components