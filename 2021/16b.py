from math import prod
from operator import lt, gt, eq


class BitStream:
	def __init__(self, hex_message):
		self.binary_message = ''.join('{:04b}'.format(int(x, 16)) for x in hex_message)
		self.index = 0

	def pop(self, num_bits, as_string=False):
		result = self.binary_message[self.index:self.index+num_bits]
		if not as_string:
			result = int(result, 2)
		self.index += num_bits
		return result

	def cursor_position(self):
		return self.index


PACKET_TYPE_ID_LITERAL = 4

LENGTH_TYPE_ID_BY_SIZE = 0
# LENGTH_TYPE_ID_BY_NUM = 1

OPERATORS = {
	0: sum,
	1: prod,
	2: min,
	3: max,
	5: lambda x: int(gt(*x)),
	6: lambda x: int(lt(*x)),
	7: lambda x: int(eq(*x)),
}


def evaluate_packet(stream):
	stream.pop(3)  # packet version
	packet_type_id = stream.pop(3)
	if packet_type_id == PACKET_TYPE_ID_LITERAL:
		literal_string = ''
		go_on = True
		while go_on:
			go_on = stream.pop(1) == 1
			literal_string += stream.pop(4, True)
		literal = int(literal_string, 2)
		return literal
	else:  # operator
		values = []
		length_type_id = stream.pop(1)
		if length_type_id == LENGTH_TYPE_ID_BY_SIZE:
			total_length = stream.pop(15)
			start_cursor_position = stream.cursor_position()
			while stream.cursor_position() - start_cursor_position < total_length:
				values.append(evaluate_packet(stream))
		else:  # LENGTH_TYPE_ID_BY_NUM
			num_sub_packets = stream.pop(11)
			for i in range(num_sub_packets):
				values.append(evaluate_packet(stream))

		return OPERATORS[packet_type_id](values)


stream = BitStream(input())
print(evaluate_packet(stream))
