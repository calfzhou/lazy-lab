// Copyright 2007. All Rights Reserved.
// Author: Ji Zhou
#include <iostream>
#include <vector>

using namespace std;

enum BloodType {BT_A, BT_B, BT_O};
typedef unsigned int Level;

template <typename BloodUnit>
BloodType BloodTyping(BloodUnit blood) {
  if (blood > 0) {
    return BT_A;
  } else if (blood < 0) {
    return BT_B;
  } else {
    return BT_O;
  }
}

template <typename BloodUnit>
BloodUnit FiltrateBlood(BloodUnit blood) {
  return (blood >= 0) ? blood : -blood;
}

template <typename BloodUnit>
class Fighter {
 public:
  static Level min_level() { return Level(1); }
  static Level max_level() { return level_limit_; }

  static void set_blood_plasma(const vector<BloodUnit> *blood_plasma) {
    blood_plasma_ = blood_plasma;
    level_limit_ = (blood_plasma_ == NULL) ?
        0 : static_cast<Level>(blood_plasma_->size());
  }

 private:
  static const vector<BloodUnit> *blood_plasma_;
  static Level level_limit_;

 public:
  Fighter(bool hot_blooded, BloodType blood_type)
      : hot_blooded_(hot_blooded),
        blood_type_(blood_type),
        blood_(0),
        blood_stock_(0),
        level_(0),
        next_level_(0) {
  }

  BloodType blood_type() const { return blood_type_; }
  BloodUnit blood() const { return blood_; }
  Level level() const { return level_; }

  bool IsAlive() const {
    Diagnose();
    return blood_ > 0 || next_level_ <= level_limit_;
  }

  bool Cure() {
    if (blood_ > 0) return true;  // Not need cure.

    Diagnose();
    if (next_level_ <= level_limit_) {
      level_ = next_level_;
      blood_ = FiltrateBlood((*blood_plasma_)[level_ - 1]);
      if (hot_blooded_)
        blood_stock_ = blood_;
      return true;  // Renascence.
    }

    level_ = level_limit_;
    return false;  // Dead.
  }

  void Fight(Fighter *opponent) {
    if (this == opponent) return;
    if (!IsAlive() || !opponent->IsAlive()) return;

    Cure();
    opponent->Cure();
    BloodUnit blood_loss = min(blood_, opponent->blood_);
    Hurt(blood_loss);
    opponent->Hurt(blood_loss);
  }

 private:
  const bool hot_blooded_;
  const BloodType blood_type_;
  BloodUnit blood_;
  BloodUnit blood_stock_;
  Level level_;
  mutable Level next_level_;

  void Diagnose() const {
    if (next_level_ == level_) {
      while (++next_level_ <= level_limit_ &&
             blood_type_ != BloodTyping((*blood_plasma_)[next_level_ - 1]));
    }
  }

  void Hurt(BloodUnit blood_loss) {
    blood_ -= blood_loss;
    if (blood_ <= 0 && hot_blooded_ && blood_stock_ > 0) {
      blood_ += blood_stock_;
      blood_stock_ = 0;
    }
  }
};

template <typename BloodUnit>
const vector<BloodUnit> *Fighter<BloodUnit>::blood_plasma_ = NULL;

template <typename BloodUnit>
Level Fighter<BloodUnit>::level_limit_ = 0;

template <typename BloodUnit>
void Foo(const vector<BloodUnit> &blood_plasma, vector<Level> *levels) {
  typedef Fighter<BloodUnit> RealFighter;
  RealFighter::set_blood_plasma(&blood_plasma);
  RealFighter peter(false, BT_A);
  RealFighter neil(false, BT_B);

  while (peter.IsAlive() && neil.IsAlive())
    peter.Fight(&neil);

  RealFighter &winner = neil.IsAlive() ? neil : peter;
  RealFighter &loser = neil.IsAlive() ? peter : neil;
  RealFighter robber(true, winner.blood_type());
  RealFighter soldier(true, loser.blood_type());

  while (robber.IsAlive() && winner.IsAlive())
    robber.Fight(&winner);

  while (true) {
    if (robber.blood() == 0 && soldier.blood() == 0) {
      Level hurt_level = max(robber.level(), soldier.level());
      robber.Cure();
      soldier.Cure();
      Level cure_level = min(robber.level(), soldier.level());
      for (Level level = max(hurt_level, RealFighter::min_level());
           level < min(cure_level, RealFighter::max_level());
           ++level) {
        levels->push_back(level);
      }
    }

    if (!robber.IsAlive() || !soldier.IsAlive()) break;
    robber.Fight(&soldier);
  }
}

int main() {
  vector<int> li;
  int num;

  while (cin >> num)
    li.push_back(num);

  vector<Level> balance_points;
  Foo<int>(li, &balance_points);
  cout << "Balance points: [";
  for (vector<Level>::const_iterator it = balance_points.begin();
       it != balance_points.end(); ) {
    cout << *it;
    if (++it != balance_points.end())
      cout << ", ";
  }
  cout << "]" << endl;

  return 0;
}
