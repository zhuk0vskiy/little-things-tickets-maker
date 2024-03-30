import os

if __name__ == "__main__":
    try:
        os.mkdir("../out")
        os.mkdir("../dataframe")
        os.mkdir("../template")
    except:
        print("Не удалось создать папки")