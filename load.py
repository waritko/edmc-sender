import sys
import ttk
import Tkinter as tk
import requests

from config import applongname, appversion
import myNotebook as nb
from config import config


this = sys.modules[__name__]
this.s = None
this.prep = {}
this.session = requests.Session()


def plugin_start():
    this.email = tk.StringVar(value=config.get("EDStatsEmail"))
    return 'EDStats'

	
def plugin_app(parent):
    this.parent = parent
    label = tk.Label(parent, text="EDStats:")
    this.status = tk.Label(parent, text="Disconnected", anchor=tk.W)
    return (label, this.status)


def plugin_prefs(parent):
    frame = nb.Frame(parent)
    frame.columnconfigure(1, weight=1)

    site_label = nb.Label(frame, text="EDStats Configuration")
    site_label.grid(padx=10, row=8, sticky=tk.W)	
	
    email_label = nb.Label(frame, text="EDStats Email")
    email_label.grid(padx=10, row=10, sticky=tk.W)

    email_entry = nb.Entry(frame, textvariable=this.email)
    email_entry.grid(padx=10, row=10, column=1, sticky=tk.EW)

    return frame

def prefs_changed():
    config.set("EDStatsEmail", this.email.get())

def journal_entry(cmdr, system, station, entry, state):
    #this.status['text'] = "Sending..."
    url = "https://vserver.varak.net/ed/journal.php"
    post = {
        "cmdr" : cmdr,
        "entry" : entry,
        "email" : this.email.get()
        }
    r = this.session.post(url, json=post, stream=False)
    if r.status_code == 200:
        this.status['text'] = "Success"
    else:
        this.status['text'] = "Fail: " + str(r.status_code)

# Update some data here too
def cmdr_data(data):
    #this.status['text'] = "Sending..."
    url = url = "https://vserver.varak.net/ed/cmdr.php"
    post = {
        "raw" : data,
        "email" : this.email.get()
        }
    r = this.session.post(url, json=post, stream=False)
    if r.status_code == 200:
        this.status['text'] = "Success"
    else:
        this.status['text'] = "Fail: " + str(r.status_code)
