use std::io::BufRead;

use itertools::Itertools;

use regex::Regex;

fn parse_input(mut input: Box<dyn BufRead>) -> (Vec<u8>, Registers) {
    let regex = Regex::new(r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: (\d(?:,\d)*)").unwrap();
    let mut s = String::new();
    input.read_to_string(&mut s).unwrap();
    let [sa, sb, sc, sp] = regex.captures(&s)
        .unwrap()
        .extract().1;
    let a: u64 = sa.parse().unwrap();
    let b = sb.parse().unwrap();
    let c = sc.parse().unwrap();
    let program: Vec<u8> = sp.split(',').map(|v| v.parse().unwrap()).collect();
    (program, Registers { a, b, c })
}

struct Registers {
    a: u64,
    b: u64,
    c: u64,
}

impl Registers {
    fn from_a(a: u64) -> Self {
        Self { a, b: 0, c: 0 }
    }

    fn get_operand(&self, instruction_code: u8, operand_code: u8) -> u64 {
        match instruction_code {
            0 | 2 | 5..8 => match operand_code {
                0..4 => operand_code as u64,
                4 => self.a,
                5 => self.b,
                6 => self.c,
                _ => panic!("unexpected instruction-operand combination {}, {}", instruction_code, operand_code),
            },
            _ => operand_code as u64,
        }
    }

    fn do_operation(&mut self, instruction_code: u8, operand: u64) {
        match instruction_code {
            0 => self.a >>= operand,
            1 => self.b ^= operand,
            2 => self.b = operand & 0b111,
            3 => unreachable!("unexpected jump operation"),
            4 => self.b ^= self.c,
            5 => unreachable!("unexpected jump operation"),
            6 => self.b = self.a >> operand,
            7 => self.c = self.a >> operand,
            _ => unreachable!("invalid instruction code {}", instruction_code),
        }
    }

    fn a(&self) -> u64 {
        self.a
    }
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let (program, mut registers) = parse_input(input);

    let mut ip = 0;
    let mut output = vec![];
    while ip < program.len() {
        let instruction_code = program[ip];
        let operand_code = program[ip + 1];
        let mut jumped = false;
        let operand = registers.get_operand(instruction_code, operand_code);
        match instruction_code {
            0..3 | 4 | 6..8 => registers.do_operation(instruction_code, operand),
            3 => if registers.a() != 0 {
                ip = operand as usize;
                jumped = true;
            },
            5 => output.push(operand & 0b111),
            _ => panic!("invalid instruction code {}", instruction_code),
        }
        if !jumped {
            ip += 2;
        }
    }

    output.into_iter().join(",")
}

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

pub fn part_2(input: Box<dyn BufRead>) -> String {
    let (program, _) = parse_input(input);

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

    format!("{}", compute_a(&program, &partial_program, output_operand_code, 0, shift).unwrap())
}
