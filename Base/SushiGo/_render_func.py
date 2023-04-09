from PIL import Image, ImageEnhance
import numpy as np
from setup import SHORT_PATH
from Base.SushiGo import _env
IMG_PATH = SHORT_PATH + "Base/SushiGo/playing_card_images/"
BG_SIZE = (1680, 720)
CARD_SIZE = (160, 240)


action_description = {
    0 :'Tempura',
    1 :'Sashimi',
    2 :'Dumpling',
    3 :'1 Maki Roll',
    4 :'2 Maki Roll',
    5 :'3 Maki Roll',
    6 :'Salmon Nigiri',
    7 :'Squid Nigiri',
    8 :'Egg Nigiri',
    9 :'Pudding',
    10:'Wasabi',
    11:'Chopsticks',
    12:'Use Chopsticks',
    13:'End Turn',
}

class Env_components:
    def __init__(self, env, winner, list_other, turn, round) -> None:
        self.env = env
        self.list_action = np.full((5, 3), 13)
        self.winner = winner
        self.list_other = list_other
        self.idx = 0
        self.turn = turn
        self.round = round


def get_description(action):
    if action < 0 or action >= _env.getActionSize():
        return ""

    if action == 0:
        return "Skip"

    return f"{action_description[action]}"


def get_env_components():
    env = _env.initEnv(5)
    winner = _env.winner_victory(env)
    list_other = np.array([-1, 1, 2, 3, 4])
    np.random.shuffle(list_other)
    turn = env[1]
    round = env[0]-1
    env_components = Env_components(env, winner, list_other, turn, round)
    return env_components


def get_main_player_state(env_components: Env_components, list_agent, list_data, action=None):
    amount_player = 5
    if not action is None:
        env_components.list_action[env_components.idx][env_components.count] = action
        env_components.env = _env.stepEnv(env_components, env_components.list_action, amount_player, env_components.turn, env_components.round)


    turn = env_components.env[1]
    check_end_game = False
    
    check_break = True
    while turn<7*3:
        round = env_components.env[0]-1
        turn = env_components.env[1]
        env_components.list_action = np.full((amount_player, 3), 13)
        for idx in range(amount_player):
            env_components.idx = idx
            player_state = _env.getAgentState(env_components.env,idx)
            count = 0
            while player_state[-1] +  player_state[-2] > 0:
                if env_components.list_other[idx] == -1:
                    check_break = False
                    break
                agent = list_agent[env_components.list_other[idx]-1]
                data = list_data[env_components.list_other[idx]-1]
                action, data = agent(player_state, data)
                env_components.list_action[idx][count] = action
                count += 1
                player_state = _env.test_action(player_state,action)
            if check_break == False:
                break
        if check_break == False:
            break
        env_components.env = _env.stepEnv(env_components.env,env_components.list_action,amount_player,turn,round)

        if turn % 7 == 0:
            env_components.env = _env.caculater_score(env_components.env,amount_player)
            if env_components.env[0] < 3:
                env_components.env[0] += 1
                env_components.env = _env.reset_card_player(env_components.env)
        if turn == 7*3:
            env_components.env = _env.caculator_pudding(env_components.env,amount_player)
        if turn <= 7*3:
            env_components.env[1] += 1

    env_components.winner = _env.winner_victory(env_components.env)

    if check_end_game == False:
        state = _env.getAgentState(env_components.env,env_components.idx)
        win = -1
    else:
        my_idx = np.where(env_components.list_other == -1)[0][0]
        env = env_components.env.copy()

        state = _env.getAgentState(env_components.env,env_components.idx)
        if my_idx == env_components.winner:
            win = 1
        else:
            win = 0

        # Chạy turn cuối cho 3 bot hệ thống
        for idx in range(amount_player):
            if idx != my_idx:
                _state = _env.getAgentState(env, idx)
                agent = list_agent[env_components.list_other[idx]-1]
                data = list_data[env_components.list_other[idx]-1]
                action, data = agent(_state, data)

    return win, state, env_components

class Sprites:
    def __init__(self) -> None:
        self.background = Image.open(IMG_PATH+"background.png").resize(BG_SIZE)
        card_values = ["3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "2"]
        card_suits = ["Spade"]
        self.cards = []
        for value in card_values:
            for suit in card_suits:
                self.cards.append(Image.open(IMG_PATH+f"{value}-{suit}.png").resize(CARD_SIZE))

        self.card_back = Image.open(IMG_PATH+"Card_back.png").resize(CARD_SIZE)
        self.faded_card_back = self.card_back.copy()
        br = ImageEnhance.Brightness(self.faded_card_back)
        self.faded_card_back = br.enhance(0.5)
        ct = ImageEnhance.Contrast(self.faded_card_back)
        self.faded_card_back = ct.enhance(0.5)

class Params:
    def __init__(self) -> None:
        self.center_card_x = BG_SIZE[0] * 0.5
        self.center_card_y = (BG_SIZE[1] - CARD_SIZE[1]) * 0.5
        self.list_coords_0 = [
            (self.center_card_x, 0.92*BG_SIZE[1] - CARD_SIZE[1]),
            (0.82*BG_SIZE[0], self.center_card_y),
            (self.center_card_x, 0.08*BG_SIZE[1]),
            (0.18*BG_SIZE[0], self.center_card_y)
        ]

        x_0 = BG_SIZE[0] * 0.32
        x_1 = BG_SIZE[0] * 0.68
        y_0 = 0.2*BG_SIZE[1] - 0.25*CARD_SIZE[1]
        y_1 = 0.8*BG_SIZE[1] - 0.75*CARD_SIZE[1]
        self.list_coords_1 = [(x_0, y_1), (x_1, y_1), (x_1, y_0), (x_0, y_0)]

params = Params()
sprites = Sprites()

def draw_cards(bg, cards, s, y, back=False, faded=False):
    n = cards.shape[0]
    y = round(y)
    if back:
        if faded:
            im = sprites.faded_card_back
        else:
            im = sprites.card_back

        for i in range(n):
            bg.paste(im, (round(s+_d_*i), y))
    else:
        id_card = 1
        for card in range(12):
            total_cards = cards[card]
            while total_cards > 0:
                bg.paste(sprites.cards[card], (round(s+_d_*id_card), y))
                total_cards -= 1
                id_card += 1

_d_ = CARD_SIZE[0] * 0.2
def get_state_image(state=None):
    background = sprites.background.copy()
    if state is None:
        return background
    else:
        n = np.sum(state[2:14])
        w = CARD_SIZE[0] + _d_ * (n-1)
        s = params.list_coords_0[0][0] - 0.5*w  
        print((round(s+_d_*1), int(params.list_coords_0[0][1])))
        print(state[2:14])
        draw_cards(background, state[2:14], s, params.list_coords_0[0][1])

    # list_cards_played = np.array_split(cards_played, 4)
    for k in range(4):
        # n = list_cards_played[k].shape[0]
        list_cards_played = state[14*(k+1):14*(k+1)+14]
        n = np.sum(list_cards_played)
        w = CARD_SIZE[0] + _d_ * (n-1)
        s = params.list_coords_1[k][0] - 0.5*w
        draw_cards(background, list_cards_played, s, params.list_coords_1[k][1])

        return background