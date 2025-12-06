use std::io::BufRead;

#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub enum Operator {
    Add,
    Multiply,
    Concatenate,
}

impl Operator {
    fn apply(&self, left: u64, right: u64) -> u64 {
        match *self {
            Self::Add => left + right,
            Self::Multiply => left * right,
            Self::Concatenate => format!("{left}{right}").parse().unwrap()
        }
    }

    fn try_unapply(&self, left: u64, right: u64) -> Result<u64, ()> {
        match *self {
            Self::Add if left >= right => Ok(left - right),
            Self::Multiply if left % right == 0 => Ok(left / right),
            Self::Concatenate => {
                let left_string = left.to_string();
                let right_string = right.to_string();
                if left_string.len() > right_string.len() {
                    let new_len = left_string.len() - right_string.len();
                    let (new_left, remainder) = left_string.split_at(new_len);
                    if remainder != right_string {
                        Err(())
                    } else {
                        Ok(new_left.parse().unwrap())
                    }
                } else {
                    Err(())
                }
            }
            _ => Err(()),
        }
    }
}

fn parse_line(line: &str) -> (u64, Vec<u64>) {
    let [left_str, right_str] = line.split(": ").collect::<Vec<_>>().try_into().unwrap();
    (
        left_str.parse().unwrap(),
        right_str.split(' ').map(|s| s.parse().unwrap()).collect(),
    )
}

fn find_operators(left: u64, right: &[u64], operators: &[Operator]) -> bool {
    if right.is_empty() {
        return false;
    }
    let mut current_left = left;
    let mut stack: Vec<(_, Option<Operator>)> = vec![(operators.iter(), None)];
    'main: loop {
        let level = right.len() - stack.len();

        // Stack is empty, so we tried everything
        let Some(head) = stack.last_mut() else {
            return false;
        };

        // Undo inverse operation that was previously done on this level
        if let Some(op) = head.1 {
            current_left = op.apply(current_left, right[level]);
        }

        if level == 0 {
            // Did an inverse operation for every level, so the remainder must match the left side
            if current_left == right[0] {
                return true;
            }
            // Otherwise we continue trying by ascending
        } else {
            // Find another operation to try
            loop {
                // Remember operation for later undoing on revisiting
                head.1 = head.0.next().copied();
                if let Some(op) = head.1 {
                    // Check if the inverse operation is applicable on this level
                    if let Ok(value) = op.try_unapply(current_left, right[level]) {
                        // Inverse operation is applicable, so we update the left side
                        current_left = value;
                        // ...and descend
                        stack.push((operators.iter(), None));
                        continue 'main; // continue instead of break to skip `stack.pop()` below
                    }
                    // If the inverse operation is not applicable, we continue with the next one
                } else {
                    // We tried all the operations, so we need to backtrack
                    break;
                }
            }
        }

        // ascend
        stack.pop();
    }
}

pub fn solve(input: Box<dyn BufRead>, operators: &[Operator]) -> u64 {
    return input.lines()
        .filter_map(|line| {
            let (left, right) = parse_line(line.as_ref().unwrap());
            find_operators(left, &right[..], operators).then_some(left)
        })
        .sum::<u64>();
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    format!("{}", solve(input, &[Operator::Add, Operator::Multiply]))
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    format!("{}", solve(input, &[Operator::Add, Operator::Multiply, Operator::Concatenate]))
}
