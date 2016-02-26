# -*- coding=utf-8 -*-
import sys

"""
Library for Dictionaries of UI Element updating, Now only for test, updating logic is empty/for debugging now.
"""
class ios_uielement_update():
    def __init__(self):
        #self.mobile_lib =  BuiltIn().get_library_instance(CUSTOME_LIBRARY_NAME)
        print "init the class ios_uielement_update !"

    def Print_Dict(self, **mydict):
        print "****size of mydict: %d *****" %  len(mydict)
        for key in mydict.keys():
            print "%s: %s" % (key, mydict[key])

    def Update_Dict(self, **mydict):
        """
        Keyword for update Dictionary instant:
        Can be used to run in RIDE, only for debugging.
        | Library | common_lib_mobile.py |
        *** Test Cases ***
        dict_test_case
            | Print_Dict     |  &{user_dict}   |
            | ${update_dict} |  Updated_Dict  |  &{user_dict}   |
            | Print_Dict     |  &{updated_dict}
        """
        print "*******************"
        print "dict name: %s" % mydict.get('dict_name')
        for key in mydict.keys():
            print 'Key: %s ; and its original value: %s' % (key, mydict.get(key))
            mydict[key] = 'changedvalue'
            print 'Key: %s ; and its new value: %s' % (key, mydict.get(key))
        print "*******************"
        return mydict
