use std::{
    fmt,
    io::BufRead,
    iter,
    mem,
};
use itertools::Itertools;
use regex::Regex;
use aoc_tools;

type Grid = aoc_tools::Grid<bool>;
type Vector = aoc_tools::Vector<i32, 2>;

fn orient_tiles(tiles: &Vec<Vector>, dim_swap: bool, v_flip: bool, h_flip: bool) -> Vec<Vector> {
    tiles.iter().map(|v| {
        let mut x = v[0];
        let mut y = v[1];
        if h_flip {
            x = 2 - x;
        }
        if v_flip {
            y = 2 - y;
        }
        if dim_swap {
            mem::swap(&mut x, &mut y);
        }
        Vector::new(x, y)
    }).collect()
}

#[derive(Debug)]
struct Tree {
    width: usize,
    height: usize,
    num_presents: [usize; 6],
}

fn parse_input(mut input: Box<dyn BufRead>) -> ([Vec<Vec<Vector>>; 6], Vec<Tree>) {
    let mut input_string = String::new();
    input.read_to_string(&mut input_string).unwrap();
    let sections = input_string.split("\n\n").collect::<Vec<_>>();
    let presents = sections[..sections.len() - 1].iter().enumerate().map(|(i, present_string)| {
        let mut iter = present_string.lines();
        let index_string = iter.next().unwrap();
        assert_eq!(index_string, format!("{i}:"));
        let tiles = iter
            .enumerate()
            .flat_map(|(i, line)|
                line
                    .chars()
                    .enumerate()
                    .filter_map(move |(j, c)| (c == '#').then_some(Vector::new(j as i32, i as i32)))
            )
            .collect::<Vec<_>>();
        assert!(tiles.len() >= 5); // needed for the assumption that presents can not be in the same 3x3 region
        assert!(tiles.iter().all(|v| (0..3).contains(&v[0]) && (0..3).contains(&v[1])));
        let mut presents = (0..8)
            .map(|x| orient_tiles(&tiles, (x & 1) != 0, ((x >> 1) & 1) != 0, ((x >> 2) & 1) != 0))
            .collect::<Vec<_>>();
        presents.sort();
        presents.dedup();
        presents
    }).collect_array().unwrap();
    let tree_regex = Regex::new(r"^(?<width>\d\d)x(?<height>\d\d): (?<num_presents>\d\d(?: \d\d){5})$").unwrap();
    let trees_string = *sections.last().unwrap();
    let trees = trees_string.lines().map(|line| {
        let captures = tree_regex.captures(line).unwrap();
        let width = captures["width"].parse().unwrap();
        let height = captures["height"].parse().unwrap();
        let num_presents = captures["num_presents"]
            .split(' ')
            .map(|n| n.parse::<usize>().unwrap())
            .collect_array::<6>()
            .unwrap();
        Tree { width, height, num_presents }
    }).collect();
    (presents, trees)
}

struct PlacedPresent {
    present_index: usize,
    orientation_index: usize,
}

impl fmt::Debug for PlacedPresent {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} {}", self.present_index, self.orientation_index)
    }
}

enum StackElementKind {
    TryPlace,
    Remove
}

struct StackElement {
    kind: StackElementKind,
    present: Option<PlacedPresent>,
}

impl fmt::Debug for StackElement {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self.kind {
            StackElementKind::TryPlace => write!(f, "Try "),
            StackElementKind::Remove => write!(f, "Rem "),
        }?;
        match self.present {
            Some(ref pp) => write!(f, "{:?}", pp),
            None => write!(f, "none"),
        }
    }
}

fn can_place_present(grid: &Grid, tiles: &Vec<Vector>, position: &Vector) -> bool {
    tiles.iter().all(|tile| grid.get(&(*position + *tile)).is_some_and(|x| !x))
}

fn place_present(grid: &mut Grid, tiles: &Vec<Vector>, position: &Vector) {
    for tile in tiles {
        grid[*position + *tile] = true;
    }
}

fn remove_present(grid: &mut Grid, tiles: &Vec<Vector>, position: &Vector) {
    for tile in tiles {
        grid[*position + *tile] = false;
    }
}

fn extend_stack(stack: &mut Vec<StackElement>, presents: &[Vec<Vec<Vector>>; 6], num_presents: &[usize; 6]) {
    stack.extend(iter::once(None)
        .chain(num_presents
            .iter()
            .enumerate()
            .filter_map(|(i, &num_remaining)| (num_remaining > 0).then_some(i))
            .flat_map(|present_index|
                (0..presents[present_index].len()).map(move |orientation_index|
                    Some(PlacedPresent { present_index, orientation_index })
                )
            )
        )
        .map(|present| StackElement { kind: StackElementKind::TryPlace, present })
    );
}

fn do_presents_fit(tree: &Tree, presents: &[Vec<Vec<Vector>>; 6]) -> bool {
    let mut grid = Grid::from_default(tree.width as usize, tree.height as usize);
    let mut num_remaining_presents = tree.num_presents;
    let mut num_remaining_free_tiles = tree.width * tree.height;
    let mut num_remaining_present_tiles = (0..6).map(|i| presents[i][0].len() * tree.num_presents[i]).sum::<usize>();
    if num_remaining_present_tiles >= num_remaining_free_tiles {
        return false;
    }
    let mut current_position = Vector::new(0, 0);
    let mut stack = Vec::new();
    extend_stack(&mut stack, presents, &num_remaining_presents);
    while let Some(e) = stack.pop() {
        match e {
            StackElement { kind: StackElementKind::TryPlace, present: maybe_pp } => {
                let placed = maybe_pp.as_ref().is_none_or(|pp| {
                    let tiles = &presents[pp.present_index][pp.orientation_index];
                    let can_place = can_place_present(&mut grid, tiles, &current_position);
                    if can_place {
                        // update grid
                        place_present(&mut grid, tiles, &current_position);

                        // update present counter
                        num_remaining_presents[pp.present_index] -= 1;

                        // update tile counters
                        num_remaining_free_tiles -= tiles.len();
                        num_remaining_present_tiles -= tiles.len();
                    }
                    can_place
                });
                if placed {
                    // check success condition
                    if maybe_pp.is_some() && num_remaining_presents.iter().sum::<usize>() == 0 {
                        return true;
                    }

                    // if the current tile isn't filled yet, it's lost
                    if !grid[current_position] {
                        num_remaining_free_tiles -= 1;
                    }

                    // advance position
                    current_position[0] += 1;
                    if current_position[0] >= tree.width as i32 {
                        current_position[0] = 0;
                        current_position[1] += 1;
                    }

                    // extend stack
                    stack.push(StackElement { kind: StackElementKind::Remove, present: maybe_pp });
                    if num_remaining_present_tiles < num_remaining_free_tiles && current_position[1] < tree.height as i32 {
                        extend_stack(&mut stack, presents, &num_remaining_presents);
                    }
                }
            }
            StackElement { kind: StackElementKind::Remove, present: maybe_pp } => {
                // reverse position
                current_position[0] -= 1;
                if current_position[0] < 0 {
                    current_position[0] = tree.width as i32 - 1;
                    current_position[1] -= 1;
                }

                // update counter based on current tile
                if !grid[current_position] {
                    num_remaining_free_tiles += 1;
                }

                if let Some(pp) = maybe_pp {
                    let tiles = &presents[pp.present_index][pp.orientation_index];

                    // update grid
                    remove_present(&mut grid, tiles, &current_position);

                    // update present counter
                    num_remaining_presents[pp.present_index] += 1;

                    // update tile counters
                    num_remaining_free_tiles += tiles.len();
                    num_remaining_present_tiles += tiles.len();
                };
            }
        }
    }

    false
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let (presents, trees) = parse_input(input);
    let solution = trees.iter().filter(|tree| do_presents_fit(tree, &presents)).count();
    format!("{solution}")
}
