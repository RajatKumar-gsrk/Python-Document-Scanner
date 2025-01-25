import tkinter

def main():
    root = tkinter.Tk()
    root.geometry("480x640")
    root.title("DocumentScanner by RajatKumar-gsrk")
    root.iconbitmap("./contract.ico")
    lbl_head = tkinter.Label(text="DocumentScanner", fg = "white", bg = "gray", width = 100, font=("Futura", 30))
    lbl_head.pack()




    root.mainloop()

if __name__ == "__main__":
    main()