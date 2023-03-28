import mouse
import re
from datetime import datetime
import os
import tkinter
from tkinter import messagebox

path = 'events.txt'

mouse_events = []

top = tkinter.Tk()
top.title("Automação - Script")
top.geometry("320x128")


def add_callback():
    if not os.path.isfile(path) == True:
        events = mouse.record()

        with open(path, 'a') as file_object:
            file_object.write(str(events))

        messagebox.showinfo(
            "Informação", "Eventos gravados com sucesso, clique no botão para executá-los")
    else:
        with open(path, 'r') as file_object:
            file_value = file_object.read()
            file_result: list[str] = re.findall('\w+?\(.*?\)', file_value)

            for result in file_result:
                event = re.search("\w+", result).group(0)
                values = re.search(
                    '\(.*?\)', result).group(0).strip("()").split(", ")

                if event == "MoveEvent":
                    arg1 = int(values[0].split("=")[1])
                    arg2 = int(values[1].split("=")[1])
                    arg3 = datetime.fromtimestamp(
                        float(values[2].split("=")[1])).timestamp()

                    mouse_events.append(mouse.MoveEvent(arg1, arg2, arg3))
                elif event == "ButtonEvent":
                    arg1 = values[0].split("=")[1].strip("'")
                    arg2 = values[1].split("=")[1].strip("'")
                    arg3 = datetime.fromtimestamp(
                        float(values[2].split("=")[1])).timestamp()

                    mouse_events.append(mouse.ButtonEvent(arg1, arg2, arg3))
        mouse.play(mouse_events)


def delete_callback():
    if os.path.isfile(path) == True:
        os.remove(path)

        messagebox.showinfo("Informação", "Script excluído com sucesso!")
    else:
        messagebox.showinfo("Informação", "Ainda não existe nenhum script")


add_button = tkinter.Button(
    top, text="Criar / Executar script", command=add_callback, width=25, height=2)

delete_button = tkinter.Button(
    top, text="Excluir script", command=delete_callback, width=25, height=2)

add_button.pack()
add_button.place(x=67.5, y=17.5)
delete_button.pack()
delete_button.place(x=67.5, y=67.5)
top.mainloop()
