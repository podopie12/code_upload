from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog
from threading import Thread, Event
from PIL import Image, ImageTk, ImageFilter

import threading
import os
import subprocess
import shutil
import time

# 스레드를 위한 이벤트 셋
event = Event()

# 현재 작업 디렉토리 얻기
current_working_directory = os.getcwd()

# 출력 경로 설정
OUTPUT_PATH = Path(current_working_directory)

# 에셋(자원) 디렉토리의 상대 경로 설정
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")

# 그림 파일에 대한 변수 사전설정
global image_tree, image_car, image_cloud, image_fill_star, image_star, image_sun, image_tire, button_upload
global image_Red_light, image_Orange_light, image_Green_light
# 에셋 폴더경로 불러오기
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# 폴더에 있는 이미지 파일 이름 가져오기
def get_single_image_file(path):
    files = os.listdir(path)
    image_files = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    if len(image_files) == 1:
        return image_files[0]
    elif len(image_files) == 0:
        return "해당 경로에 이미지 파일이 없습니다."
    else:
        return "해당 경로에 여러 개의 이미지 파일이 있습니다. 정확한 경로를 지정하세요."

# GUI2 텍스트 업로드 함수
def update_text(new_text):
    global test_text
    test_text = new_text
    canvas.itemconfig(test_text_ID, text=f"{test_text}")
    window.update()
    time.sleep(1.5)
# 자동차 사진 움직이기
def move_car():
     while True:
        x, _ = canvas.coords(image_car_2_ID)
        if x >= 400:
            canvas.coords(image_car_2_ID, -30, 356)
        else:
            canvas.move(image_car_2_ID, 1, 0)
        time.sleep(0.01)
        if event.is_set():
            print("move car stopping")
            return

# 스레드 설정 후 병렬 실행
def thread_set():
    second_gui()

    move_car_thread = threading.Thread(target=move_car)
    save_image_thread = threading.Thread(target=save_image)
    
    move_car_thread.start()
    save_image_thread.start()

#타이어 수명 콘솔로 출력
def read_tire_life():
    tire_life_path = os.path.join(current_working_directory, "tire_life.txt")
    try:
        with open(tire_life_path, "r") as file:
            # Assuming the file contains a single line with a float
            tire_life = float(file.read().strip())
            print(f"Tire life: {tire_life}")
            return tire_life
    except FileNotFoundError:
        print("tire_life.txt not found.")
    except ValueError:
        print("Error reading tire life from tire_life.txt.")

# 이미지 처리함수
def save_image():
    
    # 폴더경로 설정
    folder_path = os.path.join(current_working_directory, "Target_folder")
    
    # Open a file dialog to choose an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        # Check if the folder exists
        if os.path.exists(folder_path):
            # If it exists, remove the folder and its contents
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' and its contents removed.")
            update_text(f"Folder '{folder_path}'\n and its contents removed.")
        
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder test_folder created at: {folder_path}")
        update_text(f"Folder test_folder created at: \n{folder_path}")
        
        # Get the filename from the path
        file_name = os.path.basename(file_path)
        
        # Copy the selected image to the new folder
        destination_path = os.path.join(folder_path, file_name)
        shutil.copyfile(file_path, destination_path)

        print(f"Selected image '{file_name}' saved in the folder.")
        update_text(f"Selected image '{file_name}'\n saved in the folder.")
        
        # Run cut_img_16.exe
        cut_img_exe_path = os.path.join(current_working_directory, "cut_img_16.exe")
        print("execute cut_img_16.exe")
        update_text("execute cut_img_16.exe")
        subprocess.run([cut_img_exe_path])
        print("cut_img_16.exe execution completed.")
        update_text("cut_img_16.exe execution completed.")
        
        # Run life_check.exe
        life_exe_path = os.path.join(current_working_directory, "life_check.exe")
        print("excute life_check.exe")
        update_text("excute life_check.exe")
        subprocess.run([life_exe_path])
        print("life_check.exe execution completed.")
        update_text("life_check.exe execution completed.")
        
        read_tire_life()
        update_text("데이터가 추출되었습니다.")
        
        update_text("곧 결과가 출력됩니다.")
        time.sleep(4)
        global tire_life
        tire_life= read_tire_life()
        
        event.set()
        
        third_gui()
        # Read tire_life.txt after life_check.exe completes    
        return
    
# 첫 번째 GUI창
def init():    
    image_tire_1_ID = canvas.create_image(
        151.0,
        122.0,
        image=image_tire
    )

    canvas.create_text(
        38.0,
        241.0,
        anchor="nw",
        text="타이어 수명 측정하기",
        fill="#000000",
        font=("arial bold", 25 * -1)
    )

    canvas.create_text(
        122.0,
        307.0,
        anchor="nw",
        text="30초",
        fill="#000000",
        font=("arial bold", 20 * -1)
    )

    canvas.create_text(
        10.0,
        340.0,
        anchor="nw",
        text="지금 바로 내 타이어의 잔여 수명을 확인가능",
        fill="#000000",
        font=("arial bold", 14 * -1)
    )

    image_fill_star_1_ID = canvas.create_image(
        284.0,
        16.0,
        image=image_fill_star
    )

    global button_upload_1_ID
    button_upload_1_ID = Button(
        image=button_upload,
        borderwidth=0,
        highlightthickness=0,
        command= thread_set,
        relief="flat"
    )
    button_upload_1_ID.place(
        x=15.0,
        y=407.0,
        width=269.0,
        height=47.0
    )
    window.resizable(False, False)
    window.mainloop()

# 두 번째 GUI창
def second_gui():
    
    # 이전 GUI 초기화
    canvas.delete("all")
    button_upload_1_ID.destroy()
    
    image_tree_2_ID = canvas.create_image(
        182.0,
        343.0,
        image=image_tree
    )

    image_tire_2_ID = canvas.create_image(
        151.0,
        122.0,
        image=image_tire
    )

    image_fill_star_2_ID = canvas.create_image(
        284.0,
        16.0,
        image=image_fill_star
    )
    
    test_text = ""
    global test_text_ID
    test_text_ID = canvas.create_text(
        150.0,
        454.0,
        anchor="center",
        text=f"{test_text}",
        fill="#000000",
        font=("arial bold", 10 * -1)
    )
    
    canvas.create_text(
        58.0,
        384.0,
        anchor="nw",
        text="30초 정도 소요됩니다. \n잠시만 기다려주세요",
        fill="#000000",
        font=("arial bold", 20 * -1)
    )

    canvas.create_rectangle(
        0,
        368.9999999745712,
        300,
        372.0,
        fill="#000000",
        outline=""
    )

    image_cloud_2_ID = canvas.create_image(
        109.0,
        265.0,
        image=image_cloud
    )

    image_sun_2_ID = canvas.create_image(
        232.0,
        242.0,
        image=image_sun
    )

    # 이동을 위해 global param으로 선언
    global image_car_2_ID
    image_car_2_ID = canvas.create_image(
        50.0,
        356.0,
        image=image_car
    )
    
    window.update()

# 3번째 GUI창  
def third_gui():
    
    # 이전 GUI 초기화
    canvas.delete("all")
    
    CURRENT_TIRE_IMAGE_FOLDER = Path(current_working_directory) / Path("Target_folder")
    IMAGE_FILENAME = get_single_image_file(CURRENT_TIRE_IMAGE_FOLDER)
    print(IMAGE_FILENAME)
    original_image = Image.open(CURRENT_TIRE_IMAGE_FOLDER / IMAGE_FILENAME)

    resized_image = original_image.resize((300, 165), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=150))

    global image_current_tire
    image_current_tire = ImageTk.PhotoImage(resized_image)

    image_current_tire_3_ID = canvas.create_image(
        150.0,
        122.0,
        image=image_current_tire
    )

    image_fill_star_3_ID = canvas.create_image(
        284.0,
        16.0,
        image=image_fill_star
    )

    # 수명에 따른 출력 구분
    if 0 <= tire_life < 0.3:
        selected_light = image_Red_light
        selected_text = "즉시 교체를\n권장드립니다."
    elif 0.3 <= tire_life < 0.7:
        selected_light = image_Orange_light
        selected_text = "상태가 양호합니다."
    else:
        selected_light = image_Green_light
        selected_text = "상태가 좋습니다!"
    
    image_light_3_ID = canvas.create_image(
        40.0,
        360.0,
        image= selected_light
    )

    canvas.create_text(
        80.0,
        350.0,
        anchor="nw",
        text=f"{selected_text}",
        fill="#000000",
        font=("arial bold", 20 * -1)
    )

    # 수명에 따라 직사각형 바 색칠하기
    # 초기 직사각형 바 생성
    
    progress_bar_background = canvas.create_rectangle(
        30, 
        270, 
        270, 
        280, 
        fill="grey", 
        outline="grey"
    )

    progress_bar = canvas.create_rectangle(
        30, 
        270, 
        30 + int(240 * tire_life), 
        280, 
        fill="blue", 
        outline="blue"
    )

    canvas.create_text(
        40.0,
        240.0,
        anchor="nw",
        text="잔여 타이어 수명 : ",
        fill="#000000",
        font=("arial bold", 20 * -1)
    )

    canvas.create_text(
        210.0,
        240.0,
        anchor="nw",
        text=f"{tire_life}",
        fill="#000000",
        font=("arial bold", 20 * -1)
    )

    window.update()

#초기 캔버스 설정
window = Tk()
window.geometry("300x500")
window.configure(bg="#FFFFFF")
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=500,
    width=300,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

#이미지 파일 설정
button_upload = PhotoImage(file=relative_to_assets("button_upload.png"))
image_car = PhotoImage(file=relative_to_assets("image_car.png"))
image_cloud = PhotoImage(file=relative_to_assets("image_cloud.png"))
image_fill_star = PhotoImage(file=relative_to_assets("image_fill_star.png"))
image_star = PhotoImage(file=relative_to_assets("image_star.png"))
image_sun = PhotoImage(file=relative_to_assets("image_sun.png"))
image_tire = PhotoImage(file=relative_to_assets("image_tire.png"))
image_tree = PhotoImage(file=relative_to_assets("image_tree.png"))

image_Red_light = PhotoImage(file=relative_to_assets("Red.png"))
image_Orange_light = PhotoImage(file=relative_to_assets("Orange.png"))
image_Green_light = PhotoImage(file=relative_to_assets("Green.png"))

#시작(gui 1번째 창)
init()