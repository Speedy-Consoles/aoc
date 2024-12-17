use lib::seventeen::*;

fn main() {
    let (program, mut registers) = parse_input();

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

    let mut iter = output.into_iter();
    if let Some(v) = iter.next() {
        print!("{}", v);
        iter.for_each(|v| print!(",{}", v));
    }
}
