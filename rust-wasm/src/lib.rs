
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

#[cfg(test)]
mod tests {
    use super::*;


    /// Verifies that the `greet` function formats the name correctly.

    #[test]
    fn greets_person() {
        assert_eq!(greet("Mundo"), "Hola, Mundo!");
    }
}

