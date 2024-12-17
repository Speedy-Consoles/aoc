use std::io::{
    self,
    Read,
};

use regex::Regex;

pub fn parse_input() -> (Vec<u8>, Registers) {
    let regex = Regex::new(r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: (\d(?:,\d)*)").unwrap();
    let mut s = String::new();
    io::stdin().read_to_string(&mut s).unwrap();
    let [sa, sb, sc, sp] = regex.captures(&s)
        .unwrap()
        .extract().1;
    let a: u64 = sa.parse().unwrap();
    let b = sb.parse().unwrap();
    let c = sc.parse().unwrap();
    let program: Vec<u8> = sp.split(',').map(|v| v.parse().unwrap()).collect();
    (program, Registers { a, b, c })
}

pub struct Registers {
    a: u64,
    b: u64,
    c: u64,
}

impl Registers {
    pub fn from_a(a: u64) -> Self {
        Self { a, b: 0, c: 0 }
    }

    pub fn get_operand(&self, instruction_code: u8, operand_code: u8) -> u64 {
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

    pub fn do_operation(&mut self, instruction_code: u8, operand: u64) {
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

    pub fn a(&self) -> u64 {
        self.a
    }
}