#include <stdio.h>

int main() {
    int a, b, c;

    printf("Enter side a (max 10): ");
    scanf("%d", &a);
    printf("Enter side b (max 10): ");
    scanf("%d", &b);
    printf("Enter side c (max 10): ");
    scanf("%d", &c);

    if (a <= 0 || b <= 0 || c <= 0 || a > 10 || b > 10 || c > 10) {
        printf("Out of range values\n");
    } else if (a + b > c && a + c > b && b + c > a) {
        if (a == b && b == c)
            printf("Equilateral triangle\n");
        else if (a == b || b == c || a == c)
            printf("Isosceles triangle\n");
        else
            printf("Scalene triangle\n");
    } else {
        printf("Triangle cannot be formed\n");
    }

    return 0;
}
