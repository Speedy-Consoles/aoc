use std::{
    collections::HashMap,
    io::BufRead,
};

pub fn parse_input(input: Box<dyn BufRead>) -> (Vec<String>, impl Iterator<Item=String>) {
    let mut line_iter = input.lines();
    let towels = line_iter
        .next()
        .unwrap()
        .unwrap()
        .split(", ")
        .map(str::to_string)
        .collect();
    assert!(line_iter.next().unwrap().unwrap().is_empty());
    (towels, line_iter.map(Result::unwrap))
}

fn check_design(design: &str, towels: &[String]) -> bool {
    design.is_empty()
    || towels.iter().any(|towel|
        design.len() >= towel.len()
        && design[..towel.len()] == *towel
        && check_design(&design[towel.len()..], towels)
    )
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let (towels, designs_iter) = parse_input(input);
    let result = designs_iter
        .filter(|design| check_design(design, &towels[..]))
        .count();

    format!("{result}")
}

fn count_possibilities<'a>(design: &'a str, towels: &[String], cache: &mut HashMap<String, usize>) -> usize {
    if design.is_empty() {
        return 1;
    }
    if let Some(&num_possibilities) = cache.get(design) {
        return num_possibilities;
    };
    let num_possibilities = towels.iter()
        .map(|towel| {
            if design.len() >= towel.len() && design[..towel.len()] == *towel {
                count_possibilities(&design[towel.len()..], towels, cache)
            } else {
                0
            }
        })
        .sum();
    cache.insert(design.to_string(), num_possibilities);
    num_possibilities
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    let (towels, designs_iter) = parse_input(input);
    let mut cache = HashMap::new();
    let result = designs_iter
        .map(|design| count_possibilities(&design, &towels[..], &mut cache))
        .sum::<usize>();

    format!("{result}")
}
