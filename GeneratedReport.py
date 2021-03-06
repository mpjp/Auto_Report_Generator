import tkinter as TK 
import writeFile

from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import messagebox


total = ""
test_cases = []

def guiGenerated():
    window = TK.Tk()
    window.title("Auto Report Generator")
    window.geometry('350x250')

    lbl = Label(window, text="Enter the test case number: ")
    lbl.grid(column=0, row=0)
    txt = Entry(window,width=10)
    txt.grid(column=1, row=0)

    test_case_lable = Label(window, text="")
    test_case_lable.grid(column=0,row=1)

    def addClicked():    
        global total
        global test_cases
        test_cases.append(txt.get())
        total = total + txt.get() + "\n"
        test_case_lable.config(text = "total size:%s" %len(test_cases) + "\n" + total)
        txt.delete(0, 'end')
        
    btn = Button(window, text="Add", command=addClicked)
    btn.grid(column=2, row=0)

    def okclicked():
        global test_cases
        print(*test_cases)
        test_cases.sort()
        test_cases.sort(key=int)
        try:
            writeFile.read_data(test_cases)
            messagebox.showinfo("DONE", "DONE. The csv file is in the folder.")
        except Exception as e:
            messagebox.showerror("ERROR", e)
    
    Okbtn = Button(window, text="Ok", command=okclicked, bg='yellow')
    Okbtn.grid(column=10, row=0)

    def cleanClicked():
        global test_cases
        global total
        total = ''
        del test_cases[:]
        test_case_lable.config(text = "")

    CleanBtn = Button(window, text= 'cleanAll', command = cleanClicked, bg= 'pink' )
    CleanBtn.grid(column=15, row= 0)
    
    window.mainloop()

def main():
    guiGenerated()

if __name__ == '__main__':     
      main()