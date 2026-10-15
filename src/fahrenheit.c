#include <stdio.h>

/* C11 example: use floating-point division, not the integer expression 5 / 9. */
double fahrenheit_to_celsius(double fahrenheit)
{
    double celsius = (fahrenheit - 32.0) * 5.0 / 9.0;
    return celsius; /* Set a breakpoint here to inspect both variables. */
}

int main(void)
{
    double fahrenheit = 0.0;

    printf("Fahrenheit: ");
    fflush(stdout);
    if (scanf("%lf", &fahrenheit) != 1) {
        fprintf(stderr, "Invalid input: enter a number.\n");
        return 1;
    }

    double celsius = fahrenheit_to_celsius(fahrenheit);
    printf("%.2f F = %.2f C\n", fahrenheit, celsius);
    return 0;
}
