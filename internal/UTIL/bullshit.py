def bullshit1():
    var = None
    def bullshit2(var):
        var = 5
        print var
       
    
    bullshit2(var)
    
    print var

bullshit1()