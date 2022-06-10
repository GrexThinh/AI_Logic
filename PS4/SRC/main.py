from solveKB import readData, insertLiteralToKB, PL_RESOLUTION
import os

def main():
    list = os.listdir('input')
    count_files = len(list)
    for i in range(0, count_files):
        alpha, KB = readData('input/{}'.format(list[i]))
        KB = insertLiteralToKB(alpha, KB)
        fout = open('output/output{}.txt'.format(i+1), 'w')
        PL_RESOLUTION(KB, fout)
    print('Done! Please check your folder output.')

if __name__== "__main__":
    main()