import pytesseract
import os
import concurrent.futures

# def list_folders(path):
#     folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
#     print(folders)
#     return folders

def get_txt(png):
    text = pytesseract.image_to_string(f"press-room/{png}")
    with open(f"press-room-text/{png}_text.txt", "w") as f:
        #print(text)
        f.write(text)
        print(f"written press-room-text/{png}_text.txt")

def thread_get_txt(png_files, max_threads=100):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(get_txt, png) for png in png_files]
        concurrent.futures.wait(futures)

def main():
    png_files = [file for file in os.listdir(f"press-room/") if file.endswith('.png')]
    os.system('mkdir press-room-text/ > /dev/null 2>&1')
    thread_get_txt(png_files)

if __name__ == "__main__":
    main()