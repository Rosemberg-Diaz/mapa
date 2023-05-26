import base64
'''La función encode_img(nombre) recibe el nombre de un archivo de imagen como entrada y devuelve una representación codificada de la imagen en formato base64.'''
def encode_img(nombre):
    image = open(nombre, 'rb')
    image_read = image.read()
    encoded_bytes = base64.b64encode(image_read)
    encoded_string = encoded_bytes.decode('utf-8')
    return (encoded_string)

print(encode_img("empleado.png"))