from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import numpy as np
from setup import SHORT_PATH
from Base.Splendor_v2 import _env
IMG_PATH = SHORT_PATH + "Base/Splendor_v2/playing_card_images/"

tl = 3
BG_SIZE = (np.array([2048, 2384])/tl).astype(np.int64)
BOARD_SIZE = (int(BG_SIZE[0]*16/9), BG_SIZE[1])
CARD_SIZE = (np.array([300, 425])/(tl*0.81)).astype(np.int64)
CARD_NOBLE_SIZE = (np.array([300, 300])/(tl*0.81)).astype(np.int64)
TOKEN_SIZE = (int(CARD_SIZE[0]*0.3), int(CARD_SIZE[1]*0.3))
action_description = {
        0: "Bỏ lượt",
        1: "Lấy thẻ thứ 1",
        2: "Lấy thẻ thứ 2",
        3: "Lấy thẻ thứ 3",
        4: "Lấy thẻ thứ 4",
        5: "Lấy thẻ thứ 5",
        6: "Lấy thẻ thứ 6",
        7: "Lấy thẻ thứ 7",
        8: "Lấy thẻ thứ 8",
        9: "Lấy thẻ thứ 9",
        10: "Lấy thẻ thứ 10",
        11: "Lấy thẻ thứ 11",
        12: "Lấy thẻ thứ 12",
        13: "Mở thẻ đang úp thứ 1",
        14: "Mở thẻ đang úp thứ 2",
        15: "Mở thẻ đang úp thứ 3",
        16: "Úp thẻ thứ 1",
        17: "Úp thẻ thứ 2",
        18: "Úp thẻ thứ 3",
        19: "Úp thẻ thứ 4",
        20: "Úp thẻ thứ 5",
        21: "Úp thẻ thứ 6",
        22: "Úp thẻ thứ 7",
        23: "Úp thẻ thứ 8",
        24: "Úp thẻ thứ 9",
        25: "Úp thẻ thứ 10",
        26: "Úp thẻ thứ 11",
        27: "Úp thẻ thứ 12",
        28: "Úp thẻ ẩn loại 1",
        29: "Úp thẻ ẩn loại 2",
        30: "Úp thẻ ẩn loại 3",
        31: "Lấy nguyên liệu red",
        32: "Lấy nguyên liệu blue",
        33: "Lấy nguyên liệu green",
        34: "Lấy nguyên liệu black",
        35: "Lấy nguyên liệu white",
        36: "Trả nguyên liệu red",
        37: "Trả nguyên liệu blue",
        38: "Trả nguyên liệu green",
        39: "Trả nguyên liệu black",
        40: "Trả nguyên liệu white",
        41: "Trả nguyên liệu yellow",
    }

class Env_components:
    def __init__(self, env, winner, list_other, lv1, lv2, lv3) -> None:
        self.env = env
        self.winner = winner
        self.list_other = list_other
        self.lv1 = lv1
        self.lv2 = lv2
        self.lv3 = lv3
        self.cc = 0


def get_description(action):
    if action < 0 or action >= _env.getActionSize():
        return ""
    return f"{action_description[action]}"


def get_env_components():
    env, lv1, lv2, lv3 = _env.initEnv()
    winner = _env.checkEnded(env)
    list_other = np.array([-1, 1, 2, 3])
    np.random.shuffle(list_other)
    env_components = Env_components(env, winner, list_other, lv1, lv2, lv3)
    return env_components


class Sprites:
    def __init__(self) -> None:
        self.font=ImageFont.truetype("Base/SushiGo/font/FreeMonoBoldOblique.ttf", int(120/tl))
        self.font2=ImageFont.truetype("Base/SushiGo/font/FreeMonoBoldOblique.ttf", int(60/tl))

        self.im = Image.new('RGB', BOARD_SIZE, 'black')
        self.background = Image.open(IMG_PATH+"bg.webp").resize(BG_SIZE)
        self.list_token_name = ["red", "blue", "green", "black", "white", "yellow"]

        self.list_img_card = [Image.open(IMG_PATH+f"Cards/{card}.png").resize(CARD_SIZE) for card in range(90)]
        self.list_img_card_noble = [Image.open(IMG_PATH+f"Cards/{card}.png").resize(CARD_NOBLE_SIZE) for card in range(90, 100)]
        self.list_img_card_hide = [Image.open(IMG_PATH+f"Cards/hide_card_{card}.png").resize(CARD_SIZE) for card in range(1, 4)]
        self.list_img_token = [Image.open(IMG_PATH+f"Tokens/{token}.png").resize(TOKEN_SIZE) for token in self.list_token_name]

class Params:
    def __init__(self) -> None:
        pass

_d_ = int(BG_SIZE[0] * 0.02)
params = Params()
sprites = Sprites()

def draw_cards_image(background):
    y = int(BG_SIZE[1]*0.77)
    for d_y in range(4):
        x = int(BG_SIZE[0]*0.01)
        for d_x in range(5):
            if d_y == 3:
                background.paste(sprites.list_img_card_noble[d_x], (x, int(y*2.5)))
            else:
                if d_x == 0:
                    background.paste(sprites.list_img_card_hide[d_y], (x, y))
                else:
                    background.paste(sprites.list_img_card[d_x], (x, y))
            x += CARD_SIZE[0] + _d_
        y -= CARD_SIZE[1] + _d_

def draw_tokens_image(im, 
                      list_token_board = np.full(6, 1),
                      list_token_const = np.full((4, 4), 1),
                      list_token = np.full((4, 5), 1),
                      ):
    for i in range(6):
        x = int(BOARD_SIZE[0]*0.1)
        y = int(BOARD_SIZE[1]*0.1)
        im.paste(sprites.list_img_token[i], (x, y))
        x += TOKEN_SIZE[0] + _d_

    for agent in range(4):
        x = int(BG_SIZE[0]*1.02)
        y = int(BOARD_SIZE[1]*0.1)
        for i in range(5):
            im.paste(sprites.list_img_token[i], (x, y))
            x += TOKEN_SIZE[0] + _d_
    
def draw_line(im, color = 'White', width = 3):
    for i in range(3):
        h = int(im.size[1]/4)*(i+1)
        shape = [(0, h), (im.size[0], h)]
        ImageDraw.Draw(im).line(shape, fill=color, width=width)



def get_state_image(state=None):
    state = state.astype(np.int64)
    background = sprites.background.copy()
    im = sprites.im.copy()
    draw_cards_image(background)

    draw_line(im)
    im.paste(background, (0, 0))
    draw_tokens_image(im)
    return im






def get_main_player_state(env_components: Env_components, list_agent, list_data, action=None):
    state = _env.getAgentState(env_components.env, env_components.lv1, env_components.lv2, env_components.lv3)
    return -1, state, env_components
    # if not action is None:
    #     env_components.env, env_components.all_build_card, env_components.all_civ_card = _env.stepEnv(action, env_components.env, env_components.all_build_card, env_components.all_civ_card)

    # if env_components.winner[0] == -1:
    #     while env_components.cc <= 1000:
    #         idx = np.where(env_components.env[0:4] == 1)[0][0]
    #         if env_components.list_other[idx] == -1:
    #             break

    #         state = _env.getAgentState(env_components.env)
    #         agent = list_agent[env_components.list_other[idx]-1]
    #         data = list_data[env_components.list_other[idx]-1]
    #         action, data = agent(state, data)
    #         env_components.env, env_components.all_build_card, env_components.all_civ_card = _env.stepEnv(action, env_components.env, env_components.all_build_card, env_components.all_civ_card)


    #         env_components.winner = _env.checkEnded(env_components.env)
    #         if env_components.winner[0] != -1:
    #             break
    #         env_components.cc += 1
        
    # if env_components.winner[0] == -1:
    #     state = _env.getAgentState(env_components.env)
    #     win = -1
    # else:
    #     env = env_components.env.copy()

    #     env[82] = 1
    #     my_idx = np.where(env_components.list_other == -1)[0][0]

    #     env[83] = my_idx
    #     env[0:4] = 0
    #     env[my_idx] = 1

    #     state = _env.getAgentState(env)
    #     if my_idx in env_components.winner:
    #         win = 1
    #     else:
    #         win = 0

    #     # Chạy turn cuối cho 3 bot hệ thống
    #     for p_idx in range(4):
    #         if p_idx != my_idx:
    #             env[83] = p_idx
    #             env[0:4] = 0
    #             env[p_idx] = 1
    #             _state = _env.getAgentState(env)
    #             agent = list_agent[env_components.list_other[p_idx]-1]
    #             data = list_data[env_components.list_other[p_idx]-1]
    #             action, data = agent(_state, data)

    return win, state, env_components


#Sửa số người đã đặt/tổng số người
#Thêm chỉ dẫn người chơi chính ok
#Thêm thẻ công cụ dùng 1 lần ok
#Thêm thông tin xúc xắc ok
#Sửa số nền văn minh khác nhau ok
#Thêm thông tin thẻ chọn giá trị xúc xắc ok