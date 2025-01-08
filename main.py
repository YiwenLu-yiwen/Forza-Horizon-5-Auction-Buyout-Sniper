import os
import cv2
import time
import numpy as np
import pyautogui as pyau
import pydirectinput as pydi
import pygetwindow as gw

def find_image_with_percentage(image_path, region=None, width_ratio=1, height_ratio=1):
    # Take a screenshot and convert it to a format suitable for OpenCV
    screenshot = pyau.screenshot(region=region)
    screenshot_cv = np.array(screenshot)
    screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    screenshot_cv = cv2.resize(screenshot_cv, (int(screenshot_cv.shape[1]/width_ratio), int(screenshot_cv.shape[0]/height_ratio)))
    result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
    return result

def find_max_percentage_image(image_path, region=None, width_ratio=1, height_ratio=1, threshold=0.8):
    """ This function find the location with the highest probability matching the given image 
    """
    if type(image_path) == str:
        image_path = [image_path]
    return_index = True if len(image_path) > 1 else False
    _index = 0
    _error = 5*width_ratio
    best_prob = 0
    best_loc = ()
    for each_image_path in image_path:
        result = find_image_with_percentage(each_image_path, region=region, width_ratio=width_ratio, height_ratio=height_ratio)
        loc = np.where(result >= threshold)
        for pt in zip(*loc[::-1]):
            added= True
            if added and best_prob < result[pt[1], pt[0]]:
                best_prob = result[pt[1], pt[0]]
                best_loc = (pt[0], pt[1])
                best_index = _index
        _index += 1
    if best_loc: 
        # print("Best Prob:", best_prob)
        if return_index:
            return best_loc, best_index
        return best_loc
    return None

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
    
def click_image(image_path, search_region, width_ratio, height_ratio, threshold):
    best_loc = find_max_percentage_image(image_path, search_region, width_ratio, height_ratio, threshold)
    left, top, width, height = search_region
    if best_loc:
        pydi.press('enter')
        return True
    return False

def main():
    threshold=0.8
    game_title = "Forza Horizon 5"

    left, top, width, height = measure_game_window(game_title)
    width_ratio, height_ratio = 1, 1
    search_region_auction = (230+left, 590+top, 910, 310)
    search_region_carpage = (790+left, 190+top, 810, 90)
    search_region_bid = (520+left, 400+top, 610, 80)
    search_region_carpage2 = (60+left, 165+top, 180, 40)

    current_directory = os.getcwd()

    image_path_SA = current_directory + '/images/SA.png'
    image_path_CF = current_directory + '/images/CF.png'
    image_path_AT = current_directory + '/images/AT.png'
    image_path_BF = current_directory + '/images/BF.png'
    image_path_PB = current_directory + '/images/PB.png'
    image_path_BS = current_directory + '/images/BS.png'
    image_path_NB = current_directory + '/images/NB.png'
    image_path_VS = current_directory + '/images/VS.png'
    
    print('Welcome to the Forza 5 BUYOUT Snipper')
    print('The script will start in 5 seconds')
    time.sleep(5)
    print('Starts')

    while True:
        vertify_click_SA = click_image(image_path_SA, search_region_auction, width_ratio, height_ratio, threshold)
        time.sleep(0.1)
        vertify_click_CF = click_image(image_path_CF, search_region_auction, width_ratio, height_ratio, threshold)
        time.sleep(0.5)
        found_carpage = find_max_percentage_image(image_path_AT, search_region_carpage, width_ratio, height_ratio, threshold)
        # if found car in stock
        if found_carpage:
            stop = False
            while not stop:
                time.sleep(0.4)
                pydi.press('y')
                time.sleep(0.15)
                # detect whether we can place bid, if not it means we either missed it or still loading
                found_bid = find_max_percentage_image(image_path_PB, search_region_bid, width_ratio, height_ratio, threshold)
                found_outbid = find_max_percentage_image(image_path_VS, search_region_bid, width_ratio, height_ratio, threshold)
                if found_bid or found_outbid: stop = True

            # if found buy option
            if found_bid:
                pydi.press('s')
                pydi.press('enter')
                pydi.press('enter')
                time.sleep(5)
                stop = False

                # get the bid result
                while not stop:
                    found_buyoutfail = find_max_percentage_image(image_path_BF, search_region_bid, width_ratio, height_ratio, threshold)
                    found_buyoutsuccess = find_max_percentage_image(image_path_BS, search_region_bid, width_ratio, height_ratio, threshold)
                    if found_buyoutfail:
                        print('BUYOUT Failed!')
                        pydi.press('enter')
                        pydi.press('esc')
                        stop = True
                    if found_buyoutsuccess:
                        print('BUYOUT Success!')
                        pydi.press('enter')
                        pydi.press('esc')
                        stop = True
            else:
                pydi.press('esc')
                time.sleep(0.1)
        # return to main auction page
        if found_carpage or vertify_click_CF or find_max_percentage_image(image_path_NB, search_region_carpage2, width_ratio, height_ratio, threshold):
            pydi.press('esc')
        time.sleep(0.4)

if __name__ == "__main__":
    main()
