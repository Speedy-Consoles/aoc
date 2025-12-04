use std::{
    collections::HashMap,
    env,
    io::{
        self,
        BufRead,
        BufReader,
    },
};

pub mod one;
pub mod two;
pub mod three;

fn get_solvers() -> HashMap<String, fn(Box<dyn BufRead>) -> String> {
    [
        ("1a", one::part_1 as fn(Box<dyn BufRead>) -> String),
        ("1b", one::part_2 as fn(Box<dyn BufRead>) -> String),
        ("2a", two::part_1 as fn(Box<dyn BufRead>) -> String),
        ("2b", two::part_2 as fn(Box<dyn BufRead>) -> String),
        ("3a", three::part_1 as fn(Box<dyn BufRead>) -> String),
        ("3b", three::part_2 as fn(Box<dyn BufRead>) -> String),
    ]
        .into_iter()
        .map(|(k, v)| (k.to_string(), v))
        .collect::<HashMap<_,_>>()
}

fn main() {
    let solvers = get_solvers();
    let mut args = env::args();
    assert_eq!(args.len(), 2);
    let puzzle_name = args.nth(1).unwrap();
    let solution = solvers.get(&puzzle_name).unwrap()(Box::new(BufReader::new(io::stdin())));
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
    };

    use itertools::Itertools;

    #[test]
    fn check_solutions() {
        let nominal_solutions = BufReader::new(File::open("solutions.txt").unwrap())
            .lines()
            .inspect(|x| println!("{x:?}"))
            .map(|line| line.unwrap().split(' ').map(str::to_string).collect_tuple::<(_, _)>().unwrap())
            .collect::<HashMap<_,_>>();
        let solvers = crate::get_solvers();
        for (puzzle_name, solver) in &solvers {
            let mut iter = puzzle_name.chars();
            iter.next_back().unwrap();
            let day = iter.as_str();
            assert!((1..26).contains(&day.parse().unwrap()));
            let input = Box::new(BufReader::new(File::open(format!("{day}_input.txt")).unwrap()));
            let actual_solution = solver(input);
            let nominal_solution = nominal_solutions.get(puzzle_name).unwrap();
            assert_eq!(actual_solution, *nominal_solution);
        }
    }
}
