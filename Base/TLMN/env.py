from Base.TLMN import _env as __env
from Base.TLMN._render import Render as __Render
from numba.core.errors import NumbaPendingDeprecationWarning as __NumbaPendingDeprecationWarning
import warnings as __warnings
__warnings.simplefilter("ignore", __NumbaPendingDeprecationWarning)


getValidActions = __env.getValidActions
getActionSize = __env.getActionSize
getAgentSize = __env.getAgentSize
getStateSize = __env.getStateSize
getReward = __env.getReward
numba_main_2 = __env.numba_main_2


def render(Agent, per_data, level, *args, max_temp_frame=100):
    list_agent, list_data = __env.load_agent(level, *args)

    global __render
    __render = __Render(Agent, per_data, list_agent, list_data, max_temp_frame)
    return __render.render()

def get_data_from_visualized_match():
    if "_render" not in globals():
        print("Nothing to get, visualize the match before running this function")
        return None
    else:
        return {
            "history_state": __render.history_state,
            "history_action": __render.history_action,
        }