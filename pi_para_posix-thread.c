#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define ITERATIONS 2e09

// Si no define THREADS va a generar un error por división por 0
#ifndef THREADS
#define THREADS 0
#endif

#ifndef GAP_MULTIPLIER
#define GAP_MULTIPLIER 1
#endif

double piTotal[THREADS * GAP_MULTIPLIER];

void *calculatePi(void *arg)
{
    int initIteration, endIteration, threadId = *(int *)arg;

    initIteration = (ITERATIONS / THREADS) * threadId;
    endIteration = initIteration + ((ITERATIONS / THREADS) - 1);
    // printf("\n %i  %i  %i", threadId, initIteration, endIteration);

    piTotal[threadId] = 0.0;
    do
    {
        piTotal[threadId * GAP_MULTIPLIER] = piTotal[threadId * GAP_MULTIPLIER] + (double)(4.0 / ((initIteration * 2) + 1));
        initIteration++;
        piTotal[threadId * GAP_MULTIPLIER] = piTotal[threadId * GAP_MULTIPLIER] - (double)(4.0 / ((initIteration * 2) + 1));
        initIteration++;
    } while (initIteration < endIteration);
    return 0;
}

int main()
{
    int threadId[THREADS], i, *retval;
    pthread_t thread[THREADS];

    for (i = 0; i < THREADS; i++)
    {
        threadId[i] = i;
        pthread_create(&thread[i], NULL, (void *)calculatePi, &threadId[i]);
    }

    for (i = 0; i < THREADS; i++)
    {
        pthread_join(thread[i], (void **)&retval);
    }

    for (i = 1; i < THREADS; i++)
    {
        piTotal[0] = piTotal[0] + piTotal[i * 8];
    }

    // printf("\npi: %2.10f \n", piTotal[0]);
}
