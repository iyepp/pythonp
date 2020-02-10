import string

in_str=input("")
out_str = ""
for x in range(len(in_str)):
    if in_str[x].islower():
        print(in_str[x].upper(), end="" )
    else:
        print(in_str[x].lower(), end="" )

print("")


