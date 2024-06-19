# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 14:01:33 2024

@author: 23kmk24
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import filedialog, Toplevel, Listbox, Scrollbar, VERTICAL

def load_file_and_select_column_gui():
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを表示しない
    file_path = filedialog.askopenfilename()  # ファイル選択

    if not file_path:
        print("File not selected.")
        return None, None

    df = pd.read_csv(file_path)
    
    selected_column = tk.StringVar(value="")

    def on_confirm():
        selected_index = lb.curselection()
        if selected_index:
            selected_column.set(lb.get(selected_index))
        select_window.destroy()
        root.quit()

    select_window = Toplevel(root)
    select_window.title("Select a Column")

    lb = Listbox(select_window, exportselection=0)
    lb.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(select_window, orient=VERTICAL)
    scrollbar.config(command=lb.yview)
    scrollbar.pack(side="right", fill="y")

    lb.config(yscrollcommand=scrollbar.set)

    col_names = df.columns.tolist()[1:]  # 1列目を横軸として使用するため、列選択から除外
    for item in col_names:
        lb.insert("end", item)

    confirm_button = tk.Button(select_window, text="Confirm", command=on_confirm)
    confirm_button.pack()

    root.mainloop()

    if selected_column.get():
        return df, selected_column.get()
    else:
        print("Column not selected.")
        return None, None

def plot_with_flags(df, selected_column):
    df['Flag'] = 0  # フラグ列の追加
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)

    def onclick(event):
        if event.inaxes != ax_button:
            x, y = event.xdata, event.ydata
            distances = np.sqrt((df[df.columns[0]].values - x) ** 2 + (df[selected_column].values - y) ** 2)
            nearest_index = np.argmin(distances)
            df.iloc[nearest_index, df.columns.get_loc('Flag')] = 1
            redraw()

    def redraw():
        ax.clear()
        ax.plot(df[df.columns[0]], df[selected_column], label=selected_column)
        flagged = df[df['Flag'] == 1]
        ax.plot(flagged[flagged.columns[0]], flagged[selected_column], 'ro', markersize=10)
        plt.draw()

    def save_data(event):
        output_filename = filedialog.asksaveasfilename(defaultextension=".csv")
        if output_filename:
            # 横軸として使用した列、選択した縦軸として利用した列、フラグを示している列のみを出力
            output_df = df[[df.columns[0], selected_column, 'Flag']]
            output_df.to_csv(output_filename, index=False)
            print(f"Data saved to {output_filename}")
            plt.close(fig)  # グラフウィンドウを閉じる

    redraw()

    ax_button = plt.axes([0.81, 0.05, 0.1, 0.075])
    button = Button(ax_button, 'Complete')
    button.on_clicked(save_data)

    fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()

while True:
    df, selected_column = load_file_and_select_column_gui()
    if df is not None and selected_column is not None:
        plot_with_flags(df, selected_column)
    else:
        break  # ファイルが選択されなかった場合、ループを抜けてプログラムを終了します．
