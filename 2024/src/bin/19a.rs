use lib::nineteen::*;

fn check_design(design: &str, towels: &[String]) -> bool {
    design.is_empty()
    || towels.iter().any(|towel|
        design.len() >= towel.len()
        && design[..towel.len()] == *towel
        && check_design(&design[towel.len()..], towels)
    )
}

fn main() {
    let (towels, designs_iter) = parse_input();
    let result = designs_iter
        .filter(|design| check_design(design, &towels[..]))
        .count();

    println!("{result}");
}
