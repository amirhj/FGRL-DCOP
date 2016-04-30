import sys
from argparser import ArgParser
from factor_graph import FactorGraph
from functions import Functions1
from agent import Agent
from scheduler import Scheduler

print 'Reading options...'
opt_pattern = {'-e': {'name': 'episodes', 'type': 'int', 'default': 200},
               '--alpha': {'name': 'alpha', 'type': 'float', 'default': 0.9},
               '--gamma': {'name': 'gamma', 'type': 'float', 'default': 0.9},
               '--epsilon': {'name': 'epsilon', 'type': 'float', 'default': 0.2},
               '-t': {'name': 'timeout', 'type': 'int', 'default': 200}
               }
arg = ArgParser(sys.argv[2:], opt_pattern)
opt = arg.read()

for o in opt:
    print "\t",o, opt[o]
print

fg = FactorGraph()
func = Functions1(fg)

fg.load(sys.argv[1], func)

print 'Factor graph loaded.'

agents = {}
for v in fg.vars:
    agents[v] = Agent(v, fg, opt, agents)

print "Number of agents:", len(agents)

sch = Scheduler(agents, fg, opt)

sch.init()
sch.run()
sch.terminate()