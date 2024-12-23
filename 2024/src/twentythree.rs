use std::{
    borrow::Borrow,
    collections::{
        HashMap,
        HashSet,
    },
    hash::Hash,
    io,
};

fn find_cliques_recursively<'a, T, U>(
    network: &'a HashMap<T, HashSet<T>>,
    candidates: &mut Vec<&'a U>,
    selected: &mut Vec<&'a U>,
    discarded: &mut Vec<&'a U>,
    result: &mut Vec<Vec<&'a U>>,
)
where
    T: Eq + Hash + Borrow<U>,
    U: Eq + Hash + ?Sized,
{
    if let Some(candidate) = candidates.pop() {
        if selected.iter().all(|s| network.get(s).unwrap().contains(candidate)) {
            selected.push(candidate);
            result.push(selected.clone());
            find_cliques_recursively::<T, U>(network, candidates, selected, discarded, result);
            selected.pop();
        }

        discarded.push(candidate);
        find_cliques_recursively::<T, U>(network, candidates, selected, discarded, result);
        discarded.pop();

        candidates.push(candidate);
    };
}

pub fn find_cliques<T, U>(network: &HashMap<T, HashSet<T>>) -> Vec<Vec<&U>>
where
    T: Eq + Hash + Borrow<U>,
    U: Eq + Hash + ?Sized,
{
    let mut candidates = Vec::new();
    let mut selected = Vec::new();
    let mut discarded = Vec::new();
    let mut checked = HashSet::new();
    let mut result = Vec::new();
    for (start, connections) in network.iter() {
        candidates.extend(connections.iter().filter(|c| !checked.contains(c)).map(Borrow::borrow));
        selected.push(start.borrow());
        find_cliques_recursively::<T, U>(network, &mut candidates, &mut selected, &mut discarded, &mut result);
        candidates.clear();
        selected.clear();
        checked.insert(start);
    }

    result
}

pub fn get_network() -> HashMap<String, HashSet<String>> {
    let mut network = HashMap::new();
    for line in io::stdin().lines().map(Result::unwrap) {
        let [a, b] = line
            .split('-')
            .collect::<Vec<_>>()
            .try_into()
            .unwrap();
        network.entry(a.to_owned()).or_insert_with(HashSet::new).insert(b.to_owned());
        network.entry(b.to_owned()).or_insert_with(HashSet::new).insert(a.to_owned());
    }

    network
}
