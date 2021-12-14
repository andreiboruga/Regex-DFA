from header import *
import sys


def parse_word(i, regex_elements, regex_len, keywords, stack, stack_size, result):
    if i == regex_len:
        return result
    if regex_elements[i] in keywords:
        if regex_elements[i] == "CONCAT":
            stack.append([Concat(), 2])
        elif regex_elements[i] == "UNION":
            stack.append([Union(), 2])
        elif regex_elements[i] == "STAR":
            stack.append([Star(), 1])
        else:
            stack.append([Plus(), 1])
        stack_size += 1
    else:
        if stack[stack_size - 1][1] == 1:
            stack[stack_size - 1][0].set_param2(regex_elements[i])
            result = stack[stack_size - 1][0]
            stack.pop()
            stack_size -= 1
            while stack_size > 0 and stack[stack_size - 1][1] == 1:
                stack[stack_size - 1][0].set_param2(result)
                result = stack[stack_size - 1][0]
                stack.pop()
                stack_size -= 1
            if stack_size > 0:
                stack[stack_size - 1][1] = 1
                stack[stack_size - 1][0].set_param1(result)
        else:
            stack[stack_size - 1][1] = 1
            stack[stack_size - 1][0].set_param1(regex_elements[i])
    return parse_word(i + 1, regex_elements, regex_len, keywords, stack, stack_size, result)



regex_elements = open(sys.argv[1], "r").read().split()
out_file = open(sys.argv[2], "w")

regex_len = len(regex_elements)
keywords = ["CONCAT", "STAR", "UNION", "PLUS"]

regex = None

if regex_len > 1:
    regex = parse_word(0, regex_elements, regex_len, keywords, [], 0, None)
else:
    regex = regex_elements[0]

nfa = NFA(regex)
nfa.name_states()

dfa = DFA(nfa)
dfa.print_dfa(out_file)
