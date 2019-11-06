# simple gui for using the ETDataClient.

from tkinter import *
from tkinter.ttk import *
from functions import metrics, savers, plotters


window = Tk()
window.title("Tfrrs Wrangler")
window.geometry('800x500')


# automatically generate check boxes for all savers
should_run_saver = []
for i, saver in enumerate(savers):
    chk_state = BooleanVar()
    chk_state.set(False)  # set check state
    chk = Checkbutton(window, text=saver.__name__, var=chk_state)
    chk.grid(column=0, row=i+1)
    should_run_saver.append((saver, chk_state))

# field for path
folder_path_label = Label(window, text="Enter path to export folder here")
folder_path_label.grid(column=0, row=4)
folder_path_txt = Entry(window, width=50, )
folder_path_txt.grid(column=1, row=4)
folder_path_txt.insert(END, '/Users/hudsonthomas/Desktop/Tffrs_data/recent_results')


# callback for when the button gets clicked
def run_savers():

    # get list of checked metrics
    for saver, checked in should_run_saver:
        if checked.get():
            saver(output_folder=folder_path_txt.get())


# make button
btn = Button(window, text='Save selected data', command=run_savers)
btn.grid(column=0, row=7)


#run
window.mainloop()
