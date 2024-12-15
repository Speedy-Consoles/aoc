use lib::fourteen::*;

fn main() {
    let result = parse_input()
        .filter_map(|robot| {
            let final_position = robot.position + robot.velocity * 100;
            let x = final_position[0].rem_euclid(WIDTH);
            let y = final_position[1].rem_euclid(HEIGHT);

            (x != WIDTH / 2 && y != HEIGHT / 2).then(||
                (x > WIDTH / 2) as usize + (y > HEIGHT / 2) as usize * 2
            )
        })
        .fold([0; 4], |mut acc, quadrant| {
            acc[quadrant] += 1;
            acc
        })
        .iter()
        .product::<u32>();

    println!("{result}");
}
