use std::collections::HashSet;

use lib::fourteen::*;

use aoc_tools;

type Vector = aoc_tools::Vector<i32, 2>;

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

fn main() {
    let mut robots: Vec<_> = parse_input().collect();

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
            println!("{i}");
            break;
        }
    }
}
