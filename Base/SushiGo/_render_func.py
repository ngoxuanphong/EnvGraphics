from PIL import Image, ImageEnhance
import numpy as np
from setup import SHORT_PATH
from Base.SushiGo import _env
IMG_PATH = SHORT_PATH + "Base/SushiGo/playing_card_images/"
BG_SIZE = (1680, 720)
CARD_SIZE = (80, 112)


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
                    break
                agent = list_agent[env_components.list_other[idx]-1]
                data = list_data[env_components.list_other[idx]-1]
                action, data = agent(player_state, data)
                env_components.list_action[idx][count] = action
                count += 1
                player_state = _env.test_action(player_state,action)
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
        card_suits = ["Spade", "Club", "Diamond", "Heart"]
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
sprites = Sprites()

def get_state_image(state=None):
    background = sprites.background.copy()
    if state is None:
        return background