import customtkinter as ctk
from PIL import Image as PIL_Image

from utility.constants import BUTTON


class Image(ctk.CTkImage):

    def __init__(self, icon_name: str, size: tuple = (10, 10)):
        """
        Custom Image Widget
        """
        icon_img = PIL_Image.open(BUTTON["icon"][icon_name])
        super().__init__(light_image=icon_img, dark_image=icon_img, size=size)
