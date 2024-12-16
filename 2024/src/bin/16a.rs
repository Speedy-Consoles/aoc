use lib::sixteen::*;

fn main() {
    let (parents, finish_node) = compute_parents();
    let result = parents.get(&finish_node).unwrap().0;
    println!("{}", result);
}
