from setup import make
from Base.TLMN._env import bot_lv0
env = make("TLMN")
env.render(Agent="human", per_data=[0], level=0, max_temp_frame=100)