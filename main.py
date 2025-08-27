import os
import random
import yaml
import cv2
import imageio
import urllib.request

data_path = "data"

with open('config/feelings.yaml', 'r') as file:
    feelings_dict = yaml.safe_load(file)

feelings = feelings_dict['reaction']

def get_reaction_meme(reaction):
    if reaction not in feelings:
        raise ValueError(f"Invalid reaction! Choose from {', '.join(feelings)}.")

    reaction_path = os.path.join(data_path, reaction)
    
    indian_path = os.path.join(reaction_path, "indian")
    
    if os.path.exists(indian_path) and os.listdir(indian_path):
        meme_list = os.listdir(indian_path)
        meme = random.choice(meme_list)
        meme_path = os.path.join(indian_path, meme)
    else:
        meme_list = os.listdir(reaction_path)
        meme = random.choice(meme_list)
        meme_path = os.path.join(reaction_path, meme)
    
    return meme_path

def show_gif(gif_meme_path):
    i = 0
    gif = imageio.mimread(gif_meme_path)
    nums = len(gif)
    imgs = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]
    while True:
        cv2.imshow("gif", imgs[i])
        if cv2.waitKey(100)&0xFF == 27:
            break
        i = (i+1)%nums
    cv2.destroyAllWindows()

def main():
    reaction = input(f"Enter a reaction from {', '.join(feelings)}: ").lower().strip()
    
    try:
        meme_path = get_reaction_meme(reaction)
        if os.path.isfile(meme_path):
            filename, file_extension = os.path.splitext(meme_path)
            print(f"Here's your meme: {meme_path}")
            if file_extension == ".gif":
                show_gif(meme_path)
            else:
                image = cv2.imread(meme_path)
                cv2.imshow("meme", image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        else:
            main()

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()