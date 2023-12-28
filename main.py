# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import numpy as np
import os


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    raw_data_path = r'D:\BaiduNetdiskDownload\极客时间-大数据项目训练营\11、Flink\2、数据资料\UserBehavior\UserBehavior.csv'
    save_data_path = r'D:\BaiduNetdiskDownload\极客时间-大数据项目训练营\11、Flink\2、数据资料\UserBehavior.csv'
    raw_data = pd.read_csv(raw_data_path)
    raw_data = raw_data.iloc[:100000]
    raw_data.to_csv(save_data_path, index=False)


