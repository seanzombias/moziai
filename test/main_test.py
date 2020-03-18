import pylog
from Iraq_learn import etc
from Iraq_learn.env import MoziEnv
from MoziService.paser_core import get_all_sides_dic

env = MoziEnv(etc.SERVER_IP, etc.SERVER_PORT, etc.SCENARIO_NAME, etc.simulate_compression)
if not env.connect_server():
    pylog.info("can not connect to server")
else:
    # ret = env.mozi_service.suspend_simulate()
    # env.mozi_service.all_info_dict = {}
    # env.scenario = env.mozi_service.load_scenario(plat=env.SERVER_PLAT)
    # env._set_duration_interval()
    #
    # env.mozi_service.set_run_mode()
    # env.mozi_service.set_simulate_compression(env.simulate_compression)
    # env.mozi_service.set_compression_mode(False)

    # env._run_simulate()

    all_info_dic = env.reset()
    print(all_info_dic)

