 #include <stdio.h>
int isleap(int year){
    if((year % 400 == 0) || (year % 4 == 0 && year % 100 != 0)){
        return 1;
    }
    return 0;
}

int dim(int month,int year){
    if(month == 2){
        return isleap(year) ? 29 : 28;
    }
    if(month==1 || month==3 || month==5 || month==7 ||
       month==8 || month==10 || month==12){
        return 31;
    }
    return 30;
}

int valid(int day,int month,int year){
    if(year < 1812 || year > 2012){
        printf("year out of range\n");
        return 0;
    }
    if(month < 1 || month > 12){
        printf("month out of range\n");
        return 0;
    }
    int max = dim(month, year);
    if(day < 1 || day > max){
        if(month == 2 && day == 29 && !isleap(year)){
            printf("invalid input for leap year\n");
        } else {
            printf("day out of range\n");
        }
        return 0;
    }
    return 1;
}

int main() {
    int day, month, year;

    printf("enter the date, month and year in dd mm yyyy format: ");
    if(scanf("%d %d %d", &day, &month, &year) != 3){
        printf("invalid input format\n");
        return 1;
    }

    if(!valid(day, month, year)){
        return 1;
    }

    // Calculate next day
    day++;
    if(day > dim(month, year)){
        day = 1;
        month++;
        if(month > 12){
            month = 1;
            year++;
        }
    }

    printf("next date is %02d/%02d/%d\n", day, month, year);
    return 0;
}
