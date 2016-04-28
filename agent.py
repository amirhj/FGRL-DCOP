from util import Counter
import random, util


class Agent:

    def __init__(self, name, fg, opt, agnets):
        self.fg = fg
        self.opt = opt
        self.name = name
        self.agents = agnets

        self.qvalues = util.Counter()
        self.last_action = 'hold'

    def get_actions(self):
        actions = ['dec', 'hold', 'inc']
        if self.fg.vars[self.name]['value'] == 0:
            del actions[0]
        if self.fg.vars[self.name]['value'] == self.fg.vars[self.name]['size'] - 1:
            del actions[1]
        return actions

    def get_state(self):
        state = []
        for f in self.fg.vars[self.name]['functions']:
            state.append(self.fg.get_value(f))
        return tuple(state)

    def policy(self, state):
        actions = self.get_actions()
        max_q = None
        for a in actions:
            action_profile = self.get_actions_profile(a)
            q = (state,) + action_profile
            if (max_q is None) or (max_q < self.qvalues[q]):
                max_q = self.qvalues[q]
                max_action = a

        other_actions = self.get_actions()
        del other_actions[other_actions.index(max_action)]

        if util.flipCoin(self.opt['epsilon']):
            return random.choice(other_actions)
        return max_action

    def reward(self, state, action_profile, next_state):
        diff = sum(next_state) - sum(state)
        action = action_profile[0]
        if (diff > 0 and action == 'inc') or (diff < 0 and action == 'dec')\
                or (diff == 0 and action == 'hold'):
            r = 0.1
        else:
            r = -0.1
        return r

    def commit(self, action):
        if action == 'inc':
            self.fg.vars[self.name]['value'] += 1
        elif action == 'dec':
            self.fg.vars[self.name]['value'] -= 1

        self.last_action = action

    def update(self, state, action_profile, next_state, reward):
        qstate = (state, ) + action_profile
        next_qstate = qstate
        sample = reward + self.opt['gamma'] * max(next_qstate)
        self.qvalues[qstate] = (1 - self.opt['alpha']) * self.qvalues[qstate] + self.opt['alpha'] * sample

    def is_terminated(self):
        return False

    def get_actions_profile(self, action):
        actions = [action]
        for a in self.fg.get_neighbour_variables(self.name):
            actions.append(self.agents[a].last_action)
        return tuple(actions)

    def run(self):
        state = self.getState()
        action = self.policy(state)
        self.commit(action)
        next_state = self.getState()
        action_profile = self.get_actions_profile(action)
        reward = self.reward(state, action_profile, next_state)
        self.update(state, action_profile, next_state, reward)
