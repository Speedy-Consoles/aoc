use std::collections::HashSet;

use lib::sixteen::*;

fn main() {
    let (parents, finish_node) = compute_parents();

    let mut fringe = vec![finish_node];
    let mut visited = HashSet::from([finish_node]);

    while let Some(node) = fringe.pop() {
        for parent in parents.get(&node).unwrap().1.iter() {
            if !visited.contains(parent) {
                visited.insert(*parent);
                fringe.push(*parent);
            }
        }
    }

    let result = visited.iter().map(|node| node.position).collect::<HashSet<_>>().len();
    println!("{}", result);
}
