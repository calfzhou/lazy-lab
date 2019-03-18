# -*- coding: utf-8 -*-
import os
from os import path
import re

import Tkinter
from ImageTk import PhotoImage
import colorsys
from PIL import Image
from PIL import ImageColor

def InputSecCode(imgpath, interimgs=[], charimgs=[], codehint=''):
  dlg = Tkinter.Tk()
  dlg.title(u'验证码')
  dlg.resizable(False, False)
  dlg.resizable(False, True)
  defpad = 2
  dlgwidth = 0
  dlgheight = 0

  imgobj = PhotoImage(file=imgpath)
  #imgobj = PhotoImage(data=imgdata.encode('base64'))
  dlgwidth = max(dlgwidth, imgobj.width())
  dlgheight += defpad + imgobj.height()
  imglbl = Tkinter.Label(dlg, image=imgobj)
  imglbl.pack(padx=0, pady=defpad)

  if interimgs:
    interobjs = [PhotoImage(image=im.convert('RGB')) for im in interimgs]
    interlbls = [Tkinter.Label(dlg, image=im) for im in interobjs]
    for i in xrange(len(interlbls)):
      dlgwidth = max(dlgwidth, interobjs[i].width())
      dlgheight += defpad + interobjs[i].height()
      interlbls[i].pack(padx=0, pady=defpad)

  if charimgs:
    chargrouplbl = Tkinter.Label(dlg)
    groupwidth = 0
    groupheight = 0
    charobjs = [PhotoImage(image=im.convert('RGB')) for im in charimgs]
    charlbls = [Tkinter.Label(chargrouplbl, image=im) for im in charobjs]
    for i in xrange(len(charlbls)):
      groupwidth += charobjs[i].width()
      groupheight = max(groupheight, charobjs[i].height())
      charlbls[i].pack(side=Tkinter.LEFT, padx=0, pady=0)
    dlgwidth = max(dlgwidth, groupwidth)
    dlgheight += defpad + groupheight
    chargrouplbl.pack(padx=0, pady=2)

  lbl = Tkinter.Label(dlg, text=u'请输入图中的验证码：')
  lbl.pack(padx=2, anchor=Tkinter.W)

  code = Tkinter.StringVar(dlg)
  code.set(codehint)
  ent = Tkinter.Entry(dlg, textvariable=code)
  ent.pack(side=Tkinter.LEFT, expand=Tkinter.YES, fill=Tkinter.X, padx=2, pady=2)
  ent.focus()
  ent.bind('<Return>', (lambda event: dlg.quit()))
  ent.bind('<Escape>', (lambda event: dlg.quit()))

  okbtn = Tkinter.Button(dlg, text=u'确定', command=dlg.quit)
  okbtn.pack(side=Tkinter.RIGHT, padx=2, pady=2)

  width = dlgwidth * 2
  height = dlgheight + 80
  xpos = (dlg.winfo_screenwidth()  - width) // 2
  ypos = (dlg.winfo_screenheight()  - height) // 2
  dlg.geometry('%dx%d+%d+%d' % (width, height, xpos, ypos))

  dlg.mainloop()
  try:
    dlg.destroy()
  except:
    pass

  return code.get().strip().upper()


def XY2Index(x, y, width):
  return y * width + x


def RGB2HLS((r, g, b)):
  return colorsys.rgb_to_hls(r/255., g/255., b/255.)


def HLS2RGB((h, l, s)):
  (r, g, b) = colorsys.hls_to_rgb(h, l, s)
  (r, g, b) = (int(r*255+0.5), int(g*255+0.5), int(b*255+0.5))
  return (r, g, b)


# surrounding label:
# +-+-+-+
# |2|U|1|
# +-+-+-+
# |L|C|R|
# +-+-+-+
# |3|D|4|
# +-+-+-+
SURROUNING_OFFSETS = {
    'C':(0,0),
    'L':(-1,0), 'R':(1,0), 'U':(0,-1), 'D':(0,1),
    '1':(1,-1), '2':(-1,-1), '3':(-1,1), '4':(1,1),
    }

def GetSurroundingPoints(xy, labels):
  labels = labels.upper()
  points = []
  for label in labels:
    offset = SURROUNING_OFFSETS[label]
    newxy = (xy[0] + offset[0], xy[1] + offset[1])
    points.append(newxy)
  return points


varCharColorMinS = 0.65
varCharColorMaxL = 0.6
varCharMinWidth = 10
varCharMinHeight = 10
varCharWidth = 19
varCharHeight = 16

CHARACTER_CATEGORIES = (
    '0123456789'
    'ABCDEFGHIJ'
    'KLMNOPQRST'
    'UVWXYZ'
    )
NON_CHARACTER_RE = re.compile('[^0-9A-Z]')


def DetectSecCode(imgpath, exefp, datafp, modelfp, resultfp):
  (interimgs, charimgs) = SplitChars(imgpath)
  return DetectSecCodeFromImages(charimgs, exefp, datafp, modelfp, resultfp)


def DetectSecCodeFromImages(charimgs, exefp, datafp, modelfp, resultfp):
  if not charimgs or len(charimgs) != 5:
    return ''

  SavePredictData(charimgs, datafp)
  PredictSvmResult(exefp, datafp, modelfp, resultfp, True)
  chars = LoadPredictResult(resultfp)
  #os.remove(datafp)
  #os.remove(resultfp)
  return ''.join(chars)


def PrepareTrainingData(imgfolder, charrootfolder, specialfolder):
  # prepare/clean char folders
  print 'preparing/cleaning char folders'
  if not path.exists(charrootfolder):
    os.mkdir(charrootfolder)
  for ch in CHARACTER_CATEGORIES:
    charfolder = path.join(charrootfolder, ch)
    if not path.exists(charfolder):
      os.mkdir(charfolder)
    else:
      for fn in os.listdir(charfolder):
        fp = path.join(charfolder, fn)
        if path.isfile(fp): os.remove(fp)

  # get and save chars
  cnt = 0
  for fn in os.listdir(imgfolder):
    fp = path.join(imgfolder, fn)
    if not path.isfile(fp):
      print 'skip sub-folder', fn
      continue
    if fn[-4:] != '.gif':
      print 'skip non-gif file', fn
      continue
    code = fn[:-4]
    if len(code) != 5:
      print 'skip not-5-chars-named file', fn
      continue
    if NON_CHARACTER_RE.search(code):
      print 'skip bad-named file', fn
      continue
    (interimgs, charimgs) = SplitChars(fp)
    if not charimgs or len(charimgs) != 5:
      print 'skip failed-to-split image', fn
      dstfp = path.join(specialfolder, fn)
      os.rename(fp, dstfp)
      continue
    for i in xrange(len(charimgs)):
      outfp = path.join(charrootfolder, code[i], '%s_%d.bmp'%(code,i))
      charimgs[i].save(outfp)
    cnt += 1
    print '%d images done\r' % cnt,
  print


def SaveTrainData(charrootfolder, datafp):
  dataf = open(datafp, 'w')
  for i in xrange(len(CHARACTER_CATEGORIES)):
    ch = CHARACTER_CATEGORIES[i]
    charfolder = path.join(charrootfolder, ch)
    for fn in os.listdir(charfolder):
      charfp = path.join(charfolder, fn)
      if not path.isfile(charfp): continue
      img = Image.open(charfp)
      imgdata = list(img.getdata())
      svmdata = GetSvmData(imgdata)
      dataf.write('%d %s\n' % (i, svmdata))
  dataf.close()


def SavePredictData(charimgs, datafp):
  dataf = open(datafp, 'w')
  for i in xrange(len(charimgs)):
    img = charimgs[i]
    imgdata = list(img.getdata())
    svmdata = GetSvmData(imgdata)
    dataf.write('%d %s\n' % (0, svmdata))
  dataf.close()


def LoadPredictResult(resultfp):
  resultf = open(resultfp)
  charids = resultf.readlines()
  resultf.close()
  chars = [CHARACTER_CATEGORIES[int(x)] for x in charids]
  return chars


def TrainSvmModel(exefp, datafp, modelfp, silent=False):
  cmd = '%s -t 2 -c 100 %s %s %s' % (exefp, datafp, modelfp, (silent and '>nul' or ''))
  os.system(cmd)


def EvaluateSvmModel(exefp, datafp, modelfp, resultfp='nul', silent=False):
  PredictSvmResult(exefp, datafp, modelfp, resultfp, silent)


def PredictSvmResult(exefp, datafp, modelfp, resultfp, silent=False):
  cmd = '%s %s %s %s %s' % (exefp, datafp, modelfp, resultfp, (silent and '>nul' or ''))
  os.system(cmd)


def CharPixel2Weight(pixel):
  if not pixel: return 0
  if pixel == (0, 0, 0): return 0
  return 1


def GetSvmData(chardata):
  return ' '.join(['%d:%s' % (i+1,CharPixel2Weight(chardata[i])) for i in xrange(len(chardata))])


def ReviewSplit(fpath):
  if path.isfile(fpath):
    (interimgs, charimgs) = SplitChars(fpath, True)
    code = InputSecCode(fpath, interimgs, charimgs)
    return code
  elif path.isdir(fpath):
    for fn in os.listdir(fpath):
      ReviewSplit(path.join(fpath, fn))
  return None


def ReviewDetect(fpath, exefp, datafp, modelfp, resultfp):
  if path.isfile(fpath):
    (interimgs, charimgs) = SplitChars(fpath, True)
    code = DetectSecCodeFromImages(charimgs, exefp, datafp, modelfp, resultfp)
    code = InputSecCode(fpath, interimgs, charimgs, code)
    return code
  elif path.isdir(fpath):
    for fn in os.listdir(fpath):
      ReviewDetect(path.join(fpath, fn), exefp, datafp, modelfp, resultfp)
  return None


def SplitChars(imgpath, isreview=False):
  secimg = Image.open(imgpath)
  secimg = secimg.convert("RGB")
  secimgdata = list(secimg.getdata())
  interimgs = []
  charimgs = []

  # binaryzation
  secbindata = [0 for i in secimgdata]
  for y in xrange(secimg.size[1]):
    for x in xrange(secimg.size[0]):
      i = XY2Index(x, y, secimg.size[0])
      (h, l, s) = RGB2HLS(secimgdata[i])
      #print (h, l, s)
      if (x != 0 and x != secimg.size[0] - 1
          and y != 0 and y != secimg.size[1] -1
          and s >= varCharColorMinS
          and l <= varCharColorMaxL
          ):
        secbindata[i] = 1
  testimg1 = Image.new('1', secimg.size)
  testimg1.putdata(secbindata)
  if isreview: testimg1.save('test1.bmp')
  interimgs.append(testimg1)

  # remove random noise
  secbindata2 = list(secbindata)
  for y in xrange(1, secimg.size[1] - 1):
    for x in xrange(1, secimg.size[0] - 1):
      centerindex = XY2Index(x, y, secimg.size[0])
      centerpixel = secbindata[centerindex]
      points = GetSurroundingPoints((x,y), 'LRUD')
      pixels = [secbindata[XY2Index(point[0], point[1], secimg.size[0])] for point in points]
      slrud = sum(pixels)
      points = GetSurroundingPoints((x,y), '1234')
      pixels = [secbindata[XY2Index(point[0], point[1], secimg.size[0])] for point in points]
      s1234 = sum(pixels)
      if centerpixel == 0:
        if slrud == 4 and s1234 > 2:
          secbindata2[centerindex] = 1
      elif centerpixel == 1:
        if slrud == 0 or (s1234 == 0 and slrud < 3):
          secbindata2[centerindex] = 0
  testimg2 = Image.new('1', secimg.size)
  testimg2.putdata(secbindata2)
  if isreview: testimg2.save('test2.bmp')
  interimgs.append(testimg2)

  clrranges = GetRanges(secbindata2, secimg.size)
  if isreview:
    for r in clrranges: print r
  clrranges = [r for r in clrranges if
      r.info.size[0] >= varCharMinWidth and r.info.size[1] >= varCharMinHeight]
  #for r in clrranges: print r

  charsize = (varCharWidth, varCharHeight)
  chardatas = [[0 for i in xrange(varCharWidth*varCharHeight)] for x in clrranges]
  for idx in xrange(len(clrranges)):
    CopyColors(chardatas[idx], charsize, (0, 0),
        clrranges[idx].data, clrranges[idx].size, clrranges[idx].info.range[0],
        charsize)
    img = Image.new('1', charsize)
    img.putdata(chardatas[idx])
    if isreview: img.save('char%d.bmp'%(idx+1))
    charimgs.append(img)

  return (interimgs, charimgs)


def GetRanges(rawdata, size):
  data = list(rawdata)
  clrranges = []
  for x in xrange(size[0]):
    for y in xrange(size[1]):
      i = XY2Index(x, y, size[0])
      if data[i] == 0: continue
      clrrange = ColorRange(size, 0, 1, (x, y))
      GetRange(data, size, clrrange, x, y, 0)
      clrranges.append(clrrange)
  return clrranges


def GetRange(data, size, clrrange, x, y, clearcolor):
  if x < 0 or x >= size[0]: return
  if y < 0 or y >= size[1]: return
  i = XY2Index(x, y, size[0])
  if data[i] == clrrange.color:
    clrrange.AddPixel((x, y))
    data[i] = clearcolor
    GetRange(data, size, clrrange, x+1, y, clearcolor)
    GetRange(data, size, clrrange, x, y-1, clearcolor)
    GetRange(data, size, clrrange, x-1, y, clearcolor)
    GetRange(data, size, clrrange, x, y+1, clearcolor)


class ColorRange:
  def __init__(self, size, bgcolor, color, xy):
    self.data = [bgcolor for i in xrange(size[0]*size[1])]
    self.size = size
    self.color = color
    self.info = ColorRangeInfo(xy)

  def AddPixel(self, xy):
    self.data[XY2Index(xy[0], xy[1], self.size[0])] = self.color
    self.info.AddPixel(xy)

  def __str__(self):
    return str(self.info)


class ColorRangeInfo:
  def __init__(self, xy):
    self.pixels = 0
    self.range = (xy, xy)
    self.size = (1, 1)
    self.AddPixel(xy)
    #self.rank = None

  def AddPixel(self, xy):
    self.pixels += 1
    self.range = (
        (
          min(self.range[0][0], xy[0]),
          min(self.range[0][1], xy[1])
        ),
        (
          max(self.range[1][0], xy[0]),
          max(self.range[1][1], xy[1])
        )
      )
    self.size = (
        1 + self.range[1][0] - self.range[0][0],
        1 + self.range[1][1] - self.range[0][1]
      )
    self.density = 1.0 * self.pixels / self.size[0] / self.size[1]
    self.squareness = 1.0 * min(self.size) / max(self.size)

  def __str__(self):
    return str((self.size, self.range, self.pixels, self.density, self.squareness))


def CopyColors(dst, dstsize, dstxy, src, srcsize, srcxy, size):
  if dstxy[0] + size[0] > dstsize[0] or dstxy[1] + size[1] > dstsize[1]:
    raise Exception('dst image has no enough size')
  if dstxy[0] + size[0] > srcsize[0] or dstxy[1] + size[1] > srcsize[1]:
    raise Exception('src image has no enough size')
  ydst = dstxy[1]
  ysrc = srcxy[1]
  for j in xrange(size[1]):
    xdst = dstxy[0]
    xsrc = srcxy[0]
    for i in xrange(size[0]):
      dst[XY2Index(xdst, ydst, dstsize[0])] = src[XY2Index(xsrc, ysrc, srcsize[0])]
      xdst += 1
      xsrc += 1
    ydst += 1
    ysrc += 1
