use std::collections::HashMap;

use proc_macro::TokenStream;

use litrs::IntegerLit;

struct Day {
    module_name: &'static str,
    part_function_names: HashMap<char, &'static str>,
}

fn day_id_to_module_name(day_id: u32) -> &'static str {
    match day_id {
        1 => "one",
        2 => "two",
        3 => "three",
        4 => "four",
        5 => "five",
        6 => "six",
        7 => "seven",
        8 => "eight",
        9 => "nine",
        10 => "ten",
        11 => "eleven",
        12 => "twelve",
        13 => "thirteen",
        14 => "fourteen",
        15 => "fifteen",
        16 => "sixteen",
        17 => "seventeen",
        18 => "eighteen",
        19 => "nineteen",
        20 => "twenty",
        21 => "twentyone",
        22 => "twentytwo",
        23 => "twentythree",
        24 => "twentyfour",
        25 => "twentyfive",
        _ => panic!("invalid day id ({day_id})"),
    }
}

fn part_id_to_function_name(part_id: char) -> &'static str {
    match part_id {
        'a' => "part_1",
        'b' => "part_2",
        _ => panic!("invalid part ({part_id})"),
    }
}

fn puzzle_name_literal_to_day_id_and_part_id(integer_literal: IntegerLit<String>) -> (u32, char) {
    let day_id = integer_literal.value::<u32>().expect("day is not a u32");
    assert!(day_id >= 1 && day_id <= 25, "day id must be between 0 and 25, got {day_id}");
    let part_id = match integer_literal.suffix() {
        "a" => 'a',
        "b" => 'b',
        x => panic!("part id must be a or b, not {x}"),
    };
    (day_id, part_id)
}

#[proc_macro]
pub fn fill_main_file(input: TokenStream) -> TokenStream {
    let mut days = HashMap::new();
    {
        for token in input.into_iter() {
            let integer_literal = IntegerLit::try_from(token).expect("token is not an integer literal");
            let (day_id, part_id) = puzzle_name_literal_to_day_id_and_part_id(integer_literal);
            let day = days.entry(day_id).or_insert_with(|| Day {
                module_name: day_id_to_module_name(day_id),
                part_function_names: HashMap::new(),
            });
            let duplicate = day.part_function_names.insert(part_id, part_id_to_function_name(part_id)).is_some();
            assert!(!duplicate, "part {part_id} of day {day_id} found twice");
        }
    }

    let mut output = String::new();

    for Day { module_name, .. } in days.values() {
        output += &format!("pub mod {module_name};\n")
    }

    output += r#"
use std::{
    collections::HashMap,
    env,
    io::{
        self,
        BufRead,
        BufReader,
    },
};

fn main() {
    let mut args = env::args();
    assert_eq!(args.len(), 2);
    let puzzle_name = args.nth(1).unwrap();
    let solution = match puzzle_name.as_str() {"#;

    for (day_id, Day { module_name, part_function_names }) in days.iter() {
        for (part_id, function_name) in part_function_names.iter() {
            output += &format!("\n        \"{day_id}{part_id}\" => {module_name}::{function_name}(Box::new(BufReader::new(io::stdin()))),")
        }
    }

    output += r#"
        _ => panic!("invalid puzzle name"),
    };
    println!("{solution}");
}

#[cfg(test)]
mod tests {
    use std::{
        collections::HashMap,
        fs::File,
        io::{
            BufRead,
            BufReader,
        },
        sync::LazyLock,
    };

    use itertools::Itertools;

    static NOMINAL_SOLUTIONS: LazyLock<HashMap<String, String>> = LazyLock::new(|| BufReader::new(File::open("solutions.txt").unwrap())
        .lines()
        .map(|line| line.unwrap().split(' ').map(str::to_string).collect_tuple::<(_, _)>().unwrap())
        .collect()
    );
"#;

    for (day_id, Day { module_name, part_function_names }) in days.iter() {
        for (part_id, function_name) in part_function_names.iter() {
            output += &format!("
    #[test]
    fn check_{day_id}{part_id}() {{
        let input = Box::new(BufReader::new(File::open(format!(\"{day_id}_input.txt\")).unwrap()));
        let actual_solution = crate::{module_name}::{function_name}(input);
        let nominal_solution = NOMINAL_SOLUTIONS.get(\"{day_id}{part_id}\").unwrap();
        assert_eq!(actual_solution, *nominal_solution);
    }}
");
        }
    }

    output += "}";

    output.parse().unwrap()
}
