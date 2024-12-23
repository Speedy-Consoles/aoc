use lib::twentythree::*;

fn main() {
    let network = get_network();
    let mut biggest_clique = find_cliques(&network)
        .into_iter()
        .max_by_key(|clique| clique.len())
        .unwrap();
    biggest_clique.sort();

    println!("{}", biggest_clique.join(","));
}
