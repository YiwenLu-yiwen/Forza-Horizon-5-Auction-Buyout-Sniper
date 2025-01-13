# grab model and download them into OCR_images
import pygetwindow as gw
import cv2
import numpy as np
import pyautogui as pyau
import easyocr
import pandas as pd
import time
import pydirectinput as pydi

reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory

def measure_game_window(title):
    """ Measure the game window size
    """
    try:
        game_window = gw.getWindowsWithTitle(title)[0]
        if game_window:
            if not game_window.isMinimized:
                game_window.restore()
            game_window.activate()
            # measure game window
            left, top, width, height = game_window.left, game_window.top, game_window.width, game_window.height
            print(f"Game window found: {title}")
            print(f"Size '{title}' is {width}x{height} pixels.")
            return left, top, width, height
        else:
            print("Game window not found. Check the title.")
    except IndexError:
        print("Game window not found. Make sure the title is correct.")
    except Exception as e:
        print(f"An error occurred: {e}")


def detect_model(region):
    img = pyau.screenshot(region=region)
    img_array = np.array(img)
    img_cv2 = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    model = reader.readtext(img_cv2)[0][-2]
    return model

def multi_press(button, _times):
    """Multi-press
    """
    for _ in range(_times):
        pydi.press(button)
        time.sleep(0.2)

def multi_press_cond(button1, button2, _times):
    if _times > 0:
        multi_press(button1, _times)
    else:
         multi_press(button2, abs(_times))

def go_to_MAKE(old_make, new_make):
    x, y = np.array(old_make) - np.array(new_make)
    if x!=0 or y!=0:
        pydi.press('enter')
        time.sleep(0.3)
        multi_press_cond('a', 'd', x)
        multi_press_cond('w', 's', y)
        pydi.press('enter')
        time.sleep(0.3)
    multi_press('s', 1)
    time.sleep(0.2)


def main():
    left, top, width, height = measure_game_window('Forza Horizon 5')
    choose_rewards_region = (860+left, 415+top, 300, 35)
    print('The script will start in 5 seconds')
    time.sleep(5)
    print('Starts')
    # make sure at the top
    multi_press('w', 7)
    df = pd.read_csv('./FH5_all_cars_info.csv')
    car_make_dict = dict(zip(df['CAR MAKE'], df['CAR MAKE LOCATION']))
    old_make_location = (0,0)
    model_list, order_list = [], []
    for car_make, new_car_make_location in car_make_dict.items():
        # start with any
        new_car_make_location = eval(new_car_make_location)
        go_to_MAKE(old_make_location, new_car_make_location)
        print('Next')
        _order, stop = 0, False
        while not stop:
            multi_press('d', 1)
            time.sleep(0.1)
            model = detect_model(choose_rewards_region)
            if model == 'ANY':
                stop=True
            else:
                _order += 1
                model_list.append(model)
                order_list.append(_order)
                print(_order, car_make, model)
            time.sleep(0.1)
        multi_press('w', 1)
        time.sleep(0.2)
        old_make_location = new_car_make_location

    df2 = pd.DataFrame({'CAR MODEL(Short Name)':model_list, 
                        'ORDER':order_list})

    df2.to_csv('./OCR_model_short_name.csv', index=False)

if __name__ == "__main__":
    main()