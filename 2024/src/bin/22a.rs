use lib::twentytwo::*;

fn main() {
    let result = get_secret_sequences()
        .map(|mut iter| iter.nth(2000).unwrap())
        .sum::<u64>();

    println!("{result}");
}
