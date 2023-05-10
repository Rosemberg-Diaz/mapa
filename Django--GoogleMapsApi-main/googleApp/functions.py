import base64

def encode_img(nombre):
    image = open(nombre, 'rb')
    image_read = image.read()
    encoded_bytes = base64.b64encode(image_read)
    encoded_string = encoded_bytes.decode('utf-8')
    return (encoded_string)

print(encode_img("empleado.png"))