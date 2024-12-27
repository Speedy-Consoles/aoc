use std::{
	collections::HashMap,
	io::{
		self,
		Read,
	},
	str::FromStr,
};

use regex::Regex;

#[derive(Debug, Copy, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Operator {
	And,
	Or,
	Xor,
}

impl Operator {
	pub fn apply(&self, left: bool, right: bool) -> bool {
		match *self {
			Self::And => left && right,
			Self::Or => left || right,
			Self::Xor => left != right,
		}
	}
}

impl FromStr for Operator {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
		match s {
			"AND" => Ok(Self::And),
			"OR" => Ok(Self::Or),
			"XOR" => Ok(Self::Xor),
			_ => Err(())
		}
	}
}

fn minmax(a: String, b: String) -> [String; 2] {
	if a <= b {
		[a, b]
	} else {
		[b, a]
	}
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Operation {
	operator: Operator,
	operands: [String; 2],
}

impl Operation {
	pub fn new(operator: Operator, operand_1: String, operand_2: String) -> Self {
		// TODO use cmp::minmax (https://github.com/rust-lang/rust/issues/115939)
		Self {
			operator,
			operands: minmax(operand_1, operand_2),
		}
	}

	pub fn operator(&self) -> Operator {
		self.operator
	}

	pub fn operands(&self) -> [&str; 2] {
		self.operands.each_ref().map(String::as_str)
	}
}

pub fn get_numbered_cable(v: char, i: usize) -> String {
	format!("{}{:02}", v, i)
}

pub fn parse_input() -> (HashMap<String, bool>, HashMap<String, Operation>) {
	let input_regex = Regex::new(r"([[:alnum:]]{3}): (0|1)").unwrap();
	let gate_regex = Regex::new(r"([[:alnum:]]{3}) (AND|OR|XOR) ([[:alnum:]]{3}) -> ([[:alnum:]]{3})").unwrap();
	let mut s = String::new();
	io::stdin().read_to_string(&mut s).unwrap();
	let [inputs_string, gates_string] = s.split("\n\n").collect::<Vec<_>>().try_into().unwrap();
	let values = inputs_string.lines().map(|line| {
		let [input, value_string] = input_regex.captures(line).unwrap().extract().1;
		(input.to_string(), value_string.parse::<u8>().unwrap() != 0)
	}).collect();
	let gates = gates_string.lines().map(|line| {
		let [input_1, operator, input_2, output] = gate_regex.captures(line).unwrap().extract().1;
		(output.to_string(), Operation::new(operator.parse().unwrap(), input_1.to_string(), input_2.to_string()))
	}).collect();

	(values, gates)
}
