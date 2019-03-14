#include <iostream>
#include <vector>
#include <numeric>
#include <assert.h>
using namespace std;

template <typename T>
void Print(const vector<T> &vec, const char *label="") {
  cout << label << "[";
  for (typename vector<T>::const_iterator it = vec.begin();
       it != vec.end(); ++it) {
    cout << *it << ", ";
  }
  cout << "]" << endl;
}

template <typename T>
void Print(const vector<vector<T> > &vec, const char *label="") {
  cout << label << "[" << endl;
  for (typename vector<vector<T> >::const_iterator it = vec.begin();
       it != vec.end(); ++it) {
    Print(*it, "  ");
  }
  cout << "]" << endl;
}

enum TDir {D_UNKNOW=-1, D_LEFT=0, D_RIGHT=1};

template <typename TDis, typename TPow, typename TEng>
TEng MinEnergy(const vector<TDis> &distance, const vector<TPow> &power,
               const size_t left_lamps_cnt, vector<size_t> &order) {
  assert(distance.size() == power.size() &&
         "The array 'distance' and 'power' should have the same size");

  const size_t kX = distance.size() - 1;
  const size_t kM = left_lamps_cnt;
  const size_t kN = kX - kM;
  assert(kM <= kX && kN <= kX && "The parameter 'left_lamps_cnt' is invalid");

  vector<TPow> power_remain_left(kM+1, TPow());
  partial_sum(power.begin(), power.begin()+kM, power_remain_left.rbegin()+1);

  vector<TPow> power_remain_right(kN+1, TPow());
  partial_sum(power.rbegin(), power.rbegin()+kN, power_remain_right.rbegin()+1);

  // Debug.
  Print(power_remain_left, "power_remain_left");
  Print(power_remain_right, "power_remain_right");

  vector<vector<TEng> > wl(kM+1, vector<TEng>(kN+1, TEng()));
  vector<vector<TEng> > wr(kM+1, vector<TEng>(kN+1, TEng()));
  vector<vector<TDir> > cl(kM+1, vector<TDir>(kN+1, D_UNKNOW));
  vector<vector<TDir> > cr(kM+1, vector<TDir>(kN+1, D_UNKNOW));

  for (size_t i = 0; i <= kM; ++i) {
    for (size_t j = 0; j <= kN; ++j) {
      if (i == 0 && j == 0) continue;

      // Left case.
      if (i == 0) {
        wl[i][j] = wr[i][j-1] +
            (power_remain_left[i] + power_remain_right[j-1]) *
            (distance[kM+j] - distance[kM+j-1]) +
            (power_remain_left[i] + power_remain_right[j]) *
            (distance[kM+j] - distance[kM]);
        cl[i][j] = D_RIGHT;
      } else {
        TPow p = power_remain_left[i-1] + power_remain_right[j];
        TEng l = wl[i-1][j] + p * (distance[kM+1-i] - distance[kM-i]);
        TEng r = wr[i-1][j] + p * (distance[kM+j] - distance[kM-i]);
        if (i == 1) {
          assert(l == r);
          wl[i][j] = r;
          cl[i][j] = D_RIGHT;
        } else {
          wl[i][j] = min(l, r);
          cl[i][j] = (l <= r) ? D_LEFT : D_RIGHT;
        }
      }

      // Right case.
      if (j == 0) {
        wr[i][j] = wl[i-1][j] +
            (power_remain_left[i-1] + power_remain_right[j]) *
            (distance[kM+1-i] - distance[kM-i]) +
            (power_remain_left[i] + power_remain_right[j]) *
            (distance[kM] - distance[kM-i]);
        cr[i][j] = D_LEFT;
      } else {
        TPow p = power_remain_left[i] + power_remain_right[j-1];
        TEng r = wr[i][j-1] + p * (distance[kM+j] - distance[kM+j-1]);
        TEng l = wl[i][j-1] + p * (distance[kM+j] - distance[kM-i]);
        if (j == 1) {
          assert(l == r);
          wr[i][j] = l;
          cr[i][j] = D_LEFT;
        } else {
          wr[i][j] = min(l, r);
          cr[i][j] = (l <= r) ? D_LEFT : D_RIGHT;
        }
      }
    }
  }

  // Debug.
  Print(wl, "w[left]");
  Print(wr, "w[right]");
  Print(cl, "c[left]");
  Print(cr, "c[right]");

  TPow min_w = min(wl[kM][kN], wr[kM][kN]);
  TDir d = (wl[kM][kN] <= wr[kM][kN]) ? D_LEFT : D_RIGHT;
  if (kM == 0) {
    assert(wl[kM][kN] == wr[kM][kN]);
    d = D_RIGHT;
  }
  if (kN == 0) {
    assert(wl[kM][kN] == wr[kM][kN]);
    d = D_LEFT;
  }

  int i = static_cast<int>(kM);
  int j = static_cast<int>(kN);
  size_t idx = kX;
  order.resize(kX+1, TEng());
  while (i >= 0 && j >= 0) {
    order[idx--] = (d ? kM + j : kM - i);
    TDir new_d = (d == D_LEFT) ? cl[i][j] : cr[i][j];
    if (d == D_LEFT) {
      --i;
    } else if (d == D_RIGHT) {
      --j;
    } else {
      assert(false && "Invalid dir here.");
    }
    d = new_d;
  }

  return min_w;
}

template <typename TDis, typename TPow, typename TEng>
void Solve(const vector<TDis> &distance, const vector<TPow> &power,
           const size_t kM) {
  cout << "\n==========Question========\n";
  Print(distance, "distance");
  Print(power, "power");

  vector<size_t> order;
  TEng eng = MinEnergy<TDis, TPow, TEng>(distance, power, kM, order);
  cout << "\n==========Solution========\n";
  cout << "Min power is: " << eng << endl;
  Print(order, "order");
  cout << "\n==========================\n" << endl;
}


template <typename TDis, typename TPow, typename TEng>
void Solve(const size_t kM, const size_t kN,
           const TDis *distance, const TPow *power) {
  assert(distance != NULL && power != NULL);
  const size_t kX = kM + kN;
  vector<TDis> dis(kX+1);
  vector<TPow> pow(kX+1);

  for (int ii = 0; ii <= kX; ++ii) {
    dis[ii] = distance[ii];
    pow[ii] = power[ii];
  }

  Solve<TDis, TPow, TEng>(dis, pow, kM);
}

void Foo() {
  {
    const int kM = 2;
    const int kN = 2;
    const int kX = kM + kN;
    const int distance[kX+1] = {2, 3, 5, 6, 8};
    const int power[kX+1] = {10, 20, 20, 30, 10};
    Solve<int, int, int>(kM, kN, distance, power);
  }

  {
    const int kM = 3;
    const int kN = 3;
    const int kX = kM + kN;
    const int distance[kX+1] = {-3, -2, -1, 0, 1, 2, 3};
    const int power[kX+1] = {10, 10, 1000, 0, 10, 1000, 10};
    Solve<int, int, int>(kM, kN, distance, power);
  }

  {
    const int kM = 0;
    const int kN = 0;
    const int kX = kM + kN;
    const int distance[kX+1] = {0};
    const int power[kX+1] = {0};
    Solve<int, int, int>(kM, kN, distance, power);
  }

  {
    const int kM = 0;
    const int kN = 2;
    const int kX = kM + kN;
    const int distance[kX+1] = {0, 1, 2};
    const int power[kX+1] = {10, 20, 20};
    Solve<int, int, int>(kM, kN, distance, power);
  }

  {
    const int kM = 2;
    const int kN = 0;
    const int kX = kM + kN;
    const int distance[kX+1] = {0, 2, 5};
    const int power[kX+1] = {20, 30, 10};
    Solve<int, int, int>(kM, kN, distance, power);
  }
}

void Bar() {
  vector<int> distance;
  vector<int> power;
  size_t m;
  if (!(cin >> m)) return;
  int d, p;
  while (cin >> d >> p) {
    distance.push_back(d);
    power.push_back(p);
  }
  Solve<int, int, int>(distance, power, m);
}

int main() {
  Foo();
  Bar();
}
