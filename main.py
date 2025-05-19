import socket
import ipaddress
import subprocess
import tkinter
from tkinter import scrolledtext
from tkinter import ttk
import threading

#Program
def ping():
    subnet = subnet_entry.get()
    try:
        network = ipaddress.ip_network(f"{subnet}/24").hosts()
    except ValueError:
        output_text.insert(tkinter.END, "Invalid subnet entered.\n")
        bar.stop()
        button.config(state="normal")
        return

    
    for ip in network:
        result = subprocess.run(["ping", "-n", "1", str(ip)], capture_output=True, text=True)

        if "time" in result.stdout:
            try:
                hostname = socket.gethostbyaddr(str(ip))[0]
            except socket.herror:
                hostname = "Unknown"
        
            output_text.insert(tkinter.END, f"{ip} is active. {hostname}\n")
        else:
            output_text.insert(tkinter.END, f"{ip} is not responding.\n")

    bar.stop()
    button.config(state="normal")
    

#Starting the Program
def run_ping_thread():
    button.config(state="disabled")
    thread = threading.Thread(target=ping)
    bar.start()
    thread.start()
    output_text.delete("1.0", tkinter.END)

#Window
window = tkinter.Tk()
window.title("LAN Scanner")
window.config(padx=50, pady=50, bg="#EEEEEE")
window.resizable(False, False)

#Canvas
canvas =tkinter.Canvas(height=200, width=200, bg="#EEEEEE", highlightthickness=0)

#Labels
label1 = tkinter.Label(text="Enter Your Subnet (255.255.255.0):", font=("Arial", 11), bg="#EEEEEE", fg="#222831")
label1.grid(row=1, column=0)

#Entries
subnet_entry = tkinter.Entry(width=35)
subnet_entry.grid(row=1, column=1, columnspan=2)
subnet_entry.focus()

#Buttons
button = tkinter.Button(text="Add", width=30, bg="#76ABAE", fg="#222831", command=run_ping_thread)
button.grid(row=4, column=1, columnspan=2)

# Output box
output_text = scrolledtext.ScrolledText(window, width=75, height=25, bg="white", fg="black", font=("Consolas", 10))
output_text.grid(row=2, column=0, columnspan=3, padx=5, pady=10)

#Progress Bar
bar = ttk.Progressbar(window, mode="indeterminate", length=300)
bar.grid(row=3, column=0, columnspan=3, pady=5)




window.mainloop()


