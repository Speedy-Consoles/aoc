use std::io;

const NUM_CUPS: usize = 1_000_000;

fn make_move(nexts: &mut [u32], current: u32) -> u32 {
	let first_selected = nexts[current as usize];
	let middle_selected = nexts[first_selected as usize];
	let last_selected = nexts[middle_selected as usize];
	let new_current = nexts[last_selected as usize];

	let selected = [ first_selected, middle_selected, last_selected ];
	let mut destination = (current + NUM_CUPS as u32 - 1) % NUM_CUPS as u32;
	while selected.contains(&destination) {
		destination = (destination + NUM_CUPS as u32 - 1) % NUM_CUPS as u32;
	}
	let after_destination = nexts[destination as usize];

	nexts[destination as usize] = first_selected;
	nexts[last_selected as usize] = after_destination;
	nexts[current as usize] = new_current;

	new_current
}

fn main() {
	// create connections
	let mut nexts: Vec<u32> = (0..NUM_CUPS as u32).map(|i| i + 1 % NUM_CUPS as u32).collect();

	// change connections for given cups
	let mut line = String::new();
	io::stdin().read_line(&mut line).unwrap();
	let given_cups = line.trim();
	let mut prev_label = NUM_CUPS as u32 - 1;
	for c in given_cups.chars() {
		let current_label = c.to_digit(10).unwrap() - 1;
		nexts[prev_label as usize] = current_label;
		prev_label = current_label;
	}
	nexts[prev_label as usize] = given_cups.len() as u32;

	// execute moves
	let mut current = nexts[NUM_CUPS - 1];
	for _ in 0..10_000_000 {
		current = make_move(nexts.as_mut(), current);
	}

	println!("{}", (nexts[0] as u64 + 1) * (nexts[nexts[0] as usize] as u64 + 1));
}
