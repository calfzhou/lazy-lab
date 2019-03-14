#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// 排列 permutation
// 组合 combination

int main() {
  const int N = 5;
  const int R = 2;

  vector<int> set;
  for (int ii = 0; ii < N; ++ii)
    set.push_back(ii + 1);  // 需要按升序排列
  sort(set.begin(), set.end());

  vector<bool> present(R, true);
  present.insert(present.end(), N - R, false);
  int cnt;

  cout << N << "全排列：" << endl;
  cnt = 0;
  do {
    for (int ii = 0; ii < N; ++ii)
      cout << set[ii] << " ";
    cout << endl;
    ++cnt;
  } while (next_permutation(set.begin(), set.end()));
  cout << "总计：" << cnt << endl;

  cout << endl;

  cout << N << "选" << R << "组合：" << endl;
  cnt = 0;
  do {
    for (int ii = 0; ii < N; ++ii)
      cout << present[ii];
    cout << "\t";
    for (int ii = 0; ii < N; ++ii)
      if (present[ii])
        cout << set[ii] << " ";
    cout << endl;
    ++cnt;
  } while (prev_permutation(present.begin(), present.end()));
  cout << "总计：" << cnt << endl;

  return 0;
}
