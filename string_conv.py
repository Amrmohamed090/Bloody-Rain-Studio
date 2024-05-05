while True:
    strin = input("enter a string: ")
    strin = strin.strip()
    if strin[0] == '"':  
        strin = strin[1:]
    if strin[-1] == '"':
        strin = strin[:len(strin)-1]

    print('"{% static ' + f"'app/{strin}" + "' %}" + '"' )