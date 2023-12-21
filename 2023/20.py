words2 = '''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''

words3 = '''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''
from collections import deque, defaultdict
import math


class Module:
    pulse_counter = {0: 0, 1: 0}

    def __init__(self, module_name='', output_modules=None):
        self.name = module_name
        self.output_modules = output_modules

    def update_input_memory(self, input_module, memory=0):
        pass

    def send(self, in_module, pulse, pulses_queue):
        Module.pulse_counter[pulse] += 1


class FlipFlopModule(Module):

    def __init__(self, module_name, output_modules):
        super().__init__(module_name, output_modules)
        self.is_on = False

    def send(self, in_module, pulse, pulses_queue):
        Module.pulse_counter[pulse] += 1
        if pulse:
            return
        self.is_on = not self.is_on
        for output_module in self.output_modules:
            pulses_queue.appendleft((self.name, int(self.is_on), output_module))


class ConjunctionModule(Module):
    def __init__(self, module_name, output_modules):
        super().__init__(module_name, output_modules)
        self.input_module_memory = dict()

    def update_input_memory(self, input_module, memory=0):
        self.input_module_memory[input_module] = memory

    def send(self, in_module, pulse, pulses_queue):
        Module.pulse_counter[pulse] += 1
        self.update_input_memory(in_module, pulse)
        low_in_memory = not (all(self.input_module_memory.values()))
        for output_module in self.output_modules:
            pulses_queue.appendleft((self.name, int(low_in_memory), output_module))


class BroadcasterModule(Module):
    def send(self, in_module, pulse, pulses_queue):
        Module.pulse_counter[pulse] += 1
        for output_module in self.output_modules:
            pulses_queue.appendleft((self.name, pulse, output_module))


def module_factory(module_str):
    in_module_str, output_modules_str = module_str.split(' -> ')
    if in_module_str[0] == '%':
        return FlipFlopModule(in_module_str[1:], output_modules_str.split(', '))
    if in_module_str[0] == '&':
        return ConjunctionModule(in_module_str[1:], output_modules_str.split(', '))
    return BroadcasterModule(in_module_str, output_modules_str.split(', '))


def parse_input(words):
    modules_dict = defaultdict(Module)
    for w in words.split('\n'):
        module = module_factory(w)
        modules_dict[module.name] = module
    for module_name, module in modules_dict.items():
        for out_module_name in module.output_modules:
            if out_module_name in modules_dict:
                modules_dict[out_module_name].update_input_memory(module_name)

    return modules_dict


def calculate_pulses_multiply(words, nb_button_pushes):
    modules_dict = parse_input(words)
    for _ in range(nb_button_pushes):
        # low pulses = 0, high pulses = 1
        pulses_queue = deque([(None, 0, 'broadcaster')])
        while len(pulses_queue) > 0:
            in_module, pulse, module_name = pulses_queue.pop()
            modules_dict[module_name].send(in_module, pulse, pulses_queue)
    nb_low_pulses = Module.pulse_counter[0]
    nb_high_pulses = Module.pulse_counter[1]
    return nb_low_pulses * nb_high_pulses


def calculate_min_button_presses_single_low(words):
    modules_dict = parse_input(words)
    nb_button_pushes = 200000
    zs_send_1 = []
    # the puzzle data was so that the 'rx would receive a low pulse iff
    # the 4 conjunction modules below would send a low pulse
    # which means that all of their incoming modules need to have last emitted high pulse.
    # From experimentation, it turns out that each of the below modules emit a low pulse periodically.
    period_dict = {'zs': 0, 'nt': 0, 'ff': 0, 'th': 0}
    i = 0
    while not all(period_dict.values()):
        i += 1
        # low pulses = 0, high pulses = 1
        pulses_queue = deque([(None, 0, 'broadcaster')])
        while len(pulses_queue) > 0:
            in_module, pulse, module_name = pulses_queue.pop()
            modules_dict[module_name].send(in_module, pulse, pulses_queue)
            if (module_name in period_dict) and (all(modules_dict[module_name].input_module_memory.values())):
                if period_dict[module_name] == 0:
                    period_dict[module_name] = i
    return math.lcm(*list(period_dict.values()))


print(calculate_pulses_multiply(words, 1000))
print(calculate_min_button_presses_single_low(words))