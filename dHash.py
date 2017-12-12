class DHash(object):

    def calculate_hash(image):
        """
        compute the dHash value for image
        :param image: PIL.Image
        :return: dHash,(string)
        """
        difference = DHash.__difference(image)
      
        decimal_value = 0
        hash_string = ""
        for index, value in enumerate(difference):
            if value:  # value为0, 
                decimal_value += value * (2 ** (index % 8))
            if index % 8 == 7: 
                hash_string += str(hex(decimal_value)[2:].rjust(2, "0"))  # fill up with 0 0xf=>0x0f
                decimal_value = 0
        return hash_string


    def hamming_distance(first, second):
        """
        
        :param first: Image or dHash (str)
        :param second: Image dHash (str)
        :return: hamming distance. 
        """
        # A. dHash calculate hamming distance
        if isinstance(first, str):
            return DHash.__hamming_distance_with_hash(first, second)

        # B. calculate hamming_distance for images
        hamming_distance = 0
        image1_difference = DHash.__difference(first)
        image2_difference = DHash.__difference(second)
        for index, img1_pix in enumerate(image1_difference):
            img2_pix = image2_difference[index]
            if img1_pix != img2_pix:
                hamming_distance += 1
        return hamming_distance


    def __difference(image):

        resize_width = 9
        resize_height = 8
        # 1. resize to (9,8)
        smaller_image = image.resize((resize_width, resize_height))
        # Grayscale
        grayscale_image = smaller_image.convert("L")
        # 
        pixels = list(grayscale_image.getdata())
        difference = []
        for row in range(resize_height):
            row_start_index = row * resize_width
            for col in range(resize_width - 1):
                left_pixel_index = row_start_index + col
                difference.append(pixels[left_pixel_index] > pixels[left_pixel_index + 1])
        return difference


    def __hamming_distance_with_hash(dhash1, dhash2):

        difference = (int(dhash1, 16)) ^ (int(dhash2, 16))
        return bin(difference).count("1")

