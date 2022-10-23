import numpy as np
import imageio
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes


def rgb2hex(rgb):

    """
    convert a list or tuple of RGB values
    to a string in hex
    """

    r,g,b = rgb
    return '{:02x}{:02x}{:02x}'.format(r, g, b)


def arrayToString(array):
    """
    convert an array to a string
    """

    string = ""
    for element in array:
        string += str(element)

    return string


def sliceStr(string,sliceLenght):
    """
    slice a string in chunks of sliceLenght lenght
    """

    string = str(string)
    array = np.array([string[i:i+sliceLenght] for i in range(0,len(string),sliceLenght)])
    return array



def hexToRGB(hexadecimal):
    """
    convert a hex string to an array of RGB values
    """
    h = hexadecimal.lstrip('#')
    return [int(h[i:i+2], 16) for i in (0, 2, 4)]



def EncryptImage(imageToEncrypt,key):
    """
    Function to encrypt
    imageToEncrypt: a string, representing the direction of the image
    key: a key. MUST be an 8 byte long bytes object
    """

    dataToEncrypt =imageio.imread(imageToEncrypt)

    if dataToEncrypt.shape[2] ==4:
        dataToEncrypt = np.delete(dataToEncrypt,3,2)

    originalRows, originalColumns,_ = dataToEncrypt.shape


    #converting rgb to hex
    hexToEncrypt = np.apply_along_axis(rgb2hex, 2, dataToEncrypt)
    hexToEncrypt = np.apply_along_axis(arrayToString, 1, hexToEncrypt)
    hexToEncrypt = str(np.apply_along_axis(arrayToString, 0, hexToEncrypt))





    data = bytes.fromhex(hexToEncrypt)
    iv = b"00000000"
    cipher = DES3.new(bytes(key), DES3.MODE_CFB,iv)


    d = cipher.encrypt(data)


    encryptedData = d.hex()


    stepOne = sliceStr(encryptedData,originalColumns*6)

    stepTwo = []

    for i in stepOne:
        stepTwo.append(sliceStr(i,6))

    stepThree = []
    for i in stepTwo:
        d = []
        for j in i:
            d.append(hexToRGB(j))

        if len(stepThree) != originalRows:
            stepThree.append(d)

        encryptedImg = np.asarray(stepThree)

    imageio.imwrite("destest.png",encryptedImg)
    return stepThree




def DecryptImage(imageToEncrypt,key):
    """
    Function to decrypt
    imageToEncrypt: a string, representing the direction of the image
    key: a key. MUST be an 8 byte long bytes object
    """

    dataToEncrypt =imageio.imread(imageToEncrypt)

    if dataToEncrypt.shape[2] ==4:
        dataToEncrypt = np.delete(dataToEncrypt,3,2)

    originalRows, originalColumns,_ = dataToEncrypt.shape


    #converting rgb to hex
    hexToEncrypt = np.apply_along_axis(rgb2hex, 2, dataToEncrypt)
    hexToEncrypt = np.apply_along_axis(arrayToString, 1, hexToEncrypt)
    hexToEncrypt = str(np.apply_along_axis(arrayToString, 0, hexToEncrypt))





    data = bytes.fromhex(hexToEncrypt)
    iv = b"00000000"
    cipher = DES3.new(bytes(key), DES3.MODE_CFB,iv)


    d = cipher.decrypt(data)


    encryptedData = d.hex()


    stepOne = sliceStr(encryptedData,originalColumns*6)

    stepTwo = []

    for i in stepOne:
        stepTwo.append(sliceStr(i,6))

    stepThree = []
    for i in stepTwo:
        d = []
        for j in i:
            d.append(hexToRGB(j))

        if len(stepThree) != originalRows:
            stepThree.append(d)

        encryptedImg = np.asarray(stepThree)


    imageio.imwrite("decryptstest.png",encryptedImg)
    return stepThree










