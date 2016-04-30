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
            del actions[2]
        print self.fg.vars[self.name]['value'], actions
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
        if self.is_terminated():
            r = 2.0
        else:
            action = action_profile[0]
            adiff = sum(next_state) - sum(state)

            if action == 'inc':
                self.fg.vars[self.name]['value'] -= 1
                actions = self.get_actions()
                self.fg.vars[self.name]['value'] += 1
                del actions[actions.index('inc')]
            elif action == 'dec':
                self.fg.vars[self.name]['value'] += 1
                actions = self.get_actions()
                self.fg.vars[self.name]['value'] -= 1
                del actions[actions.index('dec')]
            else:
                actions = self.get_actions()
                del actions[actions.index('hold')]

            r = 0.1
            for a in actions:
                s = self.simulate(a)
                diff = sum(s) - sum(state)
                if diff > adiff:
                    r = -0.1
                    # print 'best is', a
                    break
        return r

    def commit(self, action):
        if action == 'inc':
            self.fg.vars[self.name]['value'] += 1
        elif action == 'dec':
            self.fg.vars[self.name]['value'] -= 1

        self.last_action = action

    def simulate(self, action):
        if action == 'inc':
            self.fg.vars[self.name]['value'] += 1
            state = self.get_state()
            self.fg.vars[self.name]['value'] -= 1

        elif action == 'dec':
            self.fg.vars[self.name]['value'] -= 1
            state = self.get_state()
            self.fg.vars[self.name]['value'] += 1
        else:
            state = self.get_state()

        return state

    def update(self, state, action_profile, next_state, reward):
        qstate = (state, ) + action_profile
        sample = reward + self.opt['gamma'] * self.get_best_responce(next_state)
        self.qvalues[qstate] = (1 - self.opt['alpha']) * self.qvalues[qstate] + self.opt['alpha'] * sample

    def is_terminated(self):
        actions = self.get_actions()
        state = self.get_state()
        terminate = True
        if 'inc' in actions:
            self.fg.vars[self.name]['value'] += 1
            next_state = self.get_state()
            self.fg.vars[self.name]['value'] -= 1
            diff = sum(next_state) - sum(state)
            if diff > 0:
                terminate = False
        elif 'dec' in actions:
            self.fg.vars[self.name]['value'] -= 1
            next_state = self.get_state()
            self.fg.vars[self.name]['value'] += 1
            diff = sum(next_state) - sum(state)
            if diff > 0:
                terminate = False
        return terminate

    def get_actions_profile(self, action):
        actions = [action]
        for a in self.fg.get_neighbour_variables(self.name):
            actions.append(self.agents[a].last_action)
        return tuple(actions)

    def run(self):
        state = self.get_state()
        # print "state:", state
        action = self.policy(state)
        # print "action:", action
        self.commit(action)
        # print "commit"
        next_state = self.get_state()
        # print "next state:", next_state
        action_profile = self.get_actions_profile(action)
        # print "action profile:", action_profile
        reward = self.reward(state, action_profile, next_state)
        # print "reward:", reward
        self.update(state, action_profile, next_state, reward)

    def get_best_responce(self, state):
        agents = []
        action_indices = util.Counter()
        agents_actions = {}
        for a in self.fg.get_neighbour_variables(self.name):
            agents_actions[a] = self.agents[a].get_actions()
            agents.append(a)

        cartesian = []
        while action_indices[agents[0]] < len(agents_actions[agents[0]]):
            dec = []
            for v in agents:
                dec.append(agents_actions[v][action_indices[v]])
            cartesian.append(tuple(dec))

            for i in reversed(agents):
                if action_indices[i] < len(agents_actions[i]):
                    action_indices[i] += 1
                    if action_indices[i] == len(agents_actions[i]):
                        if i != agents[0]:
                            action_indices[i] = 0
                    else:
                        break

        max_q = None
        for c in cartesian:
            qstate = (state, ) + c
            if max_q is None or self.qvalues[qstate] > max_q:
                max_q = self.qvalues[qstate]

        return max_q
