import numpy as np 
from collections import Counter 

import math, random

global signs, last_react_action, configuration
signs = 3
configuration = [0, 1, 2]

def get_score(left_move, right_move):
    # This method exists in this file so it can be consumed from rps.py and agents.py without a circular dependency
    delta = (
        right_move - left_move
        if (left_move + right_move) % 2 == 0
        else left_move - right_move
    )
    return 0 if delta == 0 else math.copysign(1, delta)


def rock(lastOpponentAction):
    return 0


def paper(lastOpponentAction):
    return 1


def scissors(lastOpponentAction):
    return 2


def copy_opponent(lastOpponentAction, step):

	if step > 0:
		return lastOpponentAction
	else:
		return random.randrange(0, 3)

last_react_action = None

def reactionary(lastOpponentAction, step):
	global last_react_action
	if step == 0:
		last_react_action = random.randrange(0, 3)
	elif get_score(last_react_action, lastOpponentAction) <= 1:
		last_react_action = (lastOpponentAction + 1) % 3

	return last_react_action


last_counter_action = random.randrange(0, signs)


def counter_reactionary(lastOpponentAction, step):
	global last_counter_action
	if step == 0:
		last_counter_action = random.randrange(0, 3)
	elif get_score(last_counter_action, lastOpponentAction) == 1:
		last_counter_action = (last_counter_action + 2) % 3
	else:
		last_counter_action = (lastOpponentAction + 1) % 3

	return last_counter_action


action_histogram = {}


def statistical(lastOpponentAction, step):
	global action_histogram
	if step == 0:
		action_histogram = {}
		#return
	action = lastOpponentAction
	if action not in action_histogram:
		action_histogram[action] = 0
	action_histogram[action] += 1
	mode_action = None
	mode_action_count = None
	for k, v in action_histogram.items():
		if mode_action_count is None or v > mode_action_count:
			mode_action = k
			mode_action_count = v
			continue

	return (mode_action + 1) % 3


agents = {
    "rock": rock,
    "paper": paper,
    "scissors": scissors,
    "copy_opponent": copy_opponent,
    "reactionary": reactionary,
    "counter_reactionary": counter_reactionary,
    "statistical": statistical
}