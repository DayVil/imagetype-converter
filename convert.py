import os
import sys
import argparse
import threading
import time
from PIL import Image


def eprint(*args, **kwargs) -> None:
    print("Error: ", end="", file=sys.stderr)
    print(*args, file=sys.stderr, **kwargs)


def gen_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs='+')
    parser.add_argument(
        "-t", "--type", choices=["png", "jpg", "jpeg"], dest="type", help="Type to convert to")
    parser.add_argument("-o", "--output", dest="output",
                        default="output", help="Outputs to a specified folder")
    args = parser.parse_args()
    return args


def convert(outputfile: str, input_file: str, folder_files: list[str], output_folder: str):
    start_time = time.time()
    print(f"Converting {input_file}\nto {outputfile}\nin {output_folder}\n")
    if outputfile not in folder_files:
        try:
            with Image.open(input_file) as image:
                image.save(os.path.join(output_folder, outputfile))
        except OSError:
            eprint("cannot convert image", input_file)
    print(
        "---\nfinished: {} in {:.2f}s\n---".format(outputfile, time.time()-start_time))


def main():
    args = gen_parser()
    if not os.path.isdir(args.output):
        try:
            os.mkdir(args.output)
        except Exception as e:
            eprint(e)
            exit()

    thread_list = []

    folder_files = os.listdir(args.output)
    for input in args.filename:
        file, _ = os.path.splitext(input)
        _, single_file = os.path.split(file)
        outputfile = single_file + "." + args.type
        abs_output_folder = os.path.abspath(args.output)

        thread = threading.Thread(target=convert, args=(
            outputfile, input, folder_files, abs_output_folder,))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == '__main__':
    main()
