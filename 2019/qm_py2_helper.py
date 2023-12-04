import qm
import sys

my_qm = qm.QM(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
min_terms = [int(x) for x in sys.argv[1].split(',')]
dc_terms = [int(x) for x in sys.argv[2].split(',')]
minimized_min_terms = my_qm.solve(min_terms, dc_terms)[1]
formula = my_qm.get_function(minimized_min_terms)
#print minimized_min_terms
print formula
