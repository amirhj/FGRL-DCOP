import sys
from argparser import ArgParser
from factor_graph import FactorGraph
from functions import Functions1
from agent import Agent
from scheduler import Scheduler

opt_pattern = {}
arg = ArgParser(sys.argv[2:], opt_pattern)
opt = arg.read()

fg = FactorGraph()
func = Functions1(fg)

fg.load(sys.argv[0], func)

agents = []
for v in fg.vars:
    agents[v] = Agent(v, fg, opt, agents)

sch = Scheduler(agents, fg, opt)

sch.init()
sch.run()
sch.terminate()