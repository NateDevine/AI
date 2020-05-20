#include<stdio.h>
#include<string.h>

int clean[16]={
  0,0,0,
  0,0,0,
  0,0,0,
  0,0,0,
  0,0,0,
  0
};

void print(int *p){
  for(int i=0;i<9;i++) printf("%d", p[i]);
  printf("\n");
}

int check( int *test){
  int x=0;
  int o=0;
  for(int i=0;i<9;i++){
    if(test[i]){
      if(test[i]==1) x++;
      else o++;
    }
  }
  if(!(x==o || x==o+1)) return 0;

/*
  0|1|2
  3|4|5
  6|7|8
*/

  
//   int con[8][3] = {  //all possible win combinations
//     {0,1,2},     
//     {3,4,5},      
//     {6,7,8},      
//     {0,3,6},
//     {1,4,7},
//     {2,5,8},
//     {0,4,7},
//     {2,4,6}
//   };
//   for(int i=0;i<8;i++){
//     if(test[con[i][0]]==1 && test[con[i][1]]==1 && test[con[i][2]]==1) return 0;
//     if(test[con[i][0]]==2 && test[con[i][1]]==2 && test[con[i][2]]==2) return 0; //checking if there are any win conditions
//   }
 // uncomment the next line to print the possible states
 // print(test);
  return 1;
}
//test
int main(){
  int poss=0; 
  for(int i=0; i<43046721;i++){
    int c=i;
    int *new=clean;
    for(int j=0;j<9;j++){
      new[j]=c%3;
      c/=3;
    }
    if(check(new)) poss++;
  }  
  printf("%d\n", poss);
}