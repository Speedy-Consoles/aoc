class BitStream:
	def __init__(self, hex_message):
		self.binary_message = ''.join('{:04b}'.format(int(x, 16)) for x in hex_message)
		self.index = 0

	def pop(self, num_bits):
		result = int(self.binary_message[self.index:self.index+num_bits], 2)
		self.index += num_bits
		return result

	def cursor_position(self):
		return self.index


PACKET_TYPE_ID_LITERAL = 4

LENGTH_TYPE_ID_BY_SIZE = 0
# LENGTH_TYPE_ID_BY_NUM = 1


def evaluate_packet(stream):
	packet_version = stream.pop(3)
	packet_type_id = stream.pop(3)
	result = packet_version
	if packet_type_id == PACKET_TYPE_ID_LITERAL:
		go_on = True
		while go_on:
			go_on = stream.pop(1) == 1
			stream.pop(4)
	else:  # operator
		length_type_id = stream.pop(1)
		if length_type_id == LENGTH_TYPE_ID_BY_SIZE:
			total_length = stream.pop(15)
			start_cursor_position = stream.cursor_position()
			while stream.cursor_position() - start_cursor_position < total_length:
				result += evaluate_packet(stream)
		else:  # LENGTH_TYPE_ID_BY_NUM
			num_sub_packets = stream.pop(11)
			for i in range(num_sub_packets):
				result += evaluate_packet(stream)

	return result


stream = BitStream(input())
print(evaluate_packet(stream))
