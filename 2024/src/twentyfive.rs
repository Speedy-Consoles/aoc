use std::io::BufRead;

fn get_shape<'a, I>(lines_iter: I) -> [usize; 5]
where
    I: Iterator<Item=&'a str>
{
    lines_iter
        .enumerate()
        .fold([0; 5], |mut shape, (l, line)| {
            for (c, length) in line.chars().zip(shape.iter_mut()) {
                if c == '#' {
                    assert_eq!(*length, l);
                    *length += 1;
                }
            }
            shape
        })
}

pub fn part_1(mut input: Box<dyn BufRead>) -> String {
    let mut s = String::new();
    input.read_to_string(&mut s).unwrap();
    let mut locks = Vec::new();
    let mut keys = Vec::new();
    for section in s.split("\n\n") {
        let lines = section.lines().collect::<Vec<_>>();
        let lines_iter = lines[1..lines.len() - 1].iter().copied();
        match (lines[0], *lines.last().unwrap()) {
            (".....", "#####") => locks.push(get_shape(lines_iter.rev())),
            ("#####", ".....") => keys.push(get_shape(lines_iter)),
            _ => panic!("unexpected shape"),
        }
    }

    let result = locks.iter().flat_map(|lock|
        keys.iter().filter(|key| lock.iter().zip(key.iter()).all(|(k, l)| k + l <= 5))
    ).count();

    format!("{result}")
}
