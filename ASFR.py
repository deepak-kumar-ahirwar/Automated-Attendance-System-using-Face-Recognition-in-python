import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
from tkinter import messagebox

### for all function of main_frame system

def mainframe():
    import tkinter
    win = tk.Tk()
    win.title("Automated Attendance System using Face Recognition")
    win.geometry('1340x720')
    win.attributes('-fullscreen', True)
    win.bind("<Escape>", lambda event: win.attributes("-fullscreen", False))
    bgimage2 = ImageTk.PhotoImage(Image.open("bg.jpg"))
    bglabel = Label(image=bgimage2)
    bglabel.pack()
    w, h = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry("%dx%d+0+0" % (w, h))

    ###for fill subject name for student  attendance using recognition
    def track_attendance():
        def Fillattendances():
            sub = tx.get()
            now = time.time()  ###For calculate seconds of video
            future = now + 20
            if time.time() < future:
                if sub == '':
                    err_screen1()
                else:
                    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
                    try:
                        recognizer.read("Trainingdata\Trainner.yml")
                    except:
                        e = 'Model not found,Please train model'
                        fill_Notification.configure(text=e, bg="red", fg="black", width=33, font=('times', 15, 'bold'))
                        fill_Notification.place(x=20, y=250)
                    harcascadePath = "haarcascade_frontalface_default.xml"
                    faceCascade = cv2.CascadeClassifier(harcascadePath)
                    df = pd.read_csv("StudentDetails\StudentDetails.csv")
                    cam = cv2.VideoCapture(0)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    col_names = ['rollNo', 'Name', 'Date', 'Time']
                    attendance = pd.DataFrame(columns=col_names)
                    while True:
                        ret, im = cam.read()
                        im = cv2.flip(im, +1)
                        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                        for (x, y, w, h) in faces:
                            global Id

                            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                            if (conf < 70):
                                print(conf)
                                global Subject
                                global aa
                                global date
                                global timeStamp
                                Subject = tx.get()
                                ts = time.time()
                                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                                aa = df.loc[df['rollNo'] == Id]['Name'].values
                                global tt
                                tt = str(Id) + "-" + aa
                                En = '15624031' + str(Id)
                                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                                cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

                            else:
                                Id = 'Unknown'
                                tt = str(Id)
                            if(conf > 70):
                                noOfFile = len(os.listdir("UnknownImages")) + 1
                                cv2.imwrite("UnknownImages\Image" + str(noOfFile) + ".jpg", im[y:y + h, x:x + w])
                                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                                cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
                        attendance = attendance.drop_duplicates(['rollNo'], keep='first')
                        cv2.imshow('Filling attedance..', im)
                        key = cv2.waitKey(30) & 0xff
                        if key == 27:
                            break
                    try:
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        Hour, Minute, Second = timeStamp.split(":")
                        fileName = "Attendance/" + Subject + "_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
                        attendance = attendance.drop_duplicates(['rollNo'], keep='first')
                        print(attendance)
                        attendance.to_csv(fileName, index=False)
                        ##Create table for Attendance
                        M = 'Attendance filled Successfully'
                        fill_Notification.configure(text=M, bg="Green", fg="white", width=33, font=('times', 15, 'bold'))
                        fill_Notification.place(x=20, y=250)
                        cam.release()
                        cv2.destroyAllWindows()
                    except:
                        z = 'All students are absent.'
                        fill_Notification.configure(text=z, bg="red", fg="white", width=33, font=('times', 15, 'bold'))
                        fill_Notification.place(x=20, y=250)
                        cv2.destroyAllWindows()

                        ###for track attendance frame
        fill_attendance = tk.Tk()
        fill_attendance.iconbitmap('header.ico')
        fill_attendance.title("Enter subject name...")
        fill_attendance.geometry('580x320')
        fill_attendance.configure(background='black')
        fill_Notification = tk.Label(fill_attendance, text="Attendance filled Successfully", bg="Green", fg="white", width=33,
                            height=2, font=('times', 15, 'bold'))

        sub = tk.Label(fill_attendance, text="Enter Subject", width=15, height=2, fg="white", bg="red", borderwidth=2,
                       relief="raised", font=('times', 15, ' bold '))
        sub.place(x=30, y=100)

        tx = tk.Entry(fill_attendance, width=20, bg="white", fg="red", font=('times', 23, ' bold '))
        tx.place(x=250, y=105)

        fill_button = tk.Button(fill_attendance, text="Fill Attendance", fg="white", command=Fillattendances, borderwidth=2,
                           relief="raised", bg="green", width=20, height=2,
                           activebackground="Red", font=('times', 15, ' bold '))
        fill_button.place(x=250, y=160)
        fill_attendance.bind("<Return>", (lambda event: Fillattendances()))
        fill_attendance.mainloop()

    ### take images for datasets
    def take_img():
        l1 = txt.get()
        l2 = txt2.get()
        if l1 == '':
            err_screen()
        elif l2 == '':
            err_screen()
        else:
            try:
                cam = cv2.VideoCapture(0)
                detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                rollNo = txt.get()
                Name = txt2.get()
                sampleNum = 0
                while (True):
                    ret, img = cam.read()
                    img = cv2.flip(img, +1)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = detector.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        # incrementing sample number
                        sampleNum = sampleNum + 1
                        # saving the captured face in the dataset folder
                        cv2.imwrite("TrainingImage/ " + Name + "." + rollNo + '.' + str(sampleNum) + ".jpg",
                                    gray[y:y + h, x:x + w])
                        cv2.imshow('Frame', img)
                    # wait for 100 miliseconds
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    # break if the sample number is morethan 100
                    elif sampleNum > 100:
                        break
                cam.release()
                cv2.destroyAllWindows()
                ts = time.time()
                Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                row = [rollNo, Name, Date, Time]
                with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                    writer = csv.writer(csvFile, delimiter=',')
                    writer.writerow(row)
                    csvFile.close()
                res = "Images Saved for rollNo : " + rollNo + " Name : " + Name
                Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 15, 'bold'))
                Notification.place(x=500, y=500)
            except FileExistsError as F:
                f = 'Student Data already exists'
                Notification.configure(text=f, bg="Red", width=21)
                Notification.place(x=450, y=400)
    ###For train the image
    def trainimg():
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        global detector
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        try:
            global faces, Id
            faces, Id = getImagesAndLabels("TrainingImage")
        except Exception as e:
            l = 'please make "TrainingImage" folder & put Images'
            Notification.configure(text=l, bg="SpringGreen3", width=40, font=('times', 15, 'bold'))
            Notification.place(x=500, y=500)

        recognizer.train(faces, np.array(Id))
        try:
            recognizer.save("Trainingdata\Trainner.yml")
        except Exception as e:
            q = 'Please make "TrainingImageLabel" folder'
            Notification.configure(text=q, bg="SpringGreen3", width=40, font=('times', 15, 'bold'))
            Notification.place(x=500, y=400)

        res = "Model Trained"  # +",".join(str(f) for f in Id)
        Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 15, 'bold'))
        Notification.place(x=500, y=500)

    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        # create empth face list
        faceSamples = []
        # create empty ID list
        Ids = []
        # now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths:
            # loading the image and converting it to gray scale
            pilImage = Image.open(imagePath).convert('L')
            # Now we are converting the PIL image into numpy array
            imageNp = np.array(pilImage, 'uint8')
            # getting the Id from the image

            Id = int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            faces = detector.detectMultiScale(imageNp)
            # If a face is there then append that in the list as well as Id of it
            for (x, y, w, h) in faces:
                faceSamples.append(imageNp[y:y + h, x:x + w])
                Ids.append(Id)
        return faceSamples, Ids

#### for clear text box ................
    def clear():
        txt.delete(first=0, last=22)

    def clear1():
        txt2.delete(first=0, last=22)

#####  Error screen2
    def del_sc2():
        sc2.destroy()

    def err_screen():
        messagebox.showwarning("Note", "Student Roll No. and Name Required")

    def err_screen1():
        global sc2
        sc2 = tk.Tk()
        sc2.geometry('300x100')
        sc2.iconbitmap('header.ico')
        sc2.title('Warning!!')
        sc2.configure(background='black')
        Label(sc2, text='Please enter your subject name!!!', fg='red', bg='black', font=('times', 16, ' bold ')).pack()
        Button(sc2, text='OK', command=del_sc2, fg="black", bg="lawn green", width=9, height=1, activebackground="Red",
               font=('times', 15, ' bold ')).place(x=90, y=50)

    def about():
        messagebox.showinfo("About", "Application is created by Deepak, Ayushi and Anupam.")

    def check_register_students():
        import csv
        import tkinter
        root = tkinter.Tk()
        root.title("Student Details")
        root.configure(background='snow')
        cs = 'StudentDetails/StudentDetails.csv'
        with open(cs, newline="") as file:
            reader = csv.reader(file)
            r = 0

            for col in reader:
                c = 0
                for row in col:
                    label = tkinter.Label(root, width=12, height=1, fg="black", font=('times', 15, ' bold '),
                                          bg="lawn green", text=row, relief=tkinter.RIDGE)
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        root.mainloop()

    def check_student_attendance():
        import subprocess
        subprocess.call(r'explorer "Attendance')

    def testVal(inStr, acttyp):
        if acttyp == '1':  # insert
            if not inStr.isdigit():
                return False
        return True

    def on_closing():
        from tkinter import messagebox
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            win.destroy()
    win.protocol("WM_DELETE_win", on_closing)

    def c00():
        un_entr.delete(first=0, last=22)

    def c11():
        pw_entr.delete(first=0, last=22)

    ##### interface .................................................

    win.grid_rowconfigure(0, weight=1)
    win.grid_columnconfigure(0, weight=1)
    win.iconbitmap('header.ico')

    message = tk.Label(win, text="Automated Attendance System using Face Recognition", fg="white", bg="black",
                       width=55, height=2, font=('times', 30, ' bold '))

    message.place(x=80, y=20)

    lbl = tk.Label(win, text="Enter Student Roll no.", width=20, height=2, fg="white", bg="black", borderwidth=2,
                   relief="raised", font=('times', 15, ' bold '))
    lbl.place(x=200, y=300)

    txt = tk.Entry(win, validate="key", width=20, bg="white", fg="red", font=('times', 25, ' bold '))
    txt.place(x=550, y=300)

    txt['validatecommand'] = (txt.register(testVal), '%P', '%d')
    txt.place(x=550, y=300)

    lbl2 = tk.Label(win, text="Enter Student Name", width=20, fg="white", bg="black", height=2, borderwidth=2,
                    relief="raised", font=('times', 15, ' bold '))
    lbl2.place(x=200, y=400)

    txt2 = tk.Entry(win, width=20, bg="white", fg="red", font=('times', 25, ' bold '))
    txt2.place(x=550, y=400)

    lbl3 = tk.Label(win, text="Notification", width=20, fg="white", bg="black", height=2, borderwidth=2,
                    relief="raised", font=('times', 15, ' bold '))
    lbl3.place(x=200, y=500)

    Notification = tk.Label(win, text="All things good", bg="Green", fg="white", width=15,
                            height=3, font=('times', 17, 'bold'))

    clearButton = tk.Button(win, text="Clear", command=clear, fg="white", bg="black", width=10, height=1,
                            activebackground="Red", font=('times', 15, ' bold '))
    clearButton.place(x=950, y=300)

    clearButton1 = tk.Button(win, text="Clear", command=clear1, fg="white", bg="black", width=10, height=1,
                             activebackground="Red", font=('times', 15, ' bold '))
    clearButton1.place(x=950, y=400)

    check_registerstudent_button = tk.Button(win, text="Check Register students", command=check_register_students, fg="white", bg="black", width=19,
                   height=2, activebackground="Red", font=('times', 15, ' bold '))
    check_registerstudent_button.place(x=1150, y=500)

    take_Img = tk.Button(win, text="Take Images", command=take_img, fg="white", bg="black", borderwidth=2,
                        relief="raised", width=20, height=3, activebackground="Red", font=('times', 15, ' bold '))
    take_Img.place(x=90, y=600)

    train_Img = tk.Button(win, text="Train Images", command=trainimg, fg="white", bg="black", width=20, height=3,
                         activebackground="Red", font=('times', 15, ' bold '))
    train_Img.place(x=450, y=600)

    fill_attendance = tk.Button(win, text="Fill Attendance", command=track_attendance, fg="white", bg="black", width=20, height=3,
                   activebackground="Red", font=('times', 15, ' bold '))
    fill_attendance.place(x=800, y=600)

    check_attendance = tk.Button(win, text="Check student attendance", command=check_student_attendance, fg="white", bg="black",
                           width=20, height=3, activebackground="Red", font=('times', 15, ' bold '))
    check_attendance.place(x=1150, y=600)

    about = tk.Button(win, text="About", fg="white", bg="black", width=9, relief="raised",
                      height=2, activebackground="Red", command=about, font=('times', 20, ' bold '))
    about.place(x=1330, y=80)
    def logoutbtn():
        win.destroy()
    logoutbtn = tk.Button(win, text="Exit", fg="white", bg="black", width=9, relief="raised",
                        height=1, activebackground="Red", command=logoutbtn, font=('times', 20, ' bold '))
    logoutbtn.place(x=50, y=100)
    win.mainloop()
#####win is our Main frame of system
win = tk.Tk()
win.geometry('1340x720')
win.iconbitmap('header.ico')
win.title("Login ")
win.attributes('-fullscreen', True)
win.bind("<Escape>", lambda event: win.attributes("-fullscreen", False))
#win.attributes("-toolwin", 1)
w, h = win.winfo_screenwidth(), win.winfo_screenheight()
win.geometry("%dx%d+0+0" % (w, h))
bgimage = ImageTk.PhotoImage(Image.open("bg.jpg"))
bglabel = Label(image=bgimage)
bglabel.pack()


def err_login():
    messagebox.showwarning("Login failed", "Username and Password required")
def log_in():
    username = un_entr.get()
    password = pw_entr.get()
    l1 = username
    l2 = password
    if( l1 =='' and l2 == '' ):
        err_login()
    else:
        if username == 'deepak':
            if password == 'deepak':
                win.destroy()
                mainframe()
            else:
                messagebox.showwarning("Login failed", "Wrong Password")

        else:
            messagebox.showwarning("Login failed", "Wrong Username")


def exitbtn():
    exit()

un = tk.Label(win, text="Enter username", width=15, height=2, fg="white", bg="black",
              font=('times', 20, ' bold '))
un.place(x=400, y=300)

un_entr = tk.Entry(win, width=25, bg="white", fg="red", font=('times', 23, ' bold '))
un_entr.place(x=700, y=320)

pw = tk.Label(win, text="Enter password", width=15, height=2, fg="white", bg="black",
              font=('times', 20, ' bold '))
pw.place(x=400, y=400)

pw_entr = tk.Entry(win, width=25, show="*", bg="white", fg="red", font=('times', 23, ' bold '))
pw_entr.place(x=700, y=420)

Login = tk.Button(win, text="LogIn", fg="white", bg="green", width=10,relief="raised",
                  height=2, activebackground="Red", command=log_in, font=('times', 20, ' bold '))
Login.place(x=660, y=530)

message = tk.Label(win, text="Automated Attendance System using Face Recognition", fg="white", bg="black",
                       width=55, height=2, font=('times', 30, ' bold '))
message.place(x=80, y=50)
exitbtn = tk.Button(win, text="Exit", fg="white", bg="black", width=9, relief="raised",
                        height=1, activebackground="Red", command=exitbtn, font=('times', 20, ' bold '))
exitbtn.place(x=1300, y=100)

img = ImageTk.PhotoImage(Image.open("face.png"))
panel = Label(win, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")

win.bind("<Return>", (lambda event: log_in()))

win.mainloop()

