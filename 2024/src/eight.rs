use std::collections::{
    HashMap,
    HashSet,
};

use aoc_tools;

type Grid = aoc_tools::BoundedSparseGrid<char>;
type Vector = aoc_tools::Vector<i32, 2>;

pub fn solve<I>(factors: I) -> usize
where
    I: Iterator<Item=i32> + Clone,
{
    let grid = Grid::from_stdin('.');

    let mut antennas: HashMap<char, Vec<Vector>> = HashMap::new();
    let mut antinodes = HashSet::new();

    for (&position, &c) in grid.indexed_iter() {
        let antennas = antennas.entry(c).or_default();
        for &other_position in antennas.iter() {
            let diff = other_position - position;
            // Apparently we can assume that gcd(diff[0], diff[1]) == 1
            for factor in factors.clone() {
                let offset = diff * factor;
                let mut any_in_bounds = false;
                for antinode in [other_position + offset, position - offset] {
                    if grid.in_bounds(&antinode) {
                        antinodes.insert(antinode);
                        any_in_bounds = true;
                    }
                }
                if !any_in_bounds {
                    break;
                }
            }
        }
        antennas.push(position);
    }

    return antinodes.len();
}
