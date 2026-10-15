#include <iomanip>
#include <iostream>

// C++17 example: a one-argument static_assert is a C++17 language feature.
static_assert(__cplusplus >= 201703L);

double fahrenheit_to_celsius(double fahrenheit)
{
    const double celsius = (fahrenheit - 32.0) * 5.0 / 9.0;
    return celsius; // Set a breakpoint here to inspect both variables.
}

int main()
{
    double fahrenheit = 0.0;

    std::cout << "Fahrenheit: " << std::flush;
    if (!(std::cin >> fahrenheit)) {
        std::cerr << "Invalid input: enter a number.\n";
        return 1;
    }

    const double celsius = fahrenheit_to_celsius(fahrenheit);
    std::cout << std::fixed << std::setprecision(2)
              << fahrenheit << " F = " << celsius << " C\n";
    return 0;
}
