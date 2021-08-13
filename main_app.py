from tkinter import *
from tkinter import messagebox as mb
from datetime import datetime
import threading

def new_window_f(name):
    '''
    new window with two actions to do
    '''
    def fast_delete(name):
        '''
        delete current incident after 'Close' pressed:
            getting everything from listbox
            find 'name' in it, delete it
            clear listbox
            return everthing back w/o 'name'
        '''        
        content = incidents_list.get(0,END)
        content = tuple(incident for incident in content if incident != name)

        incidents_list.delete(0,END)
        for incident in content:
            incidents_list.insert(END, incident)        
    
        new_window.destroy()
        new_window.update()
        
    def fast_timer(name):
        '''
        creating timer after 'Hold' pressed
        '''        
        threading.Timer(3, new_window_f, args=[name,]).start()
        new_window.destroy()   
        new_window.update()
    
    new_window      = Toplevel()
    new_window.geometry('200x180')
    
    new_window_text = Label( new_window, text=f"\n{name} is still active. \n\n Close Incident or Hold it?\n\n")
    close           = Button(new_window, text='(c)Close',command=lambda: fast_delete(name))
    hold            = Button(new_window, text='(h)Hold' ,command=lambda: fast_timer(name))
    
    new_window_text.pack()    
    close.          pack(fill=X)
    hold.           pack(fill=X)
    
    new_window.bind('<Alt_L><c>', lambda event: fast_delete)
    new_window.bind('<Alt_L><h>', lambda event: fast_timer(name))
    
def shit_timer(name,warning):
    '''
     - starts timer after 'Add incident' pressed,
     - calling new_window_f() for all warnings except first one
    '''        
    if name in incidents_list.get(0,END):
        if warning:
            new_window_f(name)
        else:
            warning = True
            threading.Timer(3, shit_timer, args=[name,warning]).start()
 
def add_incident():
    '''
    adding new incident, starting a timer w/o first warning
    '''        
    hour          = datetime.now().hour
    minute        = datetime.now().minute
    incident_name = entry.get()
    incident_time = f'{hour:02d}:{minute:02d}'
    entry_text    = f' Incident name: {incident_name} \n Incident time: {incident_time}'
    
    incidents_list. insert(END, entry_text)
    entry.          delete(0, END)
    
    warning = False
    shit_timer(entry_text,warning)
 
 
def del_incident():
    '''
    deleting selected incident(s)
    '''    
    select = list(incidents_list.curselection())
    select.reverse()
    for i in select:
        incidents_list.delete(i)
        
def save_incident():
    '''
    saving all incidents to Incidents_list.txt file
    '''
    hour      = datetime.now().hour
    minute    = datetime.now().minute
    sv_string = datetime.today() 
    f  = open(f'{datetime.date()}_Incidents_list.txt', 'w')
    f. writelines(f'{sv_string:%B %d, %Y}   {hour:02d}:{minute:02d}\n\n')
    f. writelines("\n".join(incidents_list.get(0, END)))
    f. close()

''' 
shitty design 
'''
root = Tk()
 
incidents_list         = Listbox(selectmode=EXTENDED,width=60)
incidents_list_scroll  = Scrollbar(command=incidents_list.yview)
incidents_list.          config(yscrollcommand=incidents_list_scroll.set)

window_frame           = Frame()
entry                  = Entry(window_frame)

incidents_list.        pack(side=LEFT)
incidents_list_scroll. pack(side=LEFT, fill=Y)
window_frame.          pack(side=LEFT, padx=10)
entry.                 pack(anchor=N)

'''
buttons for actions
'''
Button(window_frame, text="(a)Add Incident", command=add_incident)\
    .pack(fill=X)
Button(window_frame, text="(d)Delete Incident", command=del_incident)\
    .pack(fill=X)
Button(window_frame, text="(s)Save Incidents", command=save_incident)\
    .pack(fill=X)
Button(window_frame, text="(x)Exit", command=root.destroy)\
    .pack(fill=X)

'''
bind a key to each button from above.
'''
root.bind('<Alt_L><a>', lambda event: add_incident())
root.bind('<Alt_L><d>', lambda event: del_incident())
root.bind('<Alt_L><s>', lambda event: save_incident())
root.bind('<Alt_L><x>', lambda event: root.destroy())

root.mainloop()
