# Forza-Horizon-5-Auction-Buyout-Sniper

This is the first script using image matching (e.g., OpenCV) to create a much faster and more stable macro for sniping a variety of desired cars in the auction house. Rather than sniping single specific cars, this script aims at fully collection for this game.

Note: This script DOESN'T gaurantee 100% to snipe the auctions. Due to network and other potential issues, you may run it for nothing or get quite a few cars within a long time.

This script is against [Forza Code of Conduct](https://support.forzamotorsport.net/hc/en-us/articles/360035563914-Forza-Code-of-Conduct#:~:text=Forza%20Code%20of%20Conduct%201%20The%20Driver%E2%80%99s%20Code,Suspensions%2FBanning%20...%204%20Appeals%20...%205%20Reporting%20), Use it as YOUR OWN RISK!

## Performance Preview (2MIN Demo)

In this demo, we let the script snipe these four cars `AUDI RS`, `AUDI R1`, `MEGANE R26 R`, `MINI COUNTRYMAN`.

![preview](archive/demo.gif)


## Result Preview
![Result](archive/script_result.PNG)
![ingame result](archive/game_success.png)

## Features

|Name         |Added version           |Breif introduction            |
| ------------- |:-------------:|:-------------:|
| ✅ Fast sniping                             |  v1.0          | Fast speed buyout |
| ✅ Enable single or multi auction snipers   |  v2.0          | Support one or many different car snipers      |
| ✅ Smart auto switch cars                   |  v3.0          | If one auction takes more than 30mins, switch to another car  |
| ✅ Easy set-up                              |  v4.0          | Only needs to set how many cars you want to buy |
| ✅ Memory efficient with 40MB(->80MB)       |  v1.1(->v4.0)  | Less memory costs      |
| ✅ Include all car info                     |  v4.0          | Include short_name, seasons, DLC, Autoshow,etc    |
| ✅ Game pre-check                           |  v4.0          | Game and windows resolution pre-check |
| ✅ Few auction house setting                |  v5.0          | Only needs to set Price|
|         |            |

## Limits:
1. [FH5_all_cars_info_v3.xlsx](https://github.com/YiwenLu-yiwen/Forza-Horizon-5-Auction-Buyout-Sniper/blob/main/FH5_all_cars_info_v3.xlsx) must be up to date. Otherwise, it may buy different cars.

## Future Work
- [ ] Apply a better interface rather than console.
- [ ] Fit any resolution.

## Pre-Requirements
1. System Requirements:

    This script only tests well on windows 10 with 1920*1080 (100% scale).

    ![system requirement](archive/system_setting.png)

2. Game setting: 
    
    I am using [Hyper-V](https://github.com/jamesstringerparsec/Easy-GPU-PV), a GPU Paravirtualization on Windows like virtual box on MacOS. Therefore, the HDR setting shows wired here. But it doesn't matter.

    ![video setting](archive/video_setting.png)

    To save energy and gpu cost, strongly suggest to set "VERY LOW" in grahic setting.

    ![Graphic setting](archive/graphics_setting.png)

3. Default language is English, any other language should replace all screenshots (See images folder, DON'T CHANGE FILE NAME)

4. Modify the [CARS.csv](https://github.com/YiwenLu-yiwen/Forza-Horizon-5-Auction-Buyout-Sniper/blob/main/FH5_all_cars_info_v3.csv)

    For introduction of `CAR MAKE LOCATION` and `CAR MODEL LOCATION`, please see previous tags.
    
    Now, only need to set `BUY NUM` in the file. Super simple and easy!!!
   
## How to run it
1. Run with Python
    
    Python version must below 3.13
```
Git Clone https://github.com/YiwenLu-yiwen/Forza-Horizon-5-Auction-Buyout-Sniper.git
cd Forza-Horizon-5-Auction-Buyout-Sniper
pip install -r requirements.txt
python main.py
```

2. Use Compiled Zip 

    Steps: 
    1. Download zip file on [release page](https://github.com/YiwenLu-yiwen/Forza-Horizon-5-Auction-Buyout-Sniper/releases).
    2. Modify the images folder.(No need if you are satisfied pre-requirements)
    3. Modify the `FH5_all_cars_info_v3.csv`.
    4. Run the exe.

## Start and Enjoy
1. Make sure you have checked all above info.

2. Modify the `FH5_all_cars_info_v3.csv` for your own needs.

3. Optional: Set auction price. 

4. Stay with this screen (Search auctions must be active), then run the script or exe.

![Auction House](archive/auction_house.png)
