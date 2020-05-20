
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
  subset sum problem -- finds all subsets of a random list of N integers
  that sum to a target specifed as a command line argument
*/

#define N  20

int count = 0;

void search(int depth, int sum, int target, int used[], int list[]);

int main(int argc, char *argv[])
{
    int i,j,k;
    int target;
    int list[N];
    int used[N];

    target = atoi(argv[1]);
    srand48(3);                               // same list every time
    memset(used, 0, N*sizeof(int));
    for(i = 0 ; i < N; i++){
        do list[i] = 10 + lrand48() % 90; while(used[list[i]]);
        used[list[i]] = 1;
        fprintf(stderr,"%4d",list[i]);
    }
    fprintf(stderr,"\n");
    memset(used, 0, N*sizeof(int));
    search(0, 0, target, used, list);
    fprintf(stderr,"%d\n", count);
}
void search(int depth, int sum, int target, int used[], int list[])
{
    int i;

    if(sum > target)
        return;
    if(sum == target){
        for(i=0;i<N;i++)
            if(used[i])
                printf("%4d",list[i]);
        printf("\n");
        count++;
        return;
    }
    if(depth == N)
        return;
    used[depth] = 1;
    search(depth+1, sum+list[depth], target, used, list);
    used[depth] = 0;
    search(depth+1, sum, target, used, list);
}
