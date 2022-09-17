from tkinter import *
import datetime
import tkcalendar
from tkinter import messagebox
from tkinter.messagebox import askyesno
import re
import json
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def main():
    global window
    window = Tk()
    window.title("Workout Tracker")
    window.geometry("640x360")
    main_menu()


def main_menu():

    for widget in window.winfo_children():
        widget.destroy()
    lv_btn = Button(window, text="Log/View Workout", command=choose_date)
    lv_btn.grid(column=0, row=0)
    lv_btn.place(relx=0.5, rely=0.4, anchor=CENTER)
    prog_btn = Button(window, text="View Progress", command=view_progress)
    prog_btn.grid(column=0, row=1)
    prog_btn.place(relx=0.5, rely=0.5, anchor=CENTER)
    settings_btn = Button(window, text="Settings", command=settings)
    settings_btn.grid(column=0, row=2)
    settings_btn.place(relx=0.5, rely=0.6, anchor=CENTER)
    window.mainloop()

def settings():

    for widget in window.winfo_children():
        widget.destroy()

    def clear():
        verify = askyesno(title="Clear All Logs", message="Are you sure you want to clear all logs?")
        if verify:
            with open("logs.json", "w") as file:
                logs = {}
                json.dump(logs, file)

    clear_btn = Button(window, text="Clear All Logs", command=clear)
    clear_btn.grid(column=0, row=0)
    menu_btn = Button(window, text="Main Menu", command=main_menu)
    menu_btn.grid(column=0, row=1)
    window.mainloop()


def choose_date():
    for widget in window.winfo_children():
        widget.destroy()
    global choose_dt
    choose_dt = tkcalendar.Calendar(
        master=None, font="Arial 25", date_pattern="MM/dd/yyyy"
    )
    choose_dt.grid(column=0, row=0, rowspan=3)
    add_btn = Button(window, text="Add Log", command=add_log)
    add_btn.grid(column=1, row=0)
    view_btn = Button(window, text="View Log", command=view_log)
    view_btn.grid(column=1, row=1)
    menu_btn = Button(window, text="Main Menu", command=main_menu)
    menu_btn.grid(column=1, row=2)
    window.mainloop()


def add_log():
    date = choose_dt.get_date()
    with open("logs.json", "r") as file:
        logs = json.load(file)
        if date in [key for key in logs]:
            messagebox.showerror(
                title="Error",
                message="You have already logged a workout for this date.",
            )
            file.close()
            choose_date()
        file.close()

    log = {}
    for widget in window.winfo_children():
        widget.destroy()
    with open("exercises.txt", "r") as file:
        exercises = file.read().splitlines()
    choice = StringVar(window)
    choice.set("Please choose an exercise")
    choices = OptionMenu(window, choice, *exercises)
    choices.config(width=17)
    choices.grid(column=0, row=0, columnspan=2)
    sets = Label(window, text="Sets")
    sets.grid(column=0, row=1)
    set_entry = Entry(window, width=5)
    set_entry.grid(column=1, row=1)
    reps = Label(window, text="Reps per Set")
    reps.grid(column=0, row=2)
    rep_entry = Entry(window, width=5)
    rep_entry.grid(column=1, row=2)
    weight = Label(window, text="Weight (KG)")
    weight.grid(column=0, row=3)
    weight_entry = Entry(window, width=5)
    weight_entry.grid(column=1, row=3)
    exercise_list = Text(window, width=54, height=27, wrap=WORD, background="white")
    exercise_list.grid(column=2, row=0, rowspan=10)
    exercise_list.insert(END, date)
    exercise_list.config(state="disabled")

    def add_exercise():

        if choice.get() in ["", "Please choose an exercise", "NECK", "CHEST", "SHOULDERS", "TRICEPS", "BICEPS", "FOREARMS", "BACK", "ABS", "LEGS (Weighted)", "LEGS (Non-Weighted)", "CALVES"]:
            messagebox.showerror(title="Error", message="Please choose an exercise.")
        elif not (
            re.search("^[0-9]+$", set_entry.get())
            and re.search("^[0-9]+$", rep_entry.get())
            and re.search("^[0-9]+\.*[0-9]*$", weight_entry.get())
        ):
            messagebox.showerror(
                title="Error",
                message="Please enter numeric values for weight, sets and reps.",
            )
        else:
            log[choice.get()] = {
                "sets": set_entry.get(),
                "reps": rep_entry.get(),
                "weight": weight_entry.get(),
            }
            print(log)
            workout = f"{date}\n"
            for exercise in log:
                workout += f"{exercise} | {log[exercise]['sets']}x{log[exercise]['reps']} {log[exercise]['weight']}KG\n"
            exercise_list.config(state="normal")
            exercise_list.delete(0.0, END)
            exercise_list.insert(END, workout)
            exercise_list.config(state="disabled")

        choice.set("Please choose an exercise")
        set_entry.delete(0, END)
        rep_entry.delete(0, END)
        weight_entry.delete(0, END)

    def rmv_exercise():

        if choice.get() in ["", "Please choose an exercise", "NECK", "CHEST", "SHOULDERS", "TRICEPS", "BICEPS", "FOREARMS", "BACK", "ABS", "LEGS (Weighted)", "LEGS (Non-Weighted)", "CALVES"]:
            messagebox.showerror(title="Error", message="Please choose an exercise.")
        elif choice.get() not in [exercise for exercise in log]:
            messagebox.showerror(
                title="Error",
                message="Please choose an exercise you have already added.",
            )

        else:
            del log[choice.get()]
            print(log)
            workout = f"{date}\n"
            for exercise in log:
                workout += f"{exercise} | {log[exercise]['sets']}x{log[exercise]['reps']} {log[exercise]['weight']}KG\n"
            exercise_list.config(state="normal")
            exercise_list.delete(0.0, END)
            exercise_list.insert(END, workout)
            exercise_list.config(state="disabled")

        choice.set("Please choose an exercise")
        set_entry.delete(0, END)
        rep_entry.delete(0, END)
        weight_entry.delete(0, END)

    def done():

        if len(log) == 0:
            messagebox.showerror(
                title="Error",
                message="Please add at least one exercise to log a workout.",
            )
        else:

            with open("logs.json", "w") as file:
                logs[date] = log
                json.dump(logs, file, indent=4)
                file.close()
                choose_date()

    add_btn = Button(window, text="Add Exercise", command=add_exercise)
    add_btn.grid(column=0, row=4)

    rmv_btn = Button(window, text="Remove Exercise", command=rmv_exercise)
    rmv_btn.grid(column=0, row=5)

    cancel_btn = Button(window, text="Cancel", command=main_menu)
    cancel_btn.grid(column=0, row=6)

    done_btn = Button(window, text="Done", command=done)
    done_btn.grid(column=0, row=7)

    window.mainloop()


def view_log():
    date = choose_dt.get_date()
    for widget in window.winfo_children():
        widget.destroy()
    workout = f"{date}\n"

    exercise_list = Text(window, width=54, height=27, wrap=WORD, background="white")
    exercise_list.grid(column=0, row=0)

    disable_delete = False

    with open("logs.json", "r") as file:

        logs = json.load(file)
        if len(logs) == 0 or date not in [key for key in logs]:
            exercise_list.delete(0.0, END)
            exercise_list.insert(END, f"No workout logged for {date}")
            exercise_list.config(state="disabled")
            disable_delete = True
        else:
            for exercise in logs[date]:
                workout += f"{exercise} | {logs[date][exercise]['sets']}x{logs[date][exercise]['reps']} {logs[date][exercise]['weight']}KG\n"
            exercise_list.delete(0.0, END)
            exercise_list.insert(END, workout)
            exercise_list.config(state="disabled")

    def delete_log():
        with open("logs.json", "r") as file:
            logs = json.load(file)
        with open("logs.json", "w") as file:
            del logs[date]
            if len(logs) == 0:
                logs = {}
            json.dump(logs, file, indent=4)
            file.close()
            choose_date()

    done_btn = Button(window, text="Done", command=choose_date)
    done_btn.grid(column=1, row=0)
    delete_btn = Button(window, text="Delete Log", command=delete_log)
    delete_btn.grid(column=2, row=0)

    if disable_delete:
        delete_btn.config(state="disabled")

    window.mainloop()


def view_progress():

    for widget in window.winfo_children():
        widget.destroy()
    with open("exercises.txt", "r") as file:
        exercises = file.read().splitlines()
    choice = StringVar(window)
    choice.set("Please choose an exercise")
    choices = OptionMenu(window, choice, *exercises)
    choices.config(width=17)
    choices.grid(column=0, row=0)

    

    def graph():
        fig = Figure(figsize=(6.5, 5), dpi=70)
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().grid(column=1, row=0, rowspan=3)
        graph = fig.add_subplot()

        dates = []
        weight = []
        with open("logs.json", "r") as file:
            logs = json.load(file)
            for date in logs:
                if choice.get() in [exercise for exercise in logs[date]]:
                    dates.append(date)
            dates = sorted(dates)
            print(dates)
            for date in dates:
                weight.append(float(logs[date][choice.get()]["weight"]))
        if choice.get() in ["", "Please choose an exercise", "NECK", "CHEST", "SHOULDERS", "TRICEPS", "BICEPS", "FOREARMS", "BACK", "ABS", "LEGS (Weighted)", "LEGS (Non-Weighted)", "CALVES"]:
            messagebox.showerror(title="Error", message="Please choose an exercise.")
            choice.set("Please choose an exercise")

        elif len(dates) == 0:
            messagebox.showerror(
                title="Error", message="No workouts logged with this exercise."
            )
        else:
            graph.plot(dates, weight)

            graph.set_ylabel("Weight (KG)")
            graph.set_xlabel("Date")

            fig.autofmt_xdate(rotation=45)

            graph.set_title(label=choice.get())

            canvas.draw()

    chart_btn = Button(window, text="View Progress", command=graph)
    chart_btn.grid(column=0, row=1)
    menu_btn = Button(window, text="Main Menu", command=main_menu)
    menu_btn.grid(column=0, row=2)


if __name__ == "__main__":
    main()
