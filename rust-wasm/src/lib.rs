/*!
Basic Rust library compiled to WebAssembly to demonstrate high-performance
computation. The `greet` function is intentionally simple, serving as a
placeholder for future structural analysis routines.
*/

/// Returns a localized greeting for the provided name.
///
/// # Examples
///
/// ```
/// let msg = greet("Mundo");
/// assert_eq!(msg, "Hola, Mundo!");
/// ```
pub fn greet(name: &str) -> String {
    format!("Hola, {}!", name)
}

/// Adds two floating-point numbers.
///
/// This function showcases how numerical routines can be exposed to the
/// WebAssembly module. In the real application it could represent high
/// performance structural calculations.
///
/// # Examples
///
/// ```
/// let sum = add(2.0, 3.5);
/// assert_eq!(sum, 5.5);
/// ```
pub fn add(a: f64, b: f64) -> f64 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;


    /// Verifies that the `greet` function formats the name correctly.
    #[test]
    fn greets_person() {
        assert_eq!(greet("Mundo"), "Hola, Mundo!");
    }

    /// Ensures that floating-point addition works as expected.
    #[test]
    fn adds_numbers() {
        assert!((add(2.0, 3.5) - 5.5).abs() < f64::EPSILON);
    }
}
