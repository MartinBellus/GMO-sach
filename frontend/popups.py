import tkinter
from utility.exceptions import NetworkException, RemoteFileNotFound

class InputPopup(tkinter.Toplevel):
    def __init__(self,title : str,text : str, callback, **args):
        super().__init__(**args)
        super().title(title)
        super().resizable(False,False)
        self.callback = callback
        main_text = tkinter.Label(self,text=text,font=("Consolas",15),wraplength=400,justify="left",anchor="w")

        self.entry = tkinter.Entry(self,font=("Consolas",12))

        bottom_frame = tkinter.Frame(self)
        self.status = tkinter.Label(bottom_frame,font=("Consolas",13),justify="left",anchor="w")
        submit_button = tkinter.Button(bottom_frame,text="Submit",font=("Consolas",12),command=self.press)

        main_text.pack(anchor="w",fill="x",expand=True,pady=20,padx=15)
        bottom_frame.pack(side="bottom",fill="both",expand=True,padx=15)
        self.entry.pack(fill="x",expand=True,padx=15)
        self.status.pack(side="left",anchor="w",fill="x")
        submit_button.pack(anchor="e",pady=5)

    def press(self):
        try:
            self.status.config(text="Loading...",fg="Blue")
            self.callback(self.entry.get())
            self.status.config(text="Successful",fg="Green")
            print("fung")
        except NetworkException:
            self.status.config(text="Server can not be reached",fg="Red")
        
        except RemoteFileNotFound:
            self.status.config(text="Invalid key",fg="Red")

        except Exception as ex:
            self.status.config(text=ex,fg="Red")

class TextPopup(tkinter.Toplevel):
    def __init__(self,title : str, *args,**kwargs):
        super().__init__(**kwargs)
        super().title(title)
        super().resizable(False,False)
        for text in args:
            main_text = tkinter.Label(self,text=text,font=("Consolas",15),wraplength=400,justify="left",anchor="w")
            main_text.pack(anchor="w",fill="x",expand=True,pady=20,padx=15)