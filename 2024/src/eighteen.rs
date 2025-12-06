use std::{
    collections::{
        hash_map::Entry,
        HashMap,
        VecDeque,
    },
    io::BufRead,
};

use aoc_tools;

type Grid = aoc_tools::BoundedSparseGrid<char>;
type Vector = aoc_tools::Vector<i32, 2>;

pub fn parse_input(input: Box<dyn BufRead>) -> impl Iterator<Item=Vector> {
    input.lines().map(|line| {
        let [x, y] = line
            .unwrap()
            .split(',')
            .map(str::parse)
            .map(Result::unwrap)
            .collect::<Vec<_>>()
            .try_into()
            .unwrap();
        Vector::new(x, y)
    })
}

pub fn find_path(grid: &Grid) -> Option<usize> {
    let start = Vector::new(0, 0);
    let finish = Vector::new(grid.width() as i32 - 1, grid.height() as i32 - 1);
    let mut fringe = VecDeque::from([start]);
    let mut distances = HashMap::from([(start, 0)]);
    while let Some(current) = fringe.pop_front() {
        let distance = *distances.get(&current).unwrap();
        for direction in Vector::DIRECTIONS_4 {
            let next = current + direction;
            if next == finish {
                return Some(distance + 1);
            }
            if grid.in_bounds(&next) && grid.get(&next).is_none() {
                if let Entry::Vacant(e) = distances.entry(next) {
                    e.insert(distance + 1);
                    fringe.push_back(next);
                }
            }
        }
    }

    None
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let mut grid = Grid::new(71, 71);
    for position in parse_input(input).take(1024) {
        grid.insert(position, '#');
    }

    format!("{}", find_path(&grid).unwrap())
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    let mut grid = Grid::new(71, 71);
    for position in parse_input(input) {
        grid.insert(position, '#');
        if find_path(&grid).is_none() {
            return format!("{},{}", position[0], position[1]);
        }
    }
    panic!();
}
