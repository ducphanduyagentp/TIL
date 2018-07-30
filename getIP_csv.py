import sys

def main():
    if len(sys.argv) < 2:
        print "Supply a .csv file from enumall"
        exit(1)
    
    filename = sys.argv[1]
    data = open(filename).read().strip('\r\n')
    data = data.split('\r\n')
    data = [d.split(',')[1] for d in data]
    data = [d.replace('"', '') for d in data]
    data = [d for d in data if len(d) > 0]
    data = list(set(data))
    data.sort()
    for d in data:
        print d

if __name__ == '__main__':
    main()