from tkinter import *
import mysql.connector

window = Tk()
window.geometry('600x700+10+10')
window.title('Operating Room Staff Perceptions of Surgical Smoke')
or_room_num_label = Label(window, text='OR Room Number:')
or_room_num_label.place(x=5, y=10)
or_room_num = Entry(window)
or_room_num.place(x=140, y=5)
role_label = Label(window, text='Role in Operating Room:')
role_label.place(x=5, y=40)
roles = ['Surgeon', 'Anesthesiologist', 'CRNA', 'PeriOp RN', 'Surg Tech', 'Radiology']
roles_list_box = Listbox(window, height=6, selectmode='multiple', exportselection=0)
for role in roles:
    roles_list_box.insert(END, role)
roles_list_box.place(x=5, y=60)
gender_label = Label(window, text='Gender:\n')
gender_label.place(x=5, y=170)
gender = StringVar()
gender.set('Male')
g1 = Radiobutton(window, text="Male", variable=gender, value='Male')
g2 = Radiobutton(window, text="Female", variable=gender, value='Female')
g1.place(x=5, y=200)
g2.place(x=100, y=200)
smoke_label = Label(window, text='Was surgical smoke generated during this case?\n')
smoke_label.place(x=5, y=230)
smoke = StringVar()
s1 = Radiobutton(window, text="Yes", variable=smoke, value='Yes')
s2 = Radiobutton(window, text="No", variable=smoke, value='No')
s1.place(x=5, y=260)
s2.place(x=100, y=260)
notice_label = Label(window, text='How did you notice the surgical smoke?\n')
notice_label.place(x=5, y=290)
notice_list_box = Listbox(window, height=2, selectmode='multiple', exportselection=0)
notice_options = ['Saw it', 'Smelled it']
for option in notice_options:
    notice_list_box.insert(END, option)
notice_list_box.place(x=5, y=320)
evac_label = Label(window, text='Was smoke evacuation used?\n')
evac_label.place(x=5, y=370)
evac = StringVar()
e1 = Radiobutton(window, text="Yes", variable=evac, value='Yes')
e2 = Radiobutton(window, text="No", variable=evac, value='No')
e1.place(x=5, y=400)
e2.place(x=100, y=400)
type_label = Label(window, text='What type of evacuation was used?\n')
type_label.place(x=5, y=430)
type_list_box = Listbox(window, height=5, width=40, selectmode='multiple', exportselection=0)
type_options = ['Hand-held suction to Neptune Suction', 'Handheld-suction to Wall',
                'Hand-held integrated hand-piece Smoke Evacuator', 'Other', 'None']
for option in type_options:
    type_list_box.insert(END, option)
type_list_box.place(x=5, y=470)
cause_label = Label(window, text='Did the smoke cause:\n')
cause_label.place(x=5, y=560)
cause_list_box = Listbox(window, height=3, selectmode='multiple', exportselection=0)
cause_options = ['An obstructed field of view', 'An odor', 'Other']
for option in cause_options:
    cause_list_box.insert(END, option)
cause_list_box.place(x=5, y=590)


def submit():
    conn = mysql.connector.connect(
        host='localhost', database='or_db', user='USERNAME', password='PASSWORD'
    )
    cursor = conn.cursor()
    role_list = [roles_list_box.get(x) for x in roles_list_box.curselection()]
    notice_list = [notice_list_box.get(x) for x in notice_list_box.curselection()]
    type_list = [type_list_box.get(x) for x in type_list_box.curselection()]
    cause_list = [cause_list_box.get(x) for x in cause_list_box.curselection()]
    sql = '''
        INSERT INTO data_input (or_num, role, gender, smoke, notice, evac, type_used, smoke_caused)VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s)'''

    cursor.execute(sql, (
        or_room_num.get(), ', '.join(role_list), gender.get(), smoke.get(), ', '.join(notice_list), evac.get(),
        ', '.join(type_list), ', '.join(cause_list)))
    conn.commit()

    conn.close()
    or_room_num.delete(0, 'end')
    roles_list_box.selection_clear(0, 'end')
    notice_list_box.selection_clear(0, 'end')
    type_list_box.selection_clear(0, 'end')
    cause_list_box.selection_clear(0, 'end')
    print(cursor.rowcount, 'Record Inserted')


submit_button = Button(window, text='Submit', command=submit)
submit_button.place(x=400, y=650)

window.mainloop()
