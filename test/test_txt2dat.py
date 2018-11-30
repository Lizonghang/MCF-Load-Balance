import sys
sys.path.append('../')

from txt2dat import txt2dat


if __name__ == "__main__":
    txt2dat(data_dir='../data', kmax=10)
