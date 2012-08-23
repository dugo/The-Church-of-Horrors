# -*- coding: utf-8 -*-
import random
from captcha.conf import settings

def math_challenge():
    operators = ('+','*','-',)
    operands = (random.randint(1,10),random.randint(1,10))
    operator = random.choice(operators)
    if operands[0] < operands[1] and '-' == operator:
        operands = (operands[1],operands[0])
    challenge = '%d%s%d' %(operands[0],operator,operands[1])
    return u'%s=' %(challenge), unicode(eval(challenge))
    
def random_char_challenge():
    chars,ret = u'abcdefghijklmnopqrstuvwxyz1234567890', u''
    settings.CAPTCHA_LENGTH = random.randint(5,8) 
    for i in range(settings.CAPTCHA_LENGTH):
        ret += chars[random.randint(0,len(chars)-1)]
    return ret.upper(),ret

def unicode_challenge():
    chars,ret = u'äàáëéèïíîöóòüúù', u''
    for i in range(settings.CAPTCHA_LENGTH):
        ret += random.choice(chars)
    return ret.upper(), ret
        
def word_challenge():
    fd = file(settings.CAPTCHA_WORDS_DICTIONARY,'rb')
    l = fd.readlines()
    fd.close()
    while True:
        word = random.choice(l).strip()
        if len(word) >= settings.CAPTCHA_DICTIONARY_MIN_LENGTH and len(word) <= settings.CAPTCHA_DICTIONARY_MAX_LENGTH:
            break
    return word.upper(), word.lower()
    
def huge_words_and_punctuation_challenge():
    "Yay, undocumneted. Mostly used to test Issue 39 - http://code.google.com/p/django-simple-captcha/issues/detail?id=39"
    fd = file(settings.CAPTCHA_WORDS_DICTIONARY,'rb')
    l = fd.readlines()
    fd.close()
    word = ''
    while True:
        word1 = random.choice(l).strip()
        word2 = random.choice(l).strip()
        punct = random.choice(settings.CAPTCHA_PUNCTUATION)
        word = '%s%s%s'%(word1,punct,word2)
        if len(word) >= settings.CAPTCHA_DICTIONARY_MIN_LENGTH and len(word) <= settings.CAPTCHA_DICTIONARY_MAX_LENGTH:
            break
    return word.upper(), word.lower()
    
def noise_arcs(draw,image):
    aux = {}
    color = {}
    for j in range(0,2):
        for i in range(0,3):
            aux[i] = hex(random.randrange(0,255)).replace("0x","").upper()
            if len(aux[i])<2: aux[i]= "0" + aux[i]
        color[j] = "#" + str(aux[0]) + str(aux[1]) + str(aux[2])
    size = image.size
    pos = int(random.randrange(-20,-5))
    pos1 = int(random.randrange(10,20))
    pos2 = int(random.randrange(-20,-5))
    pos3 = int(random.randrange(10,20))
    draw.arc([pos,pos, size[0],pos1], 0, 295, fill=str(color[0]))
    draw.arc([pos2,pos2, size[0],pos3], 0, 295, fill=str(color[1]))
    return draw

def noise_dots(draw,image):
    size = image.size
    for p in range(int(size[0]*size[1]*0.1)):
        draw.point((random.randint(0, size[0]),random.randint(0, size[1])), fill=settings.CAPTCHA_FOREGROUND_COLOR )
    return draw

def post_smooth(image):
    try:
        import ImageFilter
    except ImportError:
        from PIL import ImageFilter
    return image.filter(ImageFilter.SMOOTH)
