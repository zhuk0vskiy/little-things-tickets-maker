from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import logging
from multiprocessing import Process


def make_place(place, dataframe_name):
    img = Image.new('RGBA', (x_img, y_img), 'White')

    idraw = ImageDraw.Draw(img)
    text = str(place)

    font = ImageFont.truetype(font="arial.ttf", size=155)

    idraw.text((50 / len(text) - 5, 20), text, font=font, fill="black")

    img = img.rotate(angle=90)

    img.save("../template/place" + dataframe_name + ".png")


def make_row(row, dataframe_name):
    text = str(row)

    img = Image.new('RGBA', (x_img, y_img), 'White')
    idraw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font="arial.ttf", size=155)
    idraw.text((50 / len(text) - 5, 20), text, font=font, fill="black")

    img = img.rotate(angle=90)

    img.save("../template/row" + dataframe_name + ".png")


def make_ticket(template: Image, dataframe_name: str, place_int: int, row_int: int):
    place = Image.open("../template/place" + dataframe_name + ".png").resize((80, 100))
    row = Image.open("../template/row" + dataframe_name + ".png").resize((80, 100))

    template.paste(place, (2360, 140))
    template.paste(row, (2360, 470))

    template.save("../out/ticket_" + dataframe_name[:3] + "_" + str(place_int) + "_" + str(row_int) + ".png",
                  quality=95)

    template.close()
    place.close()
    row.close()


def make_dataframe(dataframe_name, template_name):
    amf = pd.read_excel("../dataframe/" + dataframe_name)
    path = "../template/" + template_name

    for row in amf.index:
        try:
            row = int(row) + 1
            make_row(row, dataframe_name)
        except:
            logging.error("Не удалось получить билет c рядом:" + dataframe_name + " %d", row + 1)

        print("В процессе: ", dataframe_name, row)
        for place in amf.iloc[row]:
            try:
                place = int(place)
                make_place(place, dataframe_name)
                template = Image.open(path)
                make_ticket(template, dataframe_name, row, place)
            except:
                logging.error("Не удалось получить билет c местом:" + dataframe_name + " %d %d", row + 1, place)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="file.log", filemode="w")

    # settings

    x_img = 200
    y_img = 200

    dataframe1_name = "amf.xlsx"
    dataframe2_name = "part.xlsx"

    template1_name = "amf.png"
    template2_name = "part.png"

    proc1 = Process(target=make_dataframe, args=(dataframe1_name, template1_name,))
    proc2 = Process(target=make_dataframe, args=(dataframe2_name, template2_name,))

    proc1.start()
    proc2.start()

    proc1.join()
    proc2.join()
