use std::collections::HashMap;

use lib::twentyfour::*;

fn get_value(cable: &str, values: &HashMap<String, bool>, gates: &HashMap<String, Operation>) -> Option<bool> {
	values.get(cable).copied().or_else(||
		gates.get(cable).and_then(|operation|
			get_value(operation.operands()[0], values, gates)
				.zip(get_value(operation.operands()[1], values, gates))
				.map(|(value_1, value_2)| operation.operator().apply(value_1, value_2))
		)
	)
}

fn main() {
	let (values, gates) = parse_input();

	let result = (0..)
		.map_while(|i| get_value(&get_numbered_cable('z', i), &values, &gates).map(|value| (value as usize) << i))
		.sum::<usize>();

	println!("{}", result);
}
