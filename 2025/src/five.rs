use std::{
    io::BufRead,
    ops::Range,
};

use aoc_tools::RangeSet;

fn parse_input(mut input: Box<dyn BufRead>) -> (Vec<Range<u64>>, Vec<u64>){
    let mut input_string = String::new();
    input.read_to_string(&mut input_string).unwrap();
    let [ranges_string, ids_string] = input_string.split("\n\n").collect::<Vec<_>>().try_into().unwrap();
    let ranges = ranges_string.lines().map(|range_string| {
        let [start, end] = range_string.split('-').map(|s| s.parse::<u64>().unwrap())
        .collect::<Vec<_>>()
        .try_into()
        .unwrap();
        start..end + 1
    }).collect();
    let ids = ids_string.lines().map(|id_string| id_string.parse::<u64>().unwrap()).collect();
    (ranges, ids)
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let (ranges, ids) = parse_input(input);
    let count = ids.into_iter().filter(|id| ranges.iter().any(|range| range.contains(&id))).count();
    format!("{count}")
}


pub fn part_2(input: Box<dyn BufRead>) -> String {
    let (ranges, _) = parse_input(input);
    let count = ranges
        .into_iter()
        .fold(RangeSet::new(), |mut range_set, range| { range_set.add(range); range_set })
        .count::<u64>();
    format!("{count}")
}
