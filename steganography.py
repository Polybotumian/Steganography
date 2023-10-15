from PIL import Image
from numpy import array
class Steganography:

    class LSB:
        
        @staticmethod
        def embed(ipath:str, opath:str, message:str, delimiter:str) -> bool:
            iimg = Image.open(ipath)
            width, height = iimg.size
            if len(message) * 8 <= (width * height * 3) * 8:
                message = message.encode("ascii", "replace").decode("ascii") + delimiter
                iimg_data = array(iimg.getdata(), copy= True)
                iimg.close()
                del iimg

                message_binary:str = ''.join(format(ord(char), '08b') for char in message)
                message_index:int = 0
                encoded_data = []

                for pixel in iimg_data:
                    if message_index < len(message_binary):
                        new_pixel = array(pixel)
                        for channel in range(3):
                            if message_index < len(message_binary):
                                new_pixel[channel] = int(format(new_pixel[channel], '08b')[:-1] + message_binary[message_index], 2)
                                message_index += 1
                        encoded_data.append(tuple(new_pixel))
                    else:
                        encoded_data.append(tuple(pixel))
                encoded_image = Image.new("RGB", (width, height))
                encoded_image.putdata(encoded_data)
                encoded_image.save(opath)
                return True

            else:
                return False

        @staticmethod
        def dislodge(ipath:str, delimiter:str, read_all:bool) -> str:
            try:
                iimg = Image.open(ipath)
                img_data = array(iimg.getdata())
                iimg.close()
                del iimg
                message_binary = ''
                message = ''
                for pixel in img_data:
                    for color_channel in range(3):
                        message_binary += str(pixel[color_channel] & 1)
                        if len(message_binary) == 8:
                            message += chr(int(message_binary, 2))
                            message_binary = ''
                            if message.endswith(delimiter) and not read_all:
                                return message.split(delimiter, 1)[0]
                if  read_all:
                    return message
                else:
                    return "No Message Found!"
            except Exception as e:
                return e