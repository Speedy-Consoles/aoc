use std::{
    io::BufRead,
    mem,
};

use regex::Regex;

fn extended_gcd(a: i64, b: i64) -> (i64, i64, i64, i64, i64) {
    let (mut old_r, mut r) = (a, b);
    let (mut old_s, mut s) = (1, 0);
    let (mut old_t, mut t) = (0, 1);

    while r != 0 {
        let quotient = old_r / r;
        (old_r, r) = (r, old_r - quotient * r);
        (old_s, s) = (s, old_s - quotient * s);
        (old_t, t) = (t, old_t - quotient * t);
    }

    (old_r, old_s, old_t, t, s)
}

fn compute_button_presses(mut ax: i64, mut ay: i64, mut bx: i64, mut by: i64, mut px: i64, mut py: i64) -> Option<(i64, i64)> {
    // NOTE: None of the special cases is hit by the given input, so their code may not be correct.
    // The only None case is the one with fractions of button presses.
    if ax == 0 {
        // NOTE: Never hit
        if ay == 0 {
            // A button does nothing
            let u = if bx == 0 {
                // B button does not affect X coordinate
                if px != 0 {
                    // ...but we need to move in X direction
                    return None;
                } else {
                    0
                }
            } else {
                // B button does affect X coordinate
                if px % bx != 0 {
                    // ...but it doesn't get us to the right X coordinate
                    return None;
                } else {
                    px / bx
                }
            };
            if by * u != py {
                // We can use the B button for X but it doesn't give us the right Y coordinate
                return None;
            }
            // B button alone can reach the price position by pressing it u times
            return Some((0, u));
        } else {
            mem::swap(&mut ax, &mut ay);
            mem::swap(&mut bx, &mut by);
            mem::swap(&mut px, &mut py);
        }
    } else {
        // |ax    bx           ] px
        // |ay    by           ] py
        // ->
        // |ax    bx           ] px
        // |0     by*ax - bx*ay] py*ax - px*ay

        by = by * ax - bx * ay;
        py = py * ax - px * ay;
    }

    if by == 0 {
        // NOTE: Never hit
        // Movement vectors are linearly dependent
        if py != 0 {
            // ...but we can't reach the Y coordinate if we manage to reach the X coordinate
            return None;
        }
        // ...so we just need to consider the X dimension
        let (gcd, s, t, qa, qb) = extended_gcd(ax , bx);

        if px % gcd != 0 {
            // We can't reach the price's X position with any combination of button presses
            return None;
        }

        // One way to do it, ignoring the cost:
        let k = px / gcd;
        let u_0 = s * k;
        let v_0 = t * k;

        let u = u_0.rem_euclid(qa);
        let v = v_0 - u_0.div_euclid(qa) * qb;

        if v < 0 {
            // We'd need to press the B button a negative number of times
            return None;
        }

        return Some((u, v));
    }

    // |ax    bx] px
    // |0     by] py
    // ->
    // |ax*by 0 ] px*by - py*bx
    // |0     by] py

    ax *= by;
    px = px * by - py * bx;

    // linearly independent
    if px % ax != 0 || py % by != 0 {
        // We'd need to do fractions of button presses
        return None;
    }

    Some((px / ax, py / by))
}

pub fn solve(mut input: Box<dyn BufRead>, offset: i64) -> i64 {
    let regex = Regex::new(
        r"^Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)$"
    ).unwrap();

    let mut s = String::new();
    input.read_to_string(&mut s).unwrap();
    s.trim().split("\n\n").filter_map(|block| {
        let [ax, ay, bx, by, px, py] = regex.captures(&block)
            .unwrap()
            .extract()
            .1
            .map(str::parse)
            .map(Result::unwrap);

        compute_button_presses(ax, ay, bx, by, px + offset, py + offset).map(|(u, v)| u * 3 + v)
    }).sum::<i64>()
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    format!("{}", solve(input, 0))
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    format!("{}", solve(input, 10000000000000))
}
