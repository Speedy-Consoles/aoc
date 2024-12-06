use std::{
    collections::HashMap,
    io::{
        self,
        Read,
    },
};

pub fn parse_input() -> (Vec<(u32, u32)>, Vec<Vec<u32>>) {
    let mut s = String::new();
    io::stdin().read_to_string(&mut s).unwrap();
    let [order_strings, rule_strings] = s.trim().split("\n\n")
        .map(|s| s.split('\n'))
        .collect::<Vec<_>>()
        .try_into()
        .unwrap();
    let rules = order_strings.map(|s|
        <[u32; 2]>::try_from(
        s.split('|')
            .map(|s| s.parse().unwrap())
            .collect::<Vec<_>>())
            .unwrap()
            .into()
        ).collect();
    let updates = rule_strings.map(|s|
        s.split(',').map(|s| s.parse().unwrap()).collect()
    ).collect();

    (rules, updates)
}

pub fn compute_rule_map(orders: Vec<(u32, u32)>) -> HashMap<u32, Vec<u32>> {
    let mut rule_map: HashMap<u32, Vec<u32>> = HashMap::new();
    for (first, second) in orders {
        rule_map.entry(second).or_default().push(first);
    }
    rule_map
}