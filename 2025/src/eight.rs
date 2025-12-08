use std::{
    collections::HashSet,
    io::BufRead,
};
use itertools::Itertools;
use aoc_tools::{
    self,
    DisjointSets,
};

type Vector = aoc_tools::Vector::<f64, 3>;

fn parse_input(input: Box<dyn BufRead>) -> (Vec<Vector>, Vec<(usize, usize)>) {
    let positions = input
        .lines()
        .map(|line| line.unwrap().split(',').map(|s| s.parse().unwrap()).collect_array().unwrap().into())
        .collect::<Vec<Vector>>();
    let mut edges = (0..positions.len())
        .tuple_combinations()
        .collect::<Vec<_>>();
    edges.sort_unstable_by(|&(i, j), &(k, l)|
        (positions[i] - positions[j]).norm().partial_cmp(&(positions[k] - positions[l]).norm()).unwrap()
    );
    (positions, edges)
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let (positions, edges) = parse_input(input);

    let mut disjoint_sets = DisjointSets::new(positions.len());
    for (i, j) in edges.into_iter().take(1000) {
        disjoint_sets.join(i, j);
    }

    let mut cliques = disjoint_sets.iter().map(HashSet::len).collect::<Vec<_>>();
    cliques.sort_unstable();

    let solution = cliques.iter().rev().take(3).product::<usize>();
    format!("{solution}")
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    let (positions, edges) = parse_input(input);

    let mut disjoint_sets = DisjointSets::new(positions.len());
    let mut edge_iter = edges.into_iter();
    let final_edge = loop {
        let (i, j) = edge_iter.next().unwrap();
        disjoint_sets.join(i, j);
        if disjoint_sets.len() == 1 {
            break (i, j);
        }
    };

    let solution = positions[final_edge.0][0] * positions[final_edge.1][0];
    format!("{solution}")
}
