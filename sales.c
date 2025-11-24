#include <stdio.h>

int main() {
    int l, s, b;
    const int lp = 45, sp = 30, bp = 25;

    while (1) {
        printf("enter locks (or -1 to stop): ");
        scanf("%d", &l);
        if (l == -1) {
            break;  // exit if locks = -1
        }

        printf("enter stocks: ");
        scanf("%d", &s);

        printf("enter barrels: ");
        scanf("%d", &b);

        int valid = 1; // assume valid

        if (l < 1 || l > 70) {
            printf("locks out of range\n");
            valid = 0;
        }
        if (s < 1 || s > 80) {
            printf("stocks out of range\n");
            valid = 0;
        }
        if (b < 1 || b > 90) {
            printf("barrels out of range\n");
            valid = 0;
        }

        if (valid) {
            int sales = (l * lp) + (s * sp) + (b * bp);
            float commission;

            if (sales <= 1000) {
                commission = sales * 0.10;
            } else if (sales <= 1800) {
                commission = 100 + (sales - 1000) * 0.15;
            } else {
                commission = 220 + (sales - 1800) * 0.20;
            }

            printf("locks = %d\n", l);
            printf("stocks = %d\n", s);
            printf("barrels = %d\n", b);
            printf("sales = %d\n", sales);
            printf("commission = %.2f\n", commission);
        } else {
            printf("No Sales\n");
        }

        printf("\n"); // spacing
    }

    return 0;
}