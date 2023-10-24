from sys import argv

if len(argv) <= 1:
    print('?')
else:
    if argv[1] == '123':
        print('ok')
    else:
        print('error!')
        exit(1)

