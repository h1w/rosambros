def to_utf_8_sig(lst):
    result = []
    for elem in lst:
        if elem == None:
            result.append(None)
        else:
            result.append(elem.encode('utf-8-sig').decode())
    
    return result