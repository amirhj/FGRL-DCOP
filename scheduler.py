class Scheduler:
    def __init__(self, agents, fg, opt):
        self.agents = agents
        self.fg = fg
        self.opt = opt

    def init(self):
        pass

    def run(self):
        timeout = self.opt['timeout']
        for i in range(self.opt['episodes']):
            print "Episode", i+1, ":",
            terminated = False
            t = 0
            while (not terminated) and (t < timeout):
                terminated = True
                for a in self.agents:
                    agent = self.agents[a]
                    agent.run()
                    terminated = terminated and agent.is_terminated()

                t += 1

            if t == timeout:
                print "Timeout"
            else:
                print

    def terminate(self):
        pass
