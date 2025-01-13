import os
import cv2
import time
import numpy as np
import pandas as pd
from openpyxl import load_workbook
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

def go_to_MAKE(old_make, old_CAR_MODEL_ORDER, new_make, new_CAR_MODEL_ORDER):
    x, y = np.array(old_make) - np.array(new_make)
    if x!=0 or y!=0:
        pydi.press('enter')
        time.sleep(0.3)
        multi_press_cond('a', 'd', x)
        multi_press_cond('w', 's', y)
        pydi.press('enter')
        time.sleep(0.3)
    multi_press('s', 1)
    if x ==0 and y == 0: # same brand
        CAR_MODEL_move = new_CAR_MODEL_ORDER-old_CAR_MODEL_ORDER
    else:
        CAR_MODEL_move = new_CAR_MODEL_ORDER
    multi_press_cond('d', 'a', CAR_MODEL_move)
    multi_press('s', 5)
    pydi.press('enter')

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
    
def press_image(image_path, search_region, width_ratio, height_ratio, threshold):
    best_loc = find_max_percentage_image(image_path, search_region, width_ratio, height_ratio, threshold)
    left, top, width, height = search_region
    if best_loc:
        pydi.press('enter')
        return True
    return False

def click_left():
    # Simulate the left mouse click
    pydi.mouseDown()
    time.sleep(0.05)
    pydi.mouseUp()

def write_excel(data, output_path, sheet_name):
    # write dataframe to excel and format the excel
    data.to_excel(output_path, index=False, sheet_name=sheet_name)

    workbook = load_workbook(output_path)
    sheet = workbook.active
    sheet.auto_filter.ref = sheet.dimensions
    for col in sheet.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                # Calculate the maximum length of values in the column (including the header)
                max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        # Adjust the column width
        sheet.column_dimensions[col_letter].width = max_length + 2
    # Save the workbook with adjusted widths
    workbook.save(output_path)

def main():
    threshold=0.8
    game_title = "Forza Horizon 5"

    # screenshot regions here
    left, top, width, height = measure_game_window(game_title)
    width_ratio, height_ratio = 1, 1
    search_region_auction = (230+left, 590+top, 910, 310)
    search_region_carpage = (790+left, 190+top, 810, 90)
    search_region_bid = (520+left, 380+top, 610, 100)
    search_region_carpage2 = (60+left, 165+top, 180, 40)
    current_directory = os.getcwd()

    # screenshots here
    image_path_SA = current_directory + '/images/SA.png'
    image_path_CF = current_directory + '/images/CF.png'
    image_path_AT = current_directory + '/images/AT.png'
    image_path_BF = current_directory + '/images/BF.png'
    image_path_PB = current_directory + '/images/PB.png'
    image_path_BS = current_directory + '/images/BS.png'
    image_path_NB = current_directory + '/images/NB.png'
    image_path_VS = current_directory + '/images/VS.png'
    image_path_AO = current_directory + '/images/AO.png'

    # car info details here
    car_info_file_path = "./FH5_all_cars_info_v3.xlsx"
    car_sheet_name = 'all_cars_info'

    print('Welcome to the Forza 5 CAR BUYOUT Snipper')
    print('The script will start in 5 seconds')
    time.sleep(5)
    print('Starts')

    change_make = True
    new_make, new_CAR_MODEL_ORDER = (0,0), 0
    missed_match_times = 0
    start_time, all_snipe_index, failed_snipe = 0, [], False
    while True:
        end_time = time.time()
        if end_time - start_time > 1800:
            change_make = True
            failed_snipe = True
        vertify_press_SA = press_image(image_path_SA, search_region_auction, width_ratio, height_ratio, threshold)
        time.sleep(0.1)
        # change car here
        if change_make and find_max_percentage_image(image_path_CF, search_region_auction, width_ratio, height_ratio, threshold):
            if failed_snipe:
                failed_snipe=False
                print('TIME OUT, Switching to Next Auction Sniper!')
            start_time = time.time()
            vertify_press_CF = True
            change_make = False
            # read file and filter non-zero cars
            df = pd.read_excel(car_info_file_path, car_sheet_name)
            if len(df[df['BUYOUT NUM'] > 0]) == 0:
                print('Finish Sniping!')
                break
            all_snipe_index = df[df['BUYOUT NUM'] > 0].index.tolist() if all_snipe_index == [] else all_snipe_index
            index = all_snipe_index.pop()
            old_make, old_CAR_MODEL_ORDER = new_make, new_CAR_MODEL_ORDER

            CAR_MAKE,CAR_MAKE_LOCATION, CAR_MODEL_Full_Name, CAR_MODEL_Short_Name, CAR_MODEL_LOCATION = df.iloc[index,].values[:5]
            new_make, new_CAR_MODEL_ORDER = eval(CAR_MAKE_LOCATION), CAR_MODEL_LOCATION
            print('Sniping',CAR_MAKE, CAR_MODEL_Full_Name)   
            # modify car details
            multi_press('w', 6) # one more move make sure it goes smoothly
            go_to_MAKE(old_make, old_CAR_MODEL_ORDER, new_make, new_CAR_MODEL_ORDER)
        else:
            vertify_press_CF = press_image(image_path_CF, search_region_auction, width_ratio, height_ratio, threshold)
        time.sleep(0.5)
        found_carpage = find_max_percentage_image(image_path_AT, search_region_carpage, width_ratio, height_ratio, threshold)
        # if found car in stock
        if found_carpage:
            stop = False
            while not stop:
                time.sleep(0.1)
                pydi.press('y')
                # detect whether we can place bid, if not it means we either missed it or still loading
                found_bid = find_max_percentage_image(image_path_PB, search_region_bid, width_ratio, height_ratio, threshold)
                found_outbid = find_max_percentage_image(image_path_VS, search_region_bid, width_ratio, height_ratio, threshold)
                found_auction_option = find_max_percentage_image(image_path_AO, search_region_bid, width_ratio, height_ratio, threshold)
                if found_bid or found_outbid or found_auction_option: stop = True

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
                        # Change to the next car
                        df.loc[index, 'BUYOUT NUM'] = df['BUYOUT NUM'][index]-1
                        write_excel(df, car_info_file_path, car_sheet_name)
                        if df.loc[index, 'BUYOUT NUM'] == 0:
                            change_make = True
                            old_make, old_CAR_MODEL_ORDER = new_make, new_CAR_MODEL_ORDER
                        pydi.press('enter')
                        pydi.press('esc')
                        stop = True
            else:
                print('BUYOUT Missed!')
                pydi.press('esc')
                time.sleep(0.1)
        # if stuck somewhere unknown, this may work
        if vertify_press_SA==False and vertify_press_CF==False and found_carpage==None:
            pyau.moveTo(left+20, top+20, duration=0.001)
            click_left()
            if missed_match_times >=2:
                pydi.press('esc')
            missed_match_times += 1
        else:
            missed_match_times = 0
        # return to main auction page
        if found_carpage or vertify_press_CF or find_max_percentage_image(image_path_NB, search_region_carpage2, width_ratio, height_ratio, threshold):
            pydi.press('esc')
        time.sleep(0.4)

if __name__ == "__main__":
    main()
