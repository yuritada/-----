import flet as ft
import os
import math


# 東西南北を弧度法の角度に変換
def cdntr(direction):
    if direction == "北":
        return 3 * math.pi / 2
    elif direction == "北東":
        return 7 * math.pi / 4
    elif direction == "東":
        return 0
    elif direction == "南東":
        return math.pi / 4
    elif direction == "南":
        return math.pi / 2
    elif direction == "南西":
        return 3 * math.pi / 4
    elif direction == "西":
        return math.pi
    elif direction == "北西":
        return 5 * math.pi / 4
    else:
        return 0

def make_yazirushi(direction):
    image_path = os.path.abspath("yazirushi.svg")
    image = ft.Image(src=image_path, width=50, height=50,rotate=cdntr(f"{direction}"), fit=ft.ImageFit.CONTAIN)
    return image



