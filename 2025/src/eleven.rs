use std::{
    collections::HashMap,
    io::BufRead,
};
use itertools::Itertools;

fn parse_input(input: Box<dyn BufRead>) -> HashMap<String, Vec<String>> {
    input.lines().map(|line| {
        let line = line.unwrap();
        let [device, output_string] = line.split(": ").collect_array().unwrap();
        let outputs = output_string.split(' ').map(str::to_owned).collect();
        (device.to_owned(), outputs)
    }).collect()
}

#[derive(Debug, Clone)]
enum StackElement {
    Explore(String),
    AddNumPaths(String),
}

fn get_num_paths(from: &str, to: &str, graph: &HashMap<String, Vec<String>>) -> Option<u64> {
    // assuming graph is acyclic
    let mut num_paths_for_nodes = HashMap::from([(to.to_owned(), 1)]);
    let mut stack = vec![StackElement::Explore(from.to_owned())];
    let mut current_num_paths = 0;
    while let Some(element) = stack.pop() {
        match element {
            StackElement::Explore(node) => {
                if let Some(&num_paths) = num_paths_for_nodes.get(&node) {
                    current_num_paths = num_paths;
                } else {
                    current_num_paths = 0;
                    for output in graph.get(&node).into_iter().flat_map(IntoIterator::into_iter) {
                        stack.push(StackElement::AddNumPaths(node.clone()));
                        stack.push(StackElement::Explore(output.clone()));
                    }
                }
            },
            StackElement::AddNumPaths(node) => {
                let num_paths = num_paths_for_nodes.entry(node).or_insert(0);
                *num_paths += current_num_paths;
                current_num_paths = *num_paths;
            },
        }
    }
    num_paths_for_nodes.get(from).copied()
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let graph = parse_input(input);
    let solution = get_num_paths("you", "out", &graph).unwrap();
    format!("{solution}")
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    let graph = parse_input(input);
    let (first, second, first_to_second) = ["fft", "dac"]
        .into_iter()
        .permutations(2)
        .filter_map(|v|
            get_num_paths(v[0], v[1], &graph)
            .filter(|x| *x > 0)
            .map(|num_paths| (v[0], v[1], num_paths))
        )
        .next()
        .unwrap();
    let svr_to_first = get_num_paths("svr", first, &graph).unwrap();
    let second_to_out = get_num_paths(second, "out", &graph).unwrap();
    let solution = svr_to_first * first_to_second * second_to_out;
    format!("{solution}")
}
