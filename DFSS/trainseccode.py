# -*- coding: utf-8 -*-
from yueche import DfssUser
import seccode


TEMP_IMG_FP = r'SecData\yanzheng.gif'
LABELED_ROOT = r'SecData\Labeled'
CHAR_ROOT = r'SecData\Char'
SPECIAL_ROOT = r'SecData\Special'
SVM_TRAIN_EXE_FP = r'svm-train'
SVM_PREDICT_EXE_FP = r'svm-predict'
SVM_DATA_FP = r'data.txt'
SVM_MODEL_FP = r'model.txt'
SVM_RESULT_FP = r'result.txt'


def Label(enableCodeHint=False):
  user = DfssUser('uid', 'pwd', 'sid')
  while True:
    user.SaveSecCode(TEMP_IMG_FP)
    code = seccode.ReviewDetect(TEMP_IMG_FP, SVM_PREDICT_EXE_FP, SVM_DATA_FP, SVM_MODEL_FP, SVM_RESULT_FP)
    if not code: break
    print code
    folder = LABELED_ROOT
    if code[-1] == '-':
      code = code[:-1]
      folder = SPECIAL_ROOT
    fi = open(TEMP_IMG_FP, 'rb')
    fo = open(r'%s\%s.gif' % (folder, code), 'wb')
    fo.write(fi.read())
    fo.close()
    fi.close()


def Prepare():
  seccode.PrepareTrainingData(LABELED_ROOT, CHAR_ROOT, SPECIAL_ROOT)


def ReviewSplit():
  seccode.ReviewSplit(SPECIAL_ROOT)


def Train():
  seccode.SaveTrainData(CHAR_ROOT, SVM_DATA_FP)
  seccode.TrainSvmModel(SVM_TRAIN_EXE_FP, SVM_DATA_FP, SVM_MODEL_FP, silent=True)
  seccode.EvaluateSvmModel(SVM_PREDICT_EXE_FP, SVM_DATA_FP, SVM_MODEL_FP, SVM_RESULT_FP)


def ReviewDetect():
  seccode.ReviewDetect(LABELED_ROOT, SVM_PREDICT_EXE_FP, SVM_DATA_FP, SVM_MODEL_FP, SVM_RESULT_FP)


Label()
#ReviewSplit()
#Prepare()
#Train()
#ReviewDetect()
