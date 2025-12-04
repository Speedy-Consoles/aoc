use std::{
    collections::{
        BinaryHeap,
        HashMap,
        hash_map::Entry,
    },
    cmp::Ordering,
};

use aoc_tools;

type Grid = aoc_tools::Grid<char>;
type Vector = aoc_tools::Vector<i32, 2>;

#[derive(Copy, Clone, PartialEq, Eq, Hash)]
pub struct Node {
    pub position: Vector,
    pub direction_index: usize,
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some((self.position[1], self.position[0], self.direction_index).cmp(
            &(other.position[1], other.position[0], other.direction_index)
        ))
    }
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap()
    }
}

#[derive(Copy, Clone, PartialEq, Eq)]
struct FringeNode {
    node: Node,
    distance: usize,
}

impl PartialOrd for FringeNode {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some((other.distance, other.node).cmp(&(self.distance, self.node)))
    }
}

impl Ord for FringeNode {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap()
    }
}

fn add_node(
    node: Node,
    new_node: Node,
    new_distance: usize,
    fringe: &mut BinaryHeap<FringeNode>,
    parents: &mut HashMap<Node, (usize, Vec<Node>)>,
    add_to_fringe: bool,
) -> bool {
    match parents.entry(new_node) {
        Entry::Occupied(mut occupied_entry) => if occupied_entry.get().0 == new_distance {
            occupied_entry.get_mut().1.push(node);
            true
        } else {
            false
        },
        Entry::Vacant(vacant_entry) => {
            vacant_entry.insert((new_distance, vec![node]));
            if add_to_fringe {
                fringe.push(FringeNode { node: new_node, distance: new_distance});
            }
            true
        },
    }
}

pub fn compute_parents() -> (HashMap<Node, (usize, Vec<Node>)>, Node) {
    let grid = Grid::from_stdin().unwrap();

    let start = grid.find(&'S').unwrap();

    let start_node = Node { position: start, direction_index: 0 };
    let mut finish_node = None;
    let mut fringe = BinaryHeap::from([FringeNode { node: start_node, distance: 0 }]);
    let mut parents = HashMap::from([(start_node, (0, vec![]))]);

    while let Some(FringeNode { node, distance }) = fringe.pop() {
        let Node { position, direction_index } = node;
        for i in 1..4 {
            let new_node = Node { position, direction_index: (direction_index + i) % 4 };
            add_node(node, new_node, distance + 1000, &mut fringe, &mut parents, true);
        }
        let new_position = position + Vector::DIRECTIONS_4[direction_index];
        if let Some(&c) = grid.get(&new_position) {
            match c {
                '.' | 'S' | 'E' => {
                    let new_node = Node { position: new_position, direction_index};
                    let added = add_node(node, new_node, distance + 1, &mut fringe, &mut parents, c != 'E');
                    if c == 'E' && added {
                        finish_node = Some(new_node);
                    }
                }
                '#' => (),
                c => panic!("unknown object {}", c),
            }
        }
    }

    (parents, finish_node.unwrap())
}
