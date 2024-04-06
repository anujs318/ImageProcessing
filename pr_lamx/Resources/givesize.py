def gives(h,w):
    ratio=((h*10)/6)/w
    if 7< ratio <17:
        print("size is XL")
    elif 5< ratio<=7:
        print("size is L")
    elif 3< ratio<=5:
        print("size is M")
    else:
        print("Size is S")
    return
print(gives(155,80))
