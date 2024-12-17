use itertools::Itertools;

use lib::seventeen::*;

fn compute_a(
    output_sequence: &[u8],
    program: &[u8],
    output_operand_code: u8,
    start_a: u64,
    shift: u8,
) -> Option<u64> {
    let [ref remaining_sequence @ .., output] = *output_sequence else {
        return Some(start_a);
    };

    for block in 0..(1 << shift) {
        let a = start_a << shift | block;
        let mut register = Registers::from_a(a);
        for (&instruction_code, &operand_code) in program.iter().tuples() {
            let operand = register.get_operand(instruction_code, operand_code);
            register.do_operation(instruction_code, operand);
        }
        let result = (register.get_operand(5, output_operand_code) & 0b111) as u8;
        if result == output {
            let a = compute_a(remaining_sequence, program, output_operand_code, a, shift);
            if a.is_some() {
                return a;
            }
        }
    };

    None
}

fn main() {
    let (program, _) = parse_input();

    assert!(program.len() >= 6);
    assert!(program.len() % 2 == 0);
    assert_eq!(program[program.len() - 2..], [3, 0]);
    let mut partial_program = vec![];
    let (output_operand_code, shift) = {
        let mut output_operand_code = None;
        let mut shift = None;
        let mut b_initialized = false;
        let mut c_initialized = false;
        for (&i, &o) in program[..program.len() - 2].iter().tuples() {
            assert!(i != 3);
            let initialize_b = (i == 2 || i == 6) && o != 5;
            let read_b = i == 1 || i == 4 || o == 5 && (i == 0 || i == 2 || (5..8).contains(&i));
            let initialize_c = i == 7 && o != 6;
            let read_c = i == 4 || o == 6 && (i == 0 || i == 2 || (5..8).contains(&i));
            assert!(!read_b || b_initialized);
            assert!(!read_c || c_initialized);
            if initialize_b {
                b_initialized = true;
            }
            if initialize_c {
                c_initialized = true;
            }
            if i == 0 {
                assert!(shift.is_none());
                assert!((0..4).contains(&o));
                shift = Some(o);
            } else if i == 5 {
                assert!(output_operand_code.is_none());
                output_operand_code = Some(o);
            } else {
                partial_program.push(i);
                partial_program.push(o);
            }
        }
        (output_operand_code.unwrap(), shift.unwrap())
    };

    println!("{}", compute_a(&program, &partial_program, output_operand_code, 0, shift).unwrap())
}
