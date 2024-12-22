use std::io;

const MASK: u64 = (1 << 24) - 1;

pub struct SecretSequence {
    secret: u64,
}

impl SecretSequence {
    pub fn new(secret: u64) -> Self {
        Self { secret }
    }
}

impl Iterator for SecretSequence {
    type Item = u64;

    fn next(&mut self) -> Option<Self::Item> {
        let old_secret = self.secret;
        self.secret = ((self.secret <<  6) ^ self.secret) & MASK;
        self.secret = ((self.secret >>  5) ^ self.secret) & MASK;
        self.secret = ((self.secret << 11) ^ self.secret) & MASK;
        Some(old_secret)
    }
}

pub fn get_secret_sequences() -> impl Iterator<Item=impl Iterator<Item=u64>> {
    io::stdin().lines().map(|line| SecretSequence { secret: line.unwrap().parse().unwrap() })
}
