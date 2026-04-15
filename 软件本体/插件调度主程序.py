import PySimpleGUI as sg
from tkinterdnd2 import DND_FILES, TkinterDnD
import re
import sys

def parse_dropped_files(data):
    data = data.strip()
    if not data:
        return []
    if '{' in data and '}' in data:
        return re.findall(r'{([^{}]*)}', data)
    if '\n' in data:
        return [p for p in data.split('\n') if p.strip()]
    if ' ' in data:
        parts = data.split(' ')
        return [p for p in parts if p.strip()]
    return [data]

root = TkinterDnD.Tk()
root.withdraw()

layout = [
    [sg.Text("拖入文件，可以选中一个或多个移除")],
    [sg.Listbox(values=[], size=(80, 15), key="-FILE_LIST-", select_mode=sg.SELECT_MODE_EXTENDED)],
    [sg.Button("清空所有"), sg.Button("移除选中")],
    [sg.Text("字幕处理相关")],
    [sg.Button("占位1", size=(10, 1))]
]

window = sg.Window("Re插件调度台", layout, finalize=True, location=(500,300))

listbox_widget = window["-FILE_LIST-"].Widget
listbox_widget.drop_target_register(DND_FILES)
listbox_widget.dnd_bind('<<Drop>>', lambda e: on_drop(e, window))


# 用一个独立的 Python 列表来存储所有文件路径
file_list = []

def update_listbox():
    """同步更新列表框显示"""
    window["-FILE_LIST-"].update(values=file_list)
    print(f"更新列表框: {file_list}")

if len(sys.argv) > 1:
    print("从命令行参数添加文件:")
    for file_path in sys.argv[1:]:
        file_list.append(file_path)
        print(f"添加: {file_path}")
    update_listbox()

def on_drop(event, window):
    global file_list
    raw_data = event.data
    print("\n=== 拖放事件 ===")
    print("原始数据:", repr(raw_data))
    new_paths = parse_dropped_files(raw_data)
    print("新拖入的路径:", new_paths)
    # 去重添加
    added = 0
    for p in new_paths:
        if p not in file_list:
            file_list.append(p)
            added += 1
    print(f"添加了 {added} 个新文件")
    print(f"当前文件列表: {file_list}")
    update_listbox()
    print("===============\n")

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "清空所有":
        file_list.clear()
        update_listbox()
        print("\n手动清空所有文件\n")

    if event == "移除选中":
        print("\n=== 移除选中事件 ===")
        selected_values = values["-FILE_LIST-"]  # 选中的值
        print("选中的值:", selected_values)
        if not selected_values:
            sg.popup("请先选中要移除的项目")
        else:
            # 从 file_list 中删除选中的项
            original_len = len(file_list)
            for item in selected_values:
                if item in file_list:
                    file_list.remove(item)
            print(f"删除了 {original_len - len(file_list)} 个文件")
            print(f"剩余文件列表: {file_list}")
            update_listbox()
        print("==================\n")
    
    if event == "占位1":
        sg.popup("这是一个占位按钮，可以绑定其他功能")

window.close()