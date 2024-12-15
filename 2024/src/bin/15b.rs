use lib::fifteen::*;

fn main() {
    let result = solve(|c|
        match c {
            '#' => "##".chars(),
            'O' => "[]".chars(),
            '.' => "..".chars(),
            '@' => "@.".chars(),
            c => panic!("invalid object found: {}", c),
        }
    );
    println!("{}", result);
}