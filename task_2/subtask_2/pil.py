from PIL import Image

def main():
    image = Image.open(r"C:\Users\mohamed\AUR-Training-26\.vscode\task_2\subtask_2\images.jpg")
    bw_image = image.convert("L") #converts rgb to greyscale 
    bw_image.show()

main()

#the program couldn't find the image file even though it is in the same directory as the python code , so i copied the path of the image 