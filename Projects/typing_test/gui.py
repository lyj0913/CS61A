from tkinter import *
import time
from typing_test import *
from utils import *
import threading
import string
import csv

words_list = sorted(lines_from_file('data/words.txt'))

class proj2gui(Frame):
    "Frame containing proj2 stuff in the window"
    TIME = 30
    path = './data/sample_paragraphs.txt'
    num_paragraphs = 5474
    def __init__(self, parent):
        super().__init__(parent, borderwidth = 1, bg = '#B8B8B8')
        self.parent = parent #initialize root window as parent to gui frame
        self.pack(fill=BOTH, expand = True)

        #setting up updating labels for data(ex. wpm)
        self.autocorrect = IntVar()
        self.pig_latin = IntVar()
        self.wpm_var = StringVar()
        self.accuracy = StringVar()
        self.time = StringVar()

        #initializing default values for labels
        self.autocorrect.set(0)
        self.pig_latin.set(0)
        self.wpm_var.set('0')
        self.accuracy.set('0')
        self.time.set('60')

        #setting up additional useful utilities
        self.is_running = False
        self.translator = str.maketrans('', '', string.punctuation)

        #subdividing gui frame into 3 sections of reference, typing, and options
        self.ref = Frame(self, height = 250, width = 400, borderwidth = 2, bg = 'black')
        self.ref.grid(row = 0, column = 0)
        self.text = Frame(self, height = 250, width = 400, borderwidth = 1, bg = '#B8B8B8')
        self.text.grid(row = 1, column = 0)
        self.options = Frame(self, height = 500, width =200, borderwidth = 1, bg = '#B8B8B8')
        self.options.grid(row = 0, column = 1, rowspan = 2)

        #initial setting up all the sub-frames
        self.init_ref()
        self.init_text()
        self.init_options()

    def init_ref(self):
        #not allowing frame to resize to the reference text box
        self.ref.pack_propagate(False)

        #setting up the initial reference text variables
        self.row = 0
        self.reference_text = StringVar()
        self.backup = StringVar()
        self.reference_text.set(new_sample(self.path, self.row))
        self.backup.set(self.reference_text.get())

        #setting up the label using the variables
        a = Label(self.ref, textvariable = self.reference_text, wraplength = 400)

        #make the frame appear
        a.pack(fill = BOTH, expand = YES)

    def init_text(self):
        #not allowing frame to resize to the size of the textbox
        self.text.pack_propagate(False)

        #initializing the textbox and packing it to the frame
        self.textbox = Text(self.text, height = 15, width = 56)
        self.textbox.pack(side = 'bottom')


    def init_options(self):

        #inital storage/frame setup
        self.option_buttons = []
        self.options.pack_propagate(False)

        #dividing the frame into wpm/checkboxes
        self.wpm_frame = Frame(self.options, bg = '#B8B8B8')
        self.wpm_frame.pack(fill = BOTH, expand = YES)
        self.check_frame = Frame(self.options, bg = '#B8B8B8')
        self.check_frame.pack(side = 'bottom')

        #filling the checkboxes with two checkbox button frames 
        self.pig_frame= Frame(self.check_frame, bg = '#B8B8B8')
        self.pig_frame.pack(side = 'bottom', fill = BOTH)
        self.auto_frame= Frame(self.check_frame, bg = '#B8B8B8')
        self.auto_frame.pack(side = 'bottom', fill = BOTH)

        #filling the checkbox button frames with the respective checkbox buttons
        self.option_buttons.append(Checkbutton(self.auto_frame, text = 'Autocorrect', variable = self.autocorrect, command = self.enable_autocorrect, bg = '#B8B8B8'))
        self.option_buttons[0].pack(side = 'left')
        self.option_buttons.append(Checkbutton(self.pig_frame, text = 'Pig Latin', variable = self.pig_latin, command = self.enable_piglatin, bg = '#B8B8B8'))
        self.option_buttons[1].pack(side = 'left')

        #Setting up WPM Heading
        self.wpm = Label(self.wpm_frame, text= 'WPM', bg = '#B8B8B8')
        self.wpm.config(font =('Courier', 36))
        self.wpm.pack(side = 'top')
        self.counter = Label(self.wpm_frame, textvariable = self.wpm_var,  bg = '#B8B8B8')
        self.counter.config(font = ('Courier', 30))
        self.counter.pack(side = 'top')

        #Setting up Accuracy
        self.acc = Label(self.wpm_frame, text = 'Accuracy', bg = '#B8B8B8')
        self.acc.config(font =('Courier', 36))
        self.acc.pack(side = 'top')
        self.acc_counter = Label(self.wpm_frame, textvariable = self.accuracy, bg = '#B8B8B8')
        self.acc_counter.config(font = ('Courier', 30))
        self.acc_counter.pack(side = 'top')

        #Adding a Timer
        self.timer = Label(self.wpm_frame, text = 'Time Left', bg = '#B8B8B8')
        self.timer.config(font = ('Courier', 36))
        self.timer.pack(side = 'top')
        self.time_left = Label(self.wpm_frame, textvariable = self.time, bg = '#B8B8B8')
        self.time_left.config(font = ('Courier', 30))
        self.time_left.pack(side = 'top')

        #Adding a Start Button
        self.option_buttons.append(Button(self.wpm_frame, text = 'Start', command = self.thread, bg = '#B8B8B8', fg = '#B8B8B8'))
        self.option_buttons[2].pack()

        #Adding a stop Button
        self.option_buttons.append(Button(self.wpm_frame, text = 'Save', command = self.stop, bg = '#B8B8B8', fg = '#B8B8B8'))
        self.option_buttons[3].pack()

    def get_input(self):
        self.is_running = True
        start, end = time.time(), time.time() + 60
        num = 0
        if self.autocorrect.get() == 1:
            while time.time() <= end:
                #break the thread after start has been pressed again
                if not self.is_running:
                    return

                #reading in initial values 1.0 is start in tkinter
                input_value = self.textbox.get('1.0', 'end-1c')
                typed_list = input_value.split()
                
                stripped_list = [word.translate(self.translator) for word in typed_list[:-1]]

                #add either autocorrected words or the original symbol collection should all symbols be stripped
                revised = []
                for index in range(len(stripped_list)):
                    try:
                        if stripped_list[index] != '':
                            revised.append(autocorrect(stripped_list[index].lower(), words_list, score_function_final))
                        else:
                            revised.append(typed_list[index])
                    except:
                        revised.append(typed_list[i])

                #handles capitalization
                for i in range(len(stripped_list)):
                    word = stripped_list[i]
                    if word != '' and word[0].isupper():
                        revised[i] = revised[i].capitalize()

                for i in range(len(typed_list) - 1):
                    consider = typed_list[i]
                    #calculating first and last appearance of a letter
                    for j in range(len(consider)):
                        if consider[j] not in string.punctuation:
                            first = j
                            break
                    for j in reversed(range(len(consider))):
                        if consider[j] not in string.punctuation:
                            last = j
                            break
                    #adds punctuation for things such as ,"Before
                    if consider != revised[i]:
                        if first != 0:
                            revised[i] = consider[:first] + revised[i]
                        if last != len(consider) - 1:
                            revised[i] = revised[i] + consider[last + 1:]
                #checking inputs for newly typed words
                input_value = self.textbox.get('1.0', 'end-1c')
                if len(input_value) > 0:
                    #person has just left a space because they are a typing a new word so this ends in a space
                    if input_value[-1] == ' ' and len(typed_list) > 1:
                        corrected = ' '.join(revised) + ' ' + ' '.join(input_value.split()[len(revised) :]) + ' '
                    #if not end in space just keep whatever was typed after what we revise using autocorrect
                    elif len(revised) > 0:
                        corrected = ' '.join(revised) + ' ' + ' '.join(input_value.split()[len(revised) :])
                    #if nothing was revised we can simply leave our input necessary?
                    else:
                        corrected = input_value
                else:
                    corrected = ''

                #changing textbox contents
                self.textbox.delete('1.0',END)
                self.textbox.insert('1.0', corrected)

                #updating info like wpm or accuraccy
                results = analyze(self.reference_text.get(), corrected, start, time.time())
                speed, accuracy = results[0], results[1]
                self.wpm_var.set(str(round(speed, 1)))
                self.accuracy.set(str(round(accuracy, 1)))
                self.time.set(str(round(60 - (time.time() - start))))
                time.sleep(0.5)
            #final basically runs the loop to check for autocorrecting things once more after time is done in case autocrrect was too slow
            self.final_review(start)

        else:
            while time.time() <= end:
                if not self.is_running:
                    return
                #retrieve the input
                input_value = self.textbox.get('1.0', 'end-1c')
                #calculate wpm and accuracy
                result = analyze(self.reference_text.get(), input_value, start, time.time())
                speed, accuracy = result[0], result[1]
                #set wrpm and accuracy
                self.wpm_var.set(str(round(speed, 1)))
                self.accuracy.set(str(round(accuracy, 1)))
                #update time
                self.time.set(str(round(60 - (time.time() - start))))
                time.sleep(0.5)
            self.time.set('0')


    def final_review(self, start):
        self.time.set('0')
        if self.autocorrect.get() == 1:
                #raw input
                input_value = self.textbox.get('1.0', 'end-1c')
                #input split by spaces
                typed_list = input_value.split()
                #punctuation removed
                stripped_list = [word.translate(self.translator) for word in typed_list[:-1]]
                revised = []

                #Autocorrects current words on display after removing punctuation
                for index in range(len(stripped_list)):
                    try:
                        if stripped_list[index] != '':
                            revised.append(autocorrect(stripped_list[index].lower(), words_list, score_function_final))
                        else:
                            revised.append(typed_list[index])
                    except:
                        revised.append(typed_list[i])

                #handles capitalization
                for i in range(len(stripped_list)):
                    word = stripped_list[i]
                    if word != '' and word[0].isupper():
                        revised[i] = revised[i].capitalize()

                #finds the index of the first and last word in the original so wrapping punctuation can be added
                for i in range(len(typed_list) - 1):
                    consider = typed_list[i]
                    for j in range(len(consider)):
                        if consider[j] not in string.punctuation:
                            first = j
                            break
                    for j in reversed(range(len(consider))):
                        if consider[j] not in string.punctuation:
                            last = j
                            break
                    #adds wrapping punctuation
                    if consider != revised[i]:
                        if first != 0:
                            revised[i] = consider[:first] + revised[i]
                        if last != len(consider) - 1:
                            revised[i] = revised[i] + consider[last + 1:]
                input_value = self.textbox.get('1.0', 'end-1c')
                #joins revised words with with what has been typed since corrections were made
                if len(input_value) > 0:
                    if input_value[-1] == ' ' and len(typed_list) > 1:
                        corrected = ' '.join(revised) + ' ' + ' '.join(input_value.split()[len(revised) :]) + ' '
                    elif len(revised) > 0:
                        corrected = ' '.join(revised) + ' ' + ' '.join(input_value.split()[len(revised) :])
                    else:
                        corrected = input_value
                else:
                    corrected = ''

                #clears the box and adds back all changed content
                self.textbox.delete('1.0',END)
                self.textbox.insert('1.0', corrected)

                #gets updated information(wpm, accuracy)
                results = analyze(self.reference_text.get(), corrected, start, time.time())
                speed, accuracy = results[0], results[1]

                #updates the display
                self.wpm_var.set(str(round(speed, 1)))
                self.accuracy.set(str(accuracy))
                self.time.set('0')


    def thread(self):
        #making variable to keep track of activity of second thread(used to kill second thread)
        self.is_running = not self.is_running

        #when starting the next reference text needs to be loaded
        self.reference_text.set(new_sample(self.path, self.row))
        self.backup.set(self.reference_text.get())

        #if pig_latin is enabled the new reference text should have pig_latin enabled
        if self.pig_latin.get() == 1:
            self.enable_piglatin()

        #updating next reference text to be chosen
        self.row = (self.row + 1) % self.num_paragraphs

        #starting should clear current text and reset all variables
        self.textbox.delete('1.0', END)
        self.time.set('60')
        self.accuracy.set('0')
        self.wpm_var.set('0')

        #use second thread to pull and update text(needed because without it not possible to type and have updating text)
        global submit_thread
        submit_thread = threading.Thread(target=self.get_input)
        self.thread = submit_thread
        submit_thread.daemon = True

        #in the event a second thread is running this will allow it to shut down prior to opening a new one
        time.sleep(1)
        if self.is_running == False:
            self.is_running = True

        #intializing the typing test
        submit_thread.start()



    def stop(self):
        self.is_running = False
        time.sleep(1)

        
    def enable_autocorrect(self):
        #when pig_latin is enabled autocorrect can't be activated
        if self.pig_latin.get() == 1:
            self.autocorrect.set(0)

    def enable_piglatin(self):
        #when autocorrect is activated pig_latin cannot be activated
        if self.autocorrect.get() == 1:
            self.pig_latin.set(0)

        #how to convert to pig_latin
        if self.pig_latin.get() == 1:

            #self.backup.set(self.reference_text.get()) #necessary?

            #split up the reference 
            starting =  self.reference_text.get().split()
            stripped = [word.translate(self.translator) for word in starting]
            revised = []
            for index in range(len(stripped)):
                #this try-except is meant to handle numbers, 'F' or other things that have cannot be handled by pig_latin
                try:
                    word = stripped[index]
                    #this if-else is because only punctuation need to be added such as -, ?!
                    if word != '':
                        revised.append(pig_latin(word.lower()))
                    else:
                        revised.append(starting[index])
                except:
                    revised.append(word)

            #handles capitalization
            for i in range(len(stripped)):
                word = stripped[i]
                if word != '' and word[0].isupper():
                    revised[i] = revised[i].capitalize()

            #for words with punctuation such as "Before, or end", defines first and last as first and last appearance of a letter
            for i in range(len(starting)):
                word = starting[i]
                for j in range(len(word)):
                    if word[j] not in string.punctuation:
                        first = j
                        break
                for j in reversed(range(len(word))):
                    if word[j] not in string.punctuation:
                        last = j
                        break

                #Adding punctuation from the original word using first/last
                if word != revised:
                    if first != 0:
                        revised[i] = word[:first] + revised[i]
                    if last != len(word) - 1:
                        revised[i] = revised[i] + word[last + 1:]

            self.reference_text.set(' '.join(revised))
        else:
            self.reference_text.set(self.backup.get())

root = Tk()
root.title('61A Autocorrect')
root.minsize(600, 500)
app = proj2gui(root)
root.mainloop()
