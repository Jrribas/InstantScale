import tkinter as tk

root = tk.Tk()

drag_id = ''


def dragging(event):
    global drag_id
    if event.widget is root:  # do nothing if the event is triggered by one of root's children
        if drag_id == '':
            # action on drag start
            print('start drag')
        else:
            # cancel scheduled call to stop_drag
            root.after_cancel(drag_id)
            print('dragging')
        # schedule stop_drag
        drag_id = root.after(100, stop_drag)


def stop_drag():
    global drag_id
    print('stop drag')
    # reset drag_id to be able to detect the start of next dragging
    drag_id = ''


root.bind('<Configure>', dragging)
root.mainloop()