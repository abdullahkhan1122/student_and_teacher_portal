#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define SIZE 50
int arr[SIZE];
int count = 0;
pthread_mutex_t myMutex;

void *fib(void *value)
{
    int n = *(int *)value;

    if (n < 0)
    {
        return NULL;
    }
    else
    {

        pthread_mutex_lock(&myMutex);

        int num1 = 0, num2 = 1, sum;

        arr[0] = num1;
        arr[1] = num2;
        count = 2;

        for (int i = 2; i <= n; i++)
        {
            sum = num1 + num2;
            num1 = num2;
            num2 = sum;
            arr[count++] = sum;
        }

        pthread_mutex_unlock(&myMutex);
    }
}

int main()
{
    pthread_t thread[3];
    int find = 10;

    // pthread_create(&thread, NULL, fib, &find);
    pthread_create(&thread[0], NULL, fib, &find);
    // pthread_create(&thread[1], NULL, fib, &find);
    // pthread_create(&thread[2], NULL, fib, &find);

    for (int i = 0; i < count; i++)
    {
        // printf("Element No. %d in series is: %d\n", i + 1, arr[i]);
        printf("%d\n", arr[i]);
    }

    return 0;
}
