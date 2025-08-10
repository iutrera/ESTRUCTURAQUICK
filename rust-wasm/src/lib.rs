
/// Returns a greeting for the provided name.
pub fn greet(name: &str) -> String {
    format!("Hola, {}!", name)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greets_person() {
        assert_eq!(greet("Mundo"), "Hola, Mundo!");
    }
}

