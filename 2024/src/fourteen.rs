use std::io;

use regex::Regex;

use aoc_tools;

type Vector = aoc_tools::Vector<i32, 2>;

pub const WIDTH: i32 = 101;
pub const HEIGHT: i32 = 103;

pub struct Robot {
    pub position: Vector,
    pub velocity: Vector,
}

pub fn parse_input() -> impl Iterator<Item=Robot> {
    let regex = Regex::new(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)").unwrap();
    io::stdin().lines()
        .map(move |l| {
            let [px, py, vx, vy]: [i32; 4] = regex.captures(&l.unwrap())
                .unwrap()
                .iter()
                .skip(1)
                .map(|m| m.unwrap().as_str().parse().unwrap())
                .collect::<Vec<_>>()
                .try_into()
                .unwrap();
            Robot {
                position: Vector::new(px, py),
                velocity: Vector::new(vx, vy),
            }
        })
}
