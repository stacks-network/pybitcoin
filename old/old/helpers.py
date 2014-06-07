def conv_dict_to_list(d, values):
    """This function will iterate all the keys inside the dictionary
    upto the deepest level, and return all 'values' in a list"""

    if type(d) is dict:
        
        for key in d.keys():
            if type(d[key]) is not dict:
                if type(d[key]) is list:
                    values.extend(d[key])
                else:
                    values.append(d[key])
            else:
                conv_dict_to_list(d[key], values)

    else:                   #is a list?
        if type(d) is list:
            values.extend(d)
        else:               #is a str
            values.append(d)

            
if __name__ == "__main__":
    #d =  {"info":{"registrar":"http://register.dot-bit.org"},"dns":["ns0.web-sweet-web.net","ns1.web-sweet-web.net"],"map":{"":{"ns":["ns0.web-sweet-web.net","ns1.web-sweet-web.net"]}},"email":"synchronize@gmail.com"}
    d = {'map': {'': 'halfmoonlabs.com'}}
    #d = 'halfmoonlabs.com'
    #d = ['halfmoonlabs.com' , 'halfmoon.io']

    values = []
    conv_dict_to_list(d, values)        #values is passed by reference...

