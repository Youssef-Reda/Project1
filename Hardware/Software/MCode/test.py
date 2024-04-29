def set_text(data1):
    data2 = '"' + data1 + '"'
    return data2


while(True):
    ioput = input("Enter a word\n")
    oput = set_text(ioput)
    print(oput)
    oput = set_text('Recording..')
    print(oput)
