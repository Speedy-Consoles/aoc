use std::{
    collections::HashSet,
    io::BufRead,
};

use regex::Regex;

use aoc_tools;

type Vector = aoc_tools::Vector<i32, 2>;

const WIDTH: i32 = 101;
const HEIGHT: i32 = 103;

const EASTER_EGG: [&[u8; 31]; 33] = [
    b"###############################",
b"#                             #",
b"#                             #",
b"#                             #",
b"#                             #",
b"#              #              #",
b"#             ###             #",
b"#            #####            #",
b"#           #######           #",
b"#          #########          #",
b"#            #####            #",
b"#           #######           #",
b"#          #########          #",
b"#         ###########         #",
b"#        #############        #",
b"#          #########          #",
b"#         ###########         #",
b"#        #############        #",
b"#       ###############       #",
b"#      #################      #",
b"#        #############        #",
b"#       ###############       #",
b"#      #################      #",
b"#     ###################     #",
b"#    #####################    #",
b"#             ###             #",
b"#             ###             #",
b"#             ###             #",
b"#                             #",
b"#                             #",
b"#                             #",
b"#                             #",
b"###############################",
];


struct Robot {
    position: Vector,
    velocity: Vector,
}

fn parse_input(input: Box<dyn BufRead>) -> impl Iterator<Item=Robot> {
    let regex = Regex::new(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)").unwrap();
    input.lines()
        .map(move |l| {
            let [px, py, vx, vy]: [i32; 4] = regex.captures(&l.unwrap())
                .unwrap()
                .iter()
                .skip(1)
                .map(|m| m.unwrap().as_str().parse().unwrap())
                .collect::<Vec<_>>()
                .try_into()
                .unwrap();
            Robot {
                position: Vector::new(px, py),
                velocity: Vector::new(vx, vy),
            }
        })
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let result = parse_input(input)
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

    format!("{result}")
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    let mut robots: Vec<_> = parse_input(input).collect();

    for i in 1.. {
        let mut grid = HashSet::new();
        for robot in robots.iter_mut() {
            robot.position += robot.velocity;
            robot.position[0] = robot.position[0].rem_euclid(WIDTH);
            robot.position[1] = robot.position[1].rem_euclid(HEIGHT);
            grid.insert(robot.position);
        }

        let found = robots.iter().any(|robot|
            EASTER_EGG.into_iter()
                .enumerate()
                .all(|(y, line)|
                    line.into_iter().enumerate().all(|(x, c)|
                        (*c == b'#') == grid.contains(&(Vector::new(x as i32, y as i32) + robot.position))
                    )
                )
        );

        if found {
            return format!("{i}");
        }
    }
    panic!()
}
