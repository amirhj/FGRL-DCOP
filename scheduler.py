import util, json, os, time


class Scheduler:
    def __init__(self, agents, fg, opt):
        self.agents = agents
        self.fg = fg
        self.opt = opt
        self.log = {}

    def init(self):
        for a in self.agents:
            self.log[a] = []

    def run(self):
        timeout = self.opt['timeout']
        for i in range(self.opt['episodes']):
            print "Episode", i+1, ":",

            t = 0
            while True:
                for a in self.agents:
                    agent = self.agents[a]
                    # print "\tagent", agent.name
                    agent.run()
                    self.log[a].append(self.fg.vars[a]['value'])
                t += 1

                if self.is_terminated() or (t == timeout):
                    break

            if t == timeout:
                print "Timeout"
            else:
                print

    def terminate(self):
        result = {'options': self.opt, 'result': {}}

        indices = util.Counter()
        variables = self.fg.vars.keys()

        for v in self.fg.vars:
            result['result'][v] = self.fg.vars[v]['value']

        max_sum = None
        max_vars = None
        while indices[variables[0]] < len(self.fg.vars[variables[0]]['domain']):
            dec = {}
            for v in variables:
                dec[v] = indices[v]
                self.fg.vars[v]['value'] = dec[v]

            totall_sum = 0
            for f in self.fg.funcs.keys():
                totall_sum += self.fg.get_value(f)

            if max_sum is None or max_sum < totall_sum:
                max_sum = totall_sum
                max_vars = dec

            for i in reversed(variables):
                if indices[i] < len(self.fg.vars[i]['domain']):
                    indices[i] += 1
                    if indices[i] == len(self.fg.vars[i]['domain']):
                        if i != variables[0]:
                            indices[i] = 0
                    else:
                        break

        result['optimal'] = max_vars

        folder = 'results/'+time.asctime(time.localtime(time.time()))
        os.mkdir(folder)

        res = open(folder+'/result.txt', 'w')
        res.write(json.dumps(result, indent=4))
        res.close()

        for a in self.log:
            i = 1
            l = open(folder+'/'+a+'.txt', 'w')
            for r in self.log[a]:
                l.write("%d %d\n" % (i,r))
                i += 1
            l.close()

    def is_terminated(self):
        terminated = True
        for a in self.agents:
            agent = self.agents[a]
            if not agent.is_terminated():
                terminated = False
                break
        return terminated