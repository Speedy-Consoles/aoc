use std::{
    collections::{
        HashMap,
        VecDeque,
    },
    io::BufRead,
    iter,
};
use good_lp::{
    default_solver,
    Expression,
    ProblemVariables,
    Solution,
    SolutionStatus,
    SolverModel,
    VariableDefinition,
};
use regex::Regex;

fn parse_input(input: Box<dyn BufRead>) -> impl Iterator<Item=(u16, Vec<u16>, Vec<u32>)> {
    let re = Regex::new(concat!(
        r"^\[(?<lights>(?:\.|#)*)\]",
        r" (?<buttons>\(\d+(?:,\d+)*\)(?: \(\d+(?:,\d+)*\))*)",
        r" \{(?<joltages>\d+(?:,\d+)*)\}$")
    ).unwrap();
    input.lines().map(move |line| {
        let line = line.unwrap();
        let captures = re.captures(&line).unwrap();
        let target_lights = captures["lights"]
            .chars()
            .enumerate()
            .map(|(i, c)| ((c == '#') as u16) << i)
            .sum::<u16>();
        let buttons = captures["buttons"].split(' ').map(|l| l
            .strip_prefix('(').unwrap()
            .strip_suffix(')').unwrap()
            .split(',')
            .map(|s| 1 << s.parse::<usize>().unwrap())
            .sum::<u16>()
        ).collect::<Vec<_>>();
        let joltage_requirements = captures["joltages"]
            .split(',')
            .map(|s| s.parse().unwrap())
            .collect();
        (target_lights, buttons, joltage_requirements)
    })
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let machines = parse_input(input);
    let solution = machines.map(|(target_lights, buttons, _)| {
        let mut fringe = VecDeque::from([0]);
        let mut distances = HashMap::from([(0, 0)]);
        while let Some(lights) = fringe.pop_front() {
            let distance = *distances.get(&lights).unwrap();
            for button in buttons.iter() {
                let new_lights = lights ^ button;
                if !distances.contains_key(&new_lights) {
                    let new_distance = distance + 1;
                    if new_lights == target_lights {
                        return new_distance;
                    }
                    distances.insert(new_lights, new_distance);
                    fringe.push_back(new_lights);
                }
            }
        }
        panic!("can't reach target lights")
    }).sum::<u32>();
    format!("{solution}")
}

#[derive(Debug, Copy, Clone)]
struct Constraint {
    variables: u16,
    sum: i32,
}

fn set_variable(constraints: &mut Vec<Constraint>, variable_index: u32, value: i32) -> bool {
    let bit_pattern = 1 << variable_index;
    for c in constraints.iter_mut() {
        if c.variables & bit_pattern != 0 {
            c.sum -= value;
            c.variables ^= bit_pattern;
            if c.variables == 0 && c.sum != 0 || c.sum < 0 {
                return false;
            }
        }
    }
    constraints.retain(|c| c.variables != 0);
    true
}

fn solve_lp_custom(mut constraints: Vec<Constraint>) -> Option<u32> {
    let mut num_elmininated_button_presses = 0;
    loop {
        match constraints.iter().position(|c| c.variables.count_ones() == 1) {
            Some(i) => {
                let var_index = constraints[i].variables.trailing_zeros();
                let value = constraints[i].sum;
                if !set_variable(&mut constraints, var_index, value) {
                    return None
                }
                num_elmininated_button_presses += value as u32;
            },
            None => break,
        }
    }
    if constraints.is_empty() {
        return Some(num_elmininated_button_presses);
    }

    let var_index = constraints[0].variables.trailing_zeros();
    (0..).map_while(|var_value| {
        let mut new_constraints = constraints.clone();
        if !set_variable(&mut new_constraints, var_index, var_value) {
            return None;
        }
        Some((new_constraints, var_value))
    }).filter_map(|(new_constraints, var_value)|
        solve_lp_custom(new_constraints).map(|num_button_presses|
            num_button_presses + num_elmininated_button_presses + var_value as u32
        )
    ).min()
}

#[allow(dead_code)]
fn solve_custom(buttons: Vec<u16>, target_joltages: Vec<u32>) -> Option<u32> {
    let mut constraints = target_joltages
        .into_iter()
        .map(|j| Constraint { variables: 0, sum: j as i32})
        .collect::<Vec<_>>();
    for (b, button) in buttons.into_iter().enumerate() {
        for c in (0..16).filter(|i| (1 << i) & button != 0) {
            constraints[c].variables |= 1 << b;
        }
    }
    solve_lp_custom(constraints)
}

fn solve_good(buttons: Vec<u16>, target_joltages: Vec<u32>) -> Option<u32> {
    let mut problem_variables = ProblemVariables::new();
    let variables: Vec<_> = problem_variables.add_all(
        iter::repeat_with(|| VariableDefinition::new().integer().min(0)).take(buttons.len())
    );
    let mut constraint_expressions = iter::repeat_with(|| Expression::with_capacity(buttons.len()))
        .take(target_joltages.len())
        .collect::<Vec<_>>();
    for (b, button) in buttons.into_iter().enumerate() {
        for c in (0..16).filter(|i| (1 << i) & button != 0) {
            constraint_expressions[c] += variables[b];
        }
    }
    let constraints = constraint_expressions
        .into_iter()
        .enumerate()
        .map(|(i, e)| e.eq(target_joltages[i]));
    let objective = variables.into_iter().sum::<Expression>();
    let mut model = problem_variables
        .minimise(objective.clone())
        .using(default_solver);
    model.set_parameter("loglevel", "0");
    model.with_all(constraints)
        .solve()
        .ok()
        .and_then(|solution| match solution.status() {
            // the result should be an integer but the type is f64 so we just round ¯\_(ツ)_/¯
            SolutionStatus::Optimal => Some(solution.eval(objective).round() as u32),
            SolutionStatus::TimeLimit | SolutionStatus::GapLimit => None,
        })
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    let machines = parse_input(input);
    let solution = machines.map(|(_, buttons, target_joltages)| {
        solve_good(buttons, target_joltages).unwrap()
    }).sum::<u32>();
    format!("{solution}")
}
