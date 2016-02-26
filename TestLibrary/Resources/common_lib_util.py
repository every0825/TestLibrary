# coding:utf-8
import os, re, sys
import random

try:
    import pytesseract
except ImportError:
    # try to import other lib for target OS platform
    print "[Warnning]:\n\t>import pytesseract failled"
    print "\tuse >pip install pytesseract to install the necessary module"
    pass

try:
    from PIL import Image
except ImportError:
    # try to import other lib for target OS platform
    print "[Warnning]:\n\t>from PIL import Image failled"
    print "PIL.Image module is needed to process images"
    pass


class common_lib_util(object):
    def Util_Add_String(self, *strs):
        """拼接传入的字符串，可以是多个

        str1 字符串1
        str2 字符串2
        | Add String | ${str1} | ${str2} |
        | Add String | 12 | 34 |
        """
        result = ''
        for str1 in strs:
            result = result + str1
        return result

    def Util_Image_To_String(self, filename):
        ret = re.search("\.", filename)
        if ret:
            # file = os.path.basename(filename)
            im = Image.open(filename)
            box = (449, 836, 548, 870)
            im = im.crop(box)
            im = im.convert("L")
            width = im.size[0]
            height = im.size[1]
            for h in range(0, height):
                for w in range(0, width):
                    pixel = im.getpixel((w, h))
                    if (pixel >= 140):
                        im.putpixel((w, h), 255)
                    else:
                        im.putpixel((w, h), 0)
            box = (1, 1, 99, 34)
            im = im.crop(box)

            return (pytesseract.image_to_string(im)).replace(' ', '')
        else:
            print "!! no pic !!"
            return "!! no pic !!"

    def Util_Random_String(self, str_type, length):
        """生成并返回随机字符串

        str_type 字符类型:<数字|汉字|英文|组合>
        | ${resault} | Random String | ${str_type} |
        | ${resault} | Random | 组合 |
        """
        length = int(length)
        # list = xrange(random.randint(1, length))
        list = xrange(length)
        if (str_type == '汉字'):
            # return ''.join(map(lambda x: string_gbk.decode('hex').decode('gbk', 'ignore'), list))
            return ''.join(map(lambda x:
                               ("%x" %
                                ((random.randint(0xB0, 0xCF) << 8) |
                                 (random.randint(0x0A, 0x0F) << 4) |
                                 (random.randint(0x00, 0x0F))))
                               .decode('hex').decode('gbk', 'ignore'), list))
        elif (str_type == '英文'):
            return ''.join(map(lambda x: chr(random.randint(97, 122)), list))
        elif (str_type == "数字"):
            return ''.join(map(lambda x: str(random.randint(0, 9)), list))
        elif (str_type == "组合"):
            head = random.randint(0xB0, 0xCF)
            body = random.randint(0xA, 0xF)
            tail = random.randint(0, 0xF)
            val = (head << 8) | (body << 4) | tail
            string_gbk = "%x" % val

            len1 = length/3
            len2 = length/3
            len3 = length-(len1+len2)
            return \
                ''.join(map(lambda x: chr(random.randint(97, 122)),
                            # xrange(random.randint(1, length / 3 - 1)))) \
                            xrange(len1))) \
                + ''.join(map(lambda x:
                              ("%x" %
                               ((random.randint(0xB0, 0xCF) << 8) |
                                (random.randint(0x0A, 0x0F) << 4) |
                                (random.randint(0x00, 0x0F))))
                              .decode('hex').decode('gbk', 'ignore'),
                              # xrange(random.randint(1, length / 3 - 1)))) \
                              xrange(len2))) \
                + ''.join(map(lambda x: str(random.randint(0, 9)),
                              # xrange(random.randint(1, length / 3))))
                              xrange(len3)))
        else:
            return ">illegal parameter"

    