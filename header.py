EPS = "EPSILON"


class Expression:
    def __init__(self):
        self.param1 = None
        self.param2 = None

    def set_param1(self, param1):
        self.param1 = param1

    def set_param2(self, param2):
        self.param2 = param2

    def get_param1(self):
        return self.param1

    def get_param2(self):
        return self.param2


class Concat(Expression):
    def __str__(self):
        return "Concat(" + self.param1.__str__() + "," + self.param2.__str__() + ")"


class Union(Expression):
    def __str__(self):
        return "Union(" + self.param1.__str__() + "," + self.param2.__str__() + ")"


class Star(Expression):
    def __str__(self):
        return "Star(" + self.param2.__str__() + ")"


class Plus(Expression):
    def __str__(self):
        return "Plus(" + self.param2.__str__() + ")"


class State:
    def __init__(self):
        self.name = "blank"
        self.transitions = []

    def add_t(self, char, next_state):
        self.transitions.append((char, next_state))


class NFA:
    def __init__(self, regex):
        self.states = []
        self.initial = None
        self.final = None
        self.alphabet = set()
        if isinstance(regex, Expression):
            if isinstance(regex, Concat):
                nfa1 = NFA(regex.get_param1())
                nfa2 = NFA(regex.get_param2())
                self.alphabet = set.union(nfa1.alphabet, nfa2.alphabet)
                self.initial = nfa1.get_initial()
                self.final = nfa2.get_final()
                nfa1.get_final().add_t(EPS, nfa2.get_initial())
                self.states.extend(nfa1.get_states())
                self.states.extend(nfa2.get_states())
            elif isinstance(regex, Union):
                nfa1 = NFA(regex.get_param1())
                nfa2 = NFA(regex.get_param2())
                self.alphabet = set.union(nfa1.alphabet, nfa2.alphabet)
                self.initial = State()
                self.final = State()
                self.initial.add_t(EPS, nfa1.get_initial())
                self.initial.add_t(EPS, nfa2.get_initial())
                nfa1.get_final().add_t(EPS, self.final)
                nfa2.get_final().add_t(EPS, self.final)

                self.states.extend(nfa1.get_states())
                self.states.extend(nfa2.get_states())
                self.states.append(self.initial)
                self.states.append(self.final)
            elif isinstance(regex, Star):
                nfa = NFA(regex.get_param2())
                self.alphabet = nfa.alphabet
                self.initial = nfa.get_initial()
                self.final = nfa.get_final()
                nfa.get_initial().add_t(EPS, nfa.get_final())
                nfa.get_final().add_t(EPS, nfa.get_initial())
                self.states.extend(nfa.get_states())
            else:
                nfa = NFA(regex.get_param2())
                self.alphabet = nfa.alphabet
                self.initial = nfa.get_initial()
                self.final = nfa.get_final()
                nfa.get_final().add_t(EPS, nfa.get_initial())
                self.states.extend(nfa.get_states())

        else:
            self.initial = State()
            self.final = State()
            self.initial.add_t(regex, self.final)
            self.states.append(self.initial)
            self.states.append(self.final)
            if regex not in self.alphabet:
                self.alphabet.add(regex)

    def closure(self, states_list, char):
        viz = set()
        stack = []
        ans = []
        if char == EPS:
            for state in states_list:
                viz.add(state)
                stack.append(state)
                ans.append(state)
        else:
            for state in states_list:
                stack.append(state)
        while len(stack) > 0:
            x = stack[len(stack) - 1]
            stack.pop()
            for t in x.transitions:
                if t[0] != char or t[1] in viz:
                    continue
                stack.append(t[1])
                ans.append(t[1])
                viz.add(t[1])

        return sorted(ans, key=my_key)

    def get_states(self):
        return self.states

    def get_initial(self):
        return self.initial

    def get_final(self):
        return self.final

    def name_states(self):
        for i in range(len(self.states)):
            self.states[i].name = i

    def print_nfa(self):
        print(f"Initial state: {self.initial.name}\nFinal state: {self.final.name}")
        for state in self.states:
            for t in state.transitions:
                print(f"State '{state.name}': {t[0], t[1].name}")


class DFA:
    def __init__(self, nfa):
        self.alphabet = str(nfa.alphabet)
        self.states = []
        self.initial = State()
        self.initial.name = nfa.closure([nfa.get_initial()], EPS)
        self.final_states = []

        self.states.append(self.initial)
        if nfa.get_final() in self.initial.name:
            self.final_states.append(self.initial)

        i = 0
        while i < len(self.states):
            for char in nfa.alphabet:
                config = nfa.closure(nfa.closure(self.states[i].name, char), EPS)
                new_state = self.contains_state(config)
                if new_state == False:
                    new_state = State()
                    new_state.name = config
                    self.states.append(new_state)
                    if nfa.get_final() in config:
                        self.final_states.append(new_state)
                self.states[i].add_t(char, new_state)
            i += 1

        for i in range(len(self.states)):
            self.states[i].name = i

    def contains_state(self, name):
        for i in self.states:
            if i.name == name:
                return i
        return False

    def print_dfa(self, fout):
        fout.write(f"Alphabet: {self.alphabet}\n")
        fout.write(f"Number of states: {len(self.states)}\n")
        fout.write(f"Initial state: {self.initial.name.__str__()}\n")
        fout.write(f"Final states: {get_names(self.final_states)}\nTransitions:\n")
        for state in self.states:
            for t in state.transitions:
                fout.write(f"{state.name},'{t[0]}',{t[1].name}\n")


def get_names(l):
    ans = []
    for i in l:
        ans.append(i.name)
    return ans


def my_key(elem):
    return elem.name
