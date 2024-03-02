def no_it_isnt(list):
    newList=[]
    list.reverse()
    for data in list:
        if type(data)== int or type(data)== float:
            newList.append(-data)
        elif type(data)==bool:
            newList.append(not data)
        else:
            newList.append(''.join(reversed(data)))
    return newList
    

