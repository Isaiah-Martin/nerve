#Author: Isaiah Martin // Dartmouth '21
#Started October 2017
#Nerve - an app for insecurities

# Change these:
pylib_path1 = <"PythonistaAppTemplate/Supporting_Files/PythonistaKit.framework">
#pylib_path2 = <"PythonistaAppTemplate/Supporting_Files/PythonistaKit.framework/pylib_ext">

import shutil
import os
import subprocess

def check_is_executable(file_path):
    file_output = subprocess.check_output(['file', file_path])
    if 'executable' in file_output:
        return True, file_output
    return False, file_output

def fix_executable(file_path):
    with open(file_path, 'r') as f:
        source = f.read()
    with open(file_path, 'w') as f:
        f.write('#\input texinfo\n' + source)
    is_executable, out = check_is_executable(file_path)
    return not is_executable

def fix_pylib(pylib_path, dry_run=False):
    for path, dirs, files in os.walk(pylib_path):
        for filename in files:
            full_path = full_path = os.path.join(path, filename)
            is_executable, file_output = check_is_executable(full_path)
            if is_executable:
                extension = os.path.splitext(full_path)[1].lower()
                if extension == '.py' or extension == '.pym' or filename == 'command_template':
                    if dry_run:
                        print '### Executable found: %s' % (filename,)
                    else:
                        print 'Fixing %s...' % (filename,)
                        fixed = fix_executable(full_path)
                        if not fixed:
                            print '### FIXING %s FAILED' % (full_path,)
                        else:
                            print 'Fixed'
                else:
                    print '### Executable found, but does not seem to be Python code: %s' % (full_path,)

if __name__ == '__main__':
    fix_pylib(pylib_path1)
    fix_pylib(pylib_path2)
    
import ui
import console
import time
import json
import smtplib
from email.mime.text import MIMEText

(window_width,window_height) = ui.get_screen_size()
def aligncover():
	title = homeview['title']
	feed = homeview['feed']
	post = homeview['post']
	contact = homeview['contact_btn']
	image = homeview['image']
	title.x=window_width/2-(title.width/2+10)
	title.y=window_height*.07
	feed.width = window_width*.48
	feed.x = window_width/2-(feed.width/2)
	feed.y = window_height*.20
	feed.height = window_height*.18
	post.width = feed.width
	post.x = feed.x
	post.y=window_height*.45
	post.height = feed.height
	contact.width = feed.width
	contact.x = feed.x
	contact.y = window_height*.70
	contact.height = feed.height
	image.width = contact.width/2
	image.x = window_width/2-(image.width/2)
	image.y = contact.y
	image.height = contact.height

def alignfeed():
	title = feedview['title']
	table = feedview['posttable'].data_source
	title.width = window_width
	title.height = window_height*.05

	table.width = window_width
	table.height = window_height-title.height
	table.y = title.height+title.y

def alignpost():
	title=postview['title']
	subtitle = postview['subtitle']
	post = postview['user_post']
	year = postview['user_class']
	gender = postview['user_gender']
	aff = postview['user_affiliation']
	btn = postview['post_btn']
	title.width = window_width
	title.x = 0
	title.y=0
	subtitle.y = title.height+10
	subtitle.x = title.x
	subtitle.width = title.width
	post.x = window_width/2-(post.width/2)
	year.x = window_width/2-(post.width/2)
	gender.x = year.x
	aff.x = year.x
	btn.x = window_width/2-(btn.width/2)
	post.y = subtitle.height+subtitle.y+10
	year.y = post.y+post.height+10
	gender.y = year.y+year.height+10
	aff.y = gender.y+gender.height+10
	btn.y = aff.y+aff.height+10
	
def aligncontact():
	title = contactview['title']
	msgtitle = contactview['msgtitle']
	msg = contactview['msg']
	usertitle = contactview['usertitle']
	user = contactview['user']
	btn = contactview['contactBtn']
	image = contactview['contact_image']
	
	title.x = window_width/2-(title.width/2)
	msgtitle.x = window_width/2-(msg.width/2)
	msg.x = window_width/2-(msg.width/2)
	usertitle.x = window_width/2-(user.width/2)
	user.x = window_width/2-(user.width/2)
	btn.x = window_width/2-(btn.width/2)
	image.x = window_width/2-(image.width/2)
#pull in data
def display():
	feed = feedview['posttable']
	file = open("database.json","r")
	datastore = json.load(file)
	for index in range(len(datastore["posts"])):
		feed.data_source.font = ("ChalkboardSE-Light",13)
		feed.data_source.items.insert(0,datastore["posts"][index]["post"])
	file.close()
	
#validate user posts
def validate():
	post = postview['user_post']
	#msg = postview['validate']
	#post validation
	character_count = len(post.text)
	min=40
	max=150
	if character_count < min:
		post.border_color = "red"
		#msg.color = "red"
		msg = str(min) + " characters min"
		console.hud_alert(msg,"error",2.0)
	elif character_count > max:
		post.border_color = "red"
		#msg.color = "red"
		msg = str(max) + "characters max"
		console.hud_alert(msg,"error",2.0)
	else:
		post.border_color = "#2cc157"
		msg  = "Thank you for sharing"
		console.hud_alert(msg,"success",2.0)
		post.text=""
		return True
	return False
	
def validate_contact():
	post = contactview['msg']
	#name = postview['validate']
	#post validation
	character_count = len(post.text)
	min=34
	max=91
	if character_count < min:
		post.border_color = "red"
		#msg.color = "red"
		msg = str(min) + " characters min"
		console.hud_alert(msg,"error",2.0)
	elif character_count > max:
		post.border_color = "red"
		#msg.color = "red"
		msg = str(max) + "characters max"
		console.hud_alert(msg,"error",2.0)
	else:
		post.border_color = "#2cc157"
		msg  = "Thank you for sharing"
		console.hud_alert(msg,"success",2.0)
		post.text=""
		return True
	return False
	
def getInfo():
	year = postview["user_class"].selected_index
	gender = postview["user_gender"].selected_index
	affiliation = postview["user_affiliation"].selected_index
	print("affiliation")
	if year==0:
		year = "21"
	if year==1:
		year = "20"
	if year==2:
		year = "19"
	if year ==3:
		year = "18"
	if gender == 0:
		gender = "Male"
	if gender == 1:
		gender= "Female"
	if gender == 2:
		gender="Gender Nonconforming"
	if affiliation == 0:
		affiliation = ""
	if affiliation == 1:
		affiliation = "Military Vet"
	if affiliation == 2:
		affiliation ="First Generation"
	if affiliation== 3:
		affiliation="Athlete"
	return [year,gender,affiliation]

def view_community(sender):
   	display()
	feedview.present('sheet',title_bar_color="#000000")
def send_personal(sender):
	btn = postview['post_btn']
	btn.font = ("System",18)
    #alignpost()
	postview.present('sheet',title_bar_color="#000000")
	

#when a row is tapped
def selection(sender):
	feed = feedview["posttable"]
	with open("database.json") as file:
		datastore = json.load(file)
	if sender.accessory_action:
		index = feed.data_source.selected_row
		year = "'"+ datastore["posts"][index]["class"]
		gender=" / "+datastore["posts"][index]["gender"]
		affiliation=" / "+datastore["posts"][index]["affiliation"]
		msg = year+gender+affiliation
		console.hud_alert(msg,"success",1.2)

 #When button pressed save data and write to database
def submit_post(sender):
	post = postview["user_post"]
	answers = getInfo()
	if validate():
		with open("database.json") as file:
			datastore = json.load(file)
		newdata = {"post":post.text,"class":answers[0], "gender":answers[1], "affiliation": answers[2]}
		datastore["posts"].append(newdata)
		with open("database.json", "w") as newfile:
			json.dump(datastore,newfile)
		#post.text = ""

def contactme(sender):
	btn = contactview['contactBtn']
	btn.font = ("Chalkduster",14)
    #contactview['contact_image'].image = ui.Image("me.jpg")
    #aligncontact()
	contactview.present('sheet',title_bar_color="#000000")

def submit_contact(sender):
	if validate_contact():
		contactmsg = contactview["msg"]
		user = contactview["user"]
		recipient = "isaiah.t.martin@outlook.com"
		sender = "isaiah.t.martin@outlook.com"
		msg = MIMEText(contactmsg.text+"\n"+user.text)
		s = smtplib.SMTP("localhost")
		s.send_message(msg)
		s.quit()
	
postview = ui.load_view('post')
homeview = ui.load_view('cover')
feedview = ui.load_view('feed')
contactview = ui.load_view('contact')

#meimage = homeview["image"]
#me = ui.Image("coder.JPG")
#meimage.image = me

aligncover()
alignpost()
alignfeed()
aligncontact()
#display()
homeview.present('sheet',hide_title_bar=True, animated=False)

