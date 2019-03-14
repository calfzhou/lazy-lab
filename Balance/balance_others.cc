// Copyright 2007. All Rights Reserved.
// Author: Ji Zhou
#include <iostream>
#include <vector>

using namespace std;

const int INT_THRESHOLD=10000000;

template <typename T>
int FindBalance(const vector<T> &Array)
{
  int Size = Array.size();
  int i,j,k,sum_l,sum_r;
  sum_l=sum_r=i=k=0;
  j=Size-1;
  while(i<=j)
  {
    if(sum_l<=sum_r)
      sum_l+=Array[i++];
    else
      sum_r+=Array[j--];
    if(sum_l>INT_THRESHOLD&&sum_r>INT_THRESHOLD)
    {
      sum_l-=INT_THRESHOLD;
      sum_r-=INT_THRESHOLD;
      k++;
    }


  }
  if(sum_l==sum_r)
    return i-1;
  else if((sum_l+sum_r)%2==1)
    return -1;
  else
  {
    int sum=0;
    for(i=0,j=0;j<k;i++)
    {
      sum+=Array[i ];
      if(sum>INT_THRESHOLD)
      {
        sum-=INT_THRESHOLD;
        j++;
      }
    }
    while(1)
    {
      sum+=Array[i++];
      if(sum==(sum_l+sum_r)/2)
        break;
      if(i==Size)
        return -1;
    }
    return i-1;
  }
}

int main() {
  vector<int> li;
  int num;

  while (cin >> num)
    li.push_back(num);

  int balance_point = FindBalance<int>(li);
  cout << "Balance points: [";
  cout << balance_point;
  cout << "]" << endl;

  return 0;
}
