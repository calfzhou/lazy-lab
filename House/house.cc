#include <iostream>
using namespace std;

#define COND4_IS_CONJ

const int kHouseCnt = 5;
const int kAttributeCnt = 5;
const int kConditionCnt = 15;

enum Attribute {A_NATION=0, A_COLOR, A_DRINK, A_SMOKE, A_PET};
enum Nationality {N_ENGLISH=0, N_SWEDE, N_DANE, N_NORWEGIAN, N_GERMAN};
enum Color {C_RED=0, C_GREEN, C_WHITE, C_YELLOW, C_BLUE};
enum Drink {D_TEA=0, D_COFFEE, D_MILK, D_BEER, D_WATER};
enum Smoke {S_PALLMALL=0, S_BLENDS, S_DUNHILL, S_BLUEMASTER, S_PRINCE};
enum Pet {P_DOG=0, P_BIRD, P_CAT, P_HORSE, P_FISH};

typedef int House[kAttributeCnt];

unsigned int g_cnt[kConditionCnt];

void Print(const House *houses) {
  static const char *attrs[kAttributeCnt] = {
    "国籍", "颜色", "饮料", "烟", "宠物",
  };
  static const char *vals[kHouseCnt][kAttributeCnt] = {
    {"英国", "红", "茶  ", "pallmall  ", "狗"},
    {"瑞典", "绿", "咖啡", "blends    ", "鸟"},
    {"丹麦", "白", "牛奶", "dunhill   ", "猫"},
    {"挪威", "黄", "啤酒", "bluemaster", "马"},
    {"德国", "蓝", "水  ", "prince    ", "鱼"},
  };

  for (int hh = 0; hh < kHouseCnt; ++hh) {
    cout << "House" << hh;
    for (int aa = 0; aa < kAttributeCnt; ++aa) {
      cout << " " << attrs[aa] << "-" << vals[houses[hh][aa]][aa];
    }
    cout << endl;
  }

  unsigned int cnt = 0;
  for (int cc = 0; cc < kConditionCnt; ++cc) {
    cout << "Condition" << cc+1 << "\t" << g_cnt[cc] << endl;
    cnt += g_cnt[cc];
  }
  cout << "Total: " << cnt << ", Average: " << cnt/kConditionCnt << endl;
  cout << endl;
}

template <typename T>
inline int Int(const T& val) {
  return static_cast<T>(val);
}

bool Condition01(const House *houses) {
  ++g_cnt[0];
  // A_COLOR A_NATION
  for (int hh = 0; hh < kHouseCnt; ++hh) {
    if (houses[hh][Int(A_NATION)] == Int(N_ENGLISH)) {
      return houses[hh][Int(A_COLOR)] == Int(C_RED);
    } else if (houses[hh][Int(A_COLOR)] == Int(C_RED)) {
      return false;
    }
  }
  return false;
}

bool Condition02(const House *houses) {
  ++g_cnt[1];
  // A_NATION A_PET
  for (int hh = 0; hh < kHouseCnt; ++hh) {
    if (houses[hh][Int(A_NATION)] == Int(N_SWEDE)) {
      return houses[hh][Int(A_PET)] == Int(P_DOG);
    } else if (houses[hh][Int(A_PET)] == Int(P_DOG)) {
      return false;
    }
  }
  return false;
}

bool Condition03(const House *houses) {
  ++g_cnt[2];
  // A_NATION A_DRINK
  for (int hh = 0; hh < kHouseCnt; ++hh) {
    if (houses[hh][Int(A_NATION)] == Int(N_DANE)) {
      return houses[hh][Int(A_DRINK)] == Int(D_TEA);
    } else if (houses[hh][Int(A_DRINK)] == Int(D_TEA)) {
      return false;
    }
  }
  return false;
}

bool Condition04(const House *houses) {
  ++g_cnt[3];
  // A_COLOR
  bool found_green = false;
  for (int hh = 0; hh < kHouseCnt; ++hh) {
    if (houses[hh][Int(A_COLOR)] == Int(C_GREEN)) {
#ifdef COND4_IS_CONJ
      return hh < kHouseCnt-1 && houses[hh+1][Int(A_COLOR)] == Int(C_WHITE);
#else
      found_green = true;
    } else if (houses[hh][Int(A_COLOR)] == Int(C_WHITE)) {
      return found_green;
#endif
    }
  }
  return false;
}

bool Condition05(const House *houses) {
  ++g_cnt[4];
  // A_COLOR A_DRINK
  for (int hh = 0; hh < kHouseCnt; ++hh) {
    if (houses[hh][Int(A_COLOR)] == Int(C_GREEN)) {
      return houses[hh][Int(A_DRINK)] == Int(D_COFFEE);
    } else if (houses[hh][Int(A_DRINK)] == Int(D_COFFEE)) {
      return false;
    }
  }
  return false;
}

bool Condition06(const House *houses) {
  ++g_cnt[5];
  // A_SMOKE A_PET
  for (int hh = 0; hh < kHouseCnt; ++hh) {
    if (houses[hh][Int(A_SMOKE)] == Int(S_PALLMALL)) {
      return houses[hh][Int(A_PET)] == Int(P_BIRD);
    } else if (houses[hh][Int(A_PET)] == Int(P_BIRD)) {
      return false;
    }
  }
  return false;
}

bool Condition07(const House *houses) {
  ++g_cnt[6];
  // A_COLOR A_SMOKE
  for (int hh = 0; hh < kHouseCnt; ++hh) {
    if (houses[hh][Int(A_COLOR)] == Int(C_YELLOW)) {
      return houses[hh][Int(A_SMOKE)] == Int(S_DUNHILL);
    } else if (houses[hh][Int(A_SMOKE)] == Int(S_DUNHILL)) {
      return false;
    }
  }
  return false;
}

bool Condition08(const House *houses) {
  ++g_cnt[7];
  // A_DRINK
  return houses[kHouseCnt>>1][Int(A_DRINK)] == Int(D_MILK);
}

bool Condition09(const House *houses) {
  ++g_cnt[8];
  // A_NATION
  return houses[0][Int(A_NATION)] == Int(N_NORWEGIAN);
}

bool Condition10(const House *houses) {
  ++g_cnt[9];
  // A_SMOKE A_PET
  for (int hh = 0; hh < kHouseCnt; ++hh) {
    if (houses[hh][Int(A_SMOKE)] == Int(S_BLENDS)) {
      if (hh > 0 && houses[hh-1][Int(A_PET)] == Int(P_CAT)) {
        return true;
      } else if (hh < kHouseCnt-1 && houses[hh+1][Int(A_PET)] == Int(P_CAT)) {
        return true;
      } else {
        return false;
      }
    }
  }
  return false;
}

bool Condition11(const House *houses) {
  ++g_cnt[10];
  // A_SMOKE A_PET
  for (int hh = 0; hh < kHouseCnt; ++hh) {
    if (houses[hh][Int(A_SMOKE)] == Int(S_DUNHILL)) {
      if (hh > 0 && houses[hh-1][Int(A_PET)] == Int(P_HORSE)) {
        return true;
      } else if (hh < kHouseCnt-1 && houses[hh+1][Int(A_PET)] == Int(P_HORSE)) {
        return true;
      } else {
        return false;
      }
    }
  }
  return false;
}

bool Condition12(const House *houses) {
  ++g_cnt[11];
  // A_DRINK A_SMOKE
  for (int hh = 0; hh < kHouseCnt; ++hh) {
    if (houses[hh][Int(A_DRINK)] == Int(D_BEER)) {
      return houses[hh][Int(A_SMOKE)] == Int(S_BLUEMASTER);
    } else if (houses[hh][Int(A_SMOKE)] == Int(S_BLUEMASTER)) {
      return false;
    }
  }
  return false;
}

bool Condition13(const House *houses) {
  ++g_cnt[12];
  // A_NATION A_SMOKE
  for (int hh = 0; hh < kHouseCnt; ++hh) {
    if (houses[hh][Int(A_NATION)] == Int(N_GERMAN)) {
      return houses[hh][Int(A_SMOKE)] == Int(S_PRINCE);
    } else if (houses[hh][Int(A_SMOKE)] == Int(S_PRINCE)) {
      return false;
    }
  }
  return false;
}

bool Condition14(const House *houses) {
  ++g_cnt[13];
  // A_COLOR A_NATION
  for (int hh = 0; hh < kHouseCnt; ++hh) {
    if (houses[hh][Int(A_COLOR)] == Int(C_BLUE)) {
      if (hh > 0 && houses[hh-1][Int(A_NATION)] == Int(N_NORWEGIAN)) {
        return true;
      } else if (hh < kHouseCnt-1 &&
                 houses[hh+1][Int(A_NATION)] == Int(N_NORWEGIAN)) {
        return true;
      } else {
        return false;
      }
    }
  }
  return false;
}

bool Condition15(const House *houses) {
  ++g_cnt[14];
  // A_DRINK A_SMOKE
  for (int hh = 0; hh < kHouseCnt; ++hh) {
    if (houses[hh][Int(A_DRINK)] == Int(D_WATER)) {
      if (hh > 0 && houses[hh-1][Int(A_SMOKE)] == Int(S_BLENDS)) {
        return true;
      } else if (hh < kHouseCnt-1 &&
                 houses[hh+1][Int(A_SMOKE)] == Int(S_BLENDS)) {
        return true;
      } else {
        return false;
      }
    }
  }
  return false;
}

typedef bool (*ConditionFunc)(const House*);
const ConditionFunc kCondFuncs[kAttributeCnt][5] = {
  {Condition09, NULL},
  {Condition01, Condition04, Condition14, NULL},
  {Condition03, Condition05, Condition08, NULL},
  {Condition07, Condition12, Condition13, Condition15, NULL},
  {Condition02, Condition06, Condition10, Condition11, NULL},
};

void TraceBack(House *houses, int house_lvl, int attr_lvl) {
  if (attr_lvl == kAttributeCnt) {
    cout << "Found a solution:\n";
    Print(houses);
  } else if (house_lvl < kHouseCnt) {
    for (int hh = house_lvl; hh < kHouseCnt; ++hh) {
      swap(houses[hh][attr_lvl], houses[house_lvl][attr_lvl]);
      TraceBack(houses, house_lvl+1, attr_lvl);
      swap(houses[hh][attr_lvl], houses[house_lvl][attr_lvl]);
    }
  } else {  // if (attr_lvl < kAttributeCnt)
    const ConditionFunc *cond_funcs = kCondFuncs[attr_lvl];
    while (*cond_funcs != NULL) {
      if (!(*cond_funcs)(houses)) return;
      ++cond_funcs;
    }
    TraceBack(houses, 0, attr_lvl+1);
  }
}

void Foo() {
  House houses[kHouseCnt];
  for (int hh = 0; hh < kHouseCnt; ++hh) {
    for (int aa = 0; aa < kAttributeCnt; ++aa) {
      houses[hh][aa] = hh;
    }
  }
  TraceBack(houses, 0, 0);
  cout << "TraceBack finished:\n";
  Print(houses);
}

int main() {
  Foo();
  return 0;
}
