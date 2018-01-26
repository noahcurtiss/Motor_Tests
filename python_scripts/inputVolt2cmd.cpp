#include <iostream>
#include <stdio.h>
#include <cmath>
using namespace std;

int volt_calculator(double volt)
{
	int index;
	index = round((volt-10.3)*10);
	return index;
}

int main()
{
double var[4][4] = {{1,2,3,4},{5,6,7,8},{9,10,11,12},{13,14,15,16}};
int i=0;
double volt;
int index;

for (i=0;i<4;i++){
	volt = 10.3+i*0.1;
	index = volt_calculator(volt);
	cout << var[index][0]<<"\n";
}
}