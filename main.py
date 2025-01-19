import os
import cv2
import ctypes
import time
import colorama
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
    # _error = 5*width_ratio
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

def move_mouse(x, y):
    # Move the mouse to the specified coordinates
    pyau.moveTo(x, y, duration=0.001)  # Move to (x, y) over 1 second

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

def active_game_window(title):
    game_window = gw.getWindowsWithTitle(title)[0]
    if game_window:
        try:
            game_window.activate()
        except:
            game_window.minimize()
            game_window.restore()
    return game_window

def measure_game_window(title):
    """ Measure the game window size
    """
    try:
        game_window = active_game_window(title)
        if game_window:
            game_window.resizeTo(1616, 939) # fix this
            # measure game window
            left, top, width, height = game_window.left, game_window.top, game_window.width, game_window.height
            print(f"\033[1;34;40mGame window found: \033[1;32;40m{title}\033[0m")
            # print(f"Size '{title}' is {width}x{height} pixels.")
            return left, top, width, height
        else:
            print("\033[1;31;40mGame window not found. Check the title.\033[0m")
    except IndexError:
        print("\033[1;31;40mGame window not found. Make sure the title is correct.\033[0m")
    except Exception as e:
        print(f"\033[1;31;40mAn error occurred: {e}.\033[0m")
        print(f"\033[1;31;40mTry to restart the script!\033[0m")
    
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

def exit_script():
    print(f'\033[1;31;40mScript exits in 5 seconds! \033[0m')
    time.sleep(5)
    print(f'\033[1;31;40mScript stops! \033[0m')
    
def convert_seconds(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return minutes, remaining_seconds

def multi_click_left(n):
    # click n times
    for _ in range(n):
        click_left()
        time.sleep(0.01)

def hold_key(button,secs=5):
    pyau.keyDown(button) #holds the key down
    time.sleep(secs)
    pyau.keyUp(button) #releases the key

def main():
    colorama.init(wrap=True)
    print('Welcome to the Forza 5 CAR BUYOUT Snipper')
    # add pre-check settings
    color_end_code = '\033[0m'
    red_code, blue_code, cyan_code, green_code, yellow_code = '\033[1;31;40m', '\033[1;34;40m', '\033[1;36;40m', '\033[1;32;40m', '\033[1;33;40m'
    print(f'{blue_code}Running Pre-check:{color_end_code} {cyan_code}Window resolution {color_end_code}and {cyan_code}Game resolution !{color_end_code}')
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    print(f'{cyan_code}Your Window Resolution is {screensize[0]}x{screensize[1]} !{color_end_code}')
    if screensize != (1920, 1080):
        print(f'{red_code}Sorry, script only works under 1920x1080 resolution! {color_end_code}')
        exit_script()
        return -1
    # check game resolution
    game_title = "Forza Horizon 5" 
    left, top, width, height = measure_game_window(game_title)
    print(f'{cyan_code}Resize {game_title} resolution to {width}x{height} pixels!{color_end_code}')
    
    # screenshot regions here
    threshold=0.8
    width_ratio, height_ratio = 1, 1
    current_directory = os.getcwd()
    search_region_auction = (230+left, 590+top, 910, 310)
    search_region_carpage = (790+left, 190+top, 810, 90)
    search_region_bid = (520+left, 380+top, 610, 100)
    search_region_carpage2 = (60+left, 165+top, 180, 40)
    
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
    print('The script will start in 5 seconds')
    time.sleep(5)
    print('Starts')

    change_make = True
    new_make, new_CAR_MODEL_ORDER = (0,0), 0
    missed_match_times = 1
    start_time, all_snipe_index, failed_snipe = 0, [], False
    first_start = True # add this to detect whether it is first start
    while True:

        end_time = time.time()
        if end_time - start_time > 1800:
            change_make = True
            failed_snipe = True
        # press search auction
        vertify_press_SA = press_image(image_path_SA, search_region_auction, width_ratio, height_ratio, threshold)
        time.sleep(0.1)
        # change car functions
        if change_make and find_max_percentage_image(image_path_CF, search_region_auction, width_ratio, height_ratio, threshold):
            # if time out, print this message
            if failed_snipe and not first_start:
                end_time = time.time()
                minutes, remaining_seconds = convert_seconds(end_time-start_time)
                print(f'[{minutes}:{remaining_seconds}] TIME OUT, Switching to Next Auction Sniper!')
            failed_snipe=False
            start_time = time.time() # initial start time
            vertify_press_CF = True
            change_make = False
            # read file and filter non-zero cars
            df = pd.read_excel(car_info_file_path, car_sheet_name)
            if len(df[df['BUYOUT NUM'] > 0]) == 0:
                print(f'{green_code}Finish Sniping!{color_end_code}')
                break
            # ignore car model location =-1
            all_snipe_index = df[(df['BUYOUT NUM'] > 0) & (df['CAR MODEL LOCATION']!=-1)].index.tolist() if all_snipe_index == [] else all_snipe_index
            index = all_snipe_index.pop()
            old_make, old_CAR_MODEL_ORDER = new_make, new_CAR_MODEL_ORDER

            CAR_MAKE,CAR_MAKE_LOCATION, CAR_MODEL_Full_Name, CAR_MODEL_Short_Name, CAR_MODEL_LOCATION = df.iloc[index,].values[:5]
            new_make, new_CAR_MODEL_ORDER = eval(CAR_MAKE_LOCATION), CAR_MODEL_LOCATION
            print(f'Sniping {blue_code}{CAR_MODEL_Full_Name}{color_end_code}')   
            # reset cursor
            move_mouse(left+10, top+40)
            multi_click_left(3)
            # car details
            multi_press('w', 6) # one more move make sure it goes smoothly
            # if first time, move to ANY
            if first_start:
                first_start = False
                # initial MAKE location to any
                pydi.press('enter')
                hold_key('w', 5)
                time.sleep(0.3)
                hold_key('a', 3)
                pydi.press('enter')
                time.sleep(0.3)
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
                        end_time = time.time()
                        minutes, remaining_seconds = convert_seconds(end_time-start_time)
                        print(f'[{minutes}:{remaining_seconds}] {red_code}BUYOUT Failed!{color_end_code}')
                        pydi.press('enter')
                        pydi.press('esc')
                        stop = True
                    if found_buyoutsuccess:
                        end_time = time.time()
                        minutes, remaining_seconds = convert_seconds(end_time-start_time)
                        print(f'[{minutes}:{remaining_seconds}] {green_code}BUYOUT Success!{color_end_code}')
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
                end_time = time.time()
                minutes, remaining_seconds = convert_seconds(end_time-start_time)
                print(f'[{minutes}:{remaining_seconds}] {yellow_code}BUYOUT Missed!{color_end_code}')
                pydi.press('esc')
                time.sleep(0.1)
        # if stuck somewhere unknown, this may work
        if vertify_press_SA==False and vertify_press_CF==False and found_carpage==None:
            print(f'{red_code}Fail to match anything. {missed_match_times}-th try to press ESC to see whether it works!{color_end_code}')
            active_game_window(game_title)
            pydi.press('esc')
            time.sleep(0.2)                
            if missed_match_times > 10:
                print(f'{red_code}Fail to detect anything, try to restart the script or game!{color_end_code}')
                exit_script()
                return -1
            missed_match_times += 1
        else:
            missed_match_times = 0
        # return to main auction page
        if found_carpage or vertify_press_CF or find_max_percentage_image(image_path_NB, search_region_carpage2, width_ratio, height_ratio, threshold):
            pydi.press('esc')
        time.sleep(0.4)

if __name__ == "__main__":
    main()
