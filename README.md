# Regex-DFA
Transforms a regex into a DFA

main.py receives 2 parameters: <input_file> <output_file>
The input file must contain a regex in prenex form.
Example of prenex form:
1) STAR UNION CONCAT a b CONCAT b STAR d = (ab|bd*)*
2) CONCAT PLUS c UNION a PLUS b = c+(a|b+)

The output file has the following format:
<alphabet>
<number_of_states>
<initial_state>
<list_of_final_states>
<transition_1>
<transition_2>
...
<transition_n>
