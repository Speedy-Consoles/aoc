use lib::twentythree::*;

fn main() {
    let network = get_network();
    let result = find_cliques::<_, str>(&network)
        .iter()
        .filter(|clique| clique.len() == 3 && clique.iter().find(|node| node.starts_with('t')).is_some())
        .count();

    println!("{result}");
}
