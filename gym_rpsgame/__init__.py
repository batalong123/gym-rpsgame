from gym.envs.registration import register

register(id='rps-v0', entry_point='gym_rpsgame.envs:RockPaperScissorsEnv')
register(id='rps-v1', entry_point='gym_rpsgame.envs:RockPaperScissorsTournmentEnv')