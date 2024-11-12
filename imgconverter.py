import argparse
import os.path
import PIL.ImageFile
from PIL import Image


format_list = ['JPG', 'PNG', 'GIF', 'BMP']
# format_list = ['jpg', 'png', 'gif', 'bmp']

parser = argparse.ArgumentParser(description="Image convertor")
parser.add_argument('-i', '--input', type=str, help="Import images from valid directory or select image file", required=True)
parser.add_argument('-f', '--format', type=str, help="Select the original format", choices=format_list, required=True)
parser.add_argument('-o', '--out', type=str, help="Output directory for converted images", required=True)
parser.add_argument('-r', '--Return', type=str, help="Select the output format", choices=format_list, required=True)
args = parser.parse_args()

# En ordbok där nyckeln matchar argumentet från -f och -r. (imgconvert.py -f JPG -r PNG)
formats = {'jpg': '.jpg', 'png': '.png', 'gif': '.gif', 'bmp': '.bmp', }


def path_validator(import_dir_path, output_dir_path):

    if not os.path.exists(import_dir_path):
        print("No such file or directory: '%s' " % import_dir_path)
        exit(0)
    if not os.path.exists(output_dir_path):
        try:
            os.makedirs(output_dir_path)
        except OSError as exc:
            print(exc.args[1])
            print(f"Could not create path: '{output_dir_path}'")
            exit(0)


def img_convertor(import_dir_path, img_format, output_dir_path, return_image):
    found_img_format = False

    # i fall argumenter -f,-r är lower case
    img_format = img_format.lower()
    return_image = return_image.lower()

    output_dir_path = os.path.join(output_dir_path, 'out')  # Default directory /out. Lägger automatiskt till out mappen. Bara kommentera raden om inte behövs.

    path_validator(import_dir_path, output_dir_path)

    if os.path.isdir(import_dir_path):  # Om -i sökvägen är en mapp med filer
        for root, dirs, files in os.walk(import_dir_path):  # gå igenom alla filer i mappen
            for filename in files:
                full_path_filename = os.path.join(root, filename)

                # Undantag till .JPEG som har 5 tecknen i extention.
                if filename.lower().endswith('.jpeg'):  # Skriptet ändrar extention till 4 tecknen (.jpg) För att sedan hämta värdet från ordboken med nyckel.
                    filename = filename.split('.')[-2] + '.jpg'  #  Men behåller det original namnet

                if filename.lower().endswith(formats.get(img_format)):  #  Ordboken returnerar önskat format att infoga i filen extention
                    found_img_format = True

                    new_filename = filename.split('.')[-2] + formats.get(return_image)  # Behåller det original filnamnet och byter ut bara de sista 4 tecknen till ett ny formatet i filnamnet
                    output_new_file_path = os.path.join(output_dir_path, new_filename)  # Fullständiga sökvägen för den nya filen till image.save()

                    if os.path.exists(output_new_file_path):  # Skriptet kommer inte att skriva över filen om den redan finns
                        print(f"File already exists: '{os.path.basename(output_new_file_path)}'")
                        continue
                    try:
                        with Image.open(full_path_filename) as image:  # full_path_filename - Sökväg till original fil
                            image.save(output_new_file_path)  # Sparar en fil till den skapade sökvägen med ett önskat format
                            print(f"Successfully saved: '{os.path.basename(output_new_file_path)}'")
                    except PIL.UnidentifiedImageError:
                        print(f"ERROR! Cannot identify image file: '{full_path_filename}'")  # Om filen är skadad eller ogiltig

    elif os.path.isfile(import_dir_path):  # Om --input sökvägen är en enda fil
        filename = os.path.basename(import_dir_path)

        if filename.lower().endswith('.jpeg'):
            filename = filename.split('.')[-2] + '.jpg'

        if filename.lower().endswith(formats.get(img_format)):
            found_img_format = True
            new_filename = filename.split('.')[-2] + formats.get(return_image)
            output_new_file_path = os.path.join(output_dir_path, new_filename)

            if os.path.exists(output_new_file_path):
                print(f"File already exists: '{os.path.basename(output_new_file_path)}'")
                exit(0)

            try:
                with Image.open(import_dir_path) as image:
                    image.save(output_new_file_path)
                    print(f"Successfully saved: '{os.path.basename(output_new_file_path)}'")
            except PIL.UnidentifiedImageError:
                print(f"ERROR! Cannot identify image file: '{import_dir_path}'")

    if not found_img_format:
        print(f"Could not find {str(img_format).upper()} files ")


if __name__ == "__main__":

    img_convertor(args.input, args.format, args.out, args.Return)
