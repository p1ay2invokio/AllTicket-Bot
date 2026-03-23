from playwright.sync_api import sync_playwright
import api
from rich import print
import time
import tkinter as tk
from tkinter import messagebox

def runProgram(perform_name):
    info = api.info(perform_name)

    print(info)

    consentId = ''
    consentValue = ''

    if(info['data'].get('event_consent')):
        print("Have")
        consentId = info['data']['event_consent'][0]['consentId']
        consentValue = info['data']['event_consent'][0]['active']


    performId = info['data']['event_id']

    # performId = 26027

    round_res = api.getRound(performId)


    print("ROUND : ", round_res)

    if(round_res['success']):
        print(round_res['data']['event_info']['name'])
        print("--------------------------------------")
        print(f"จองสูงสุด: {round_res['data']['event_info']['maxReserve']} ที่นั่ง")
        
        seat = api.seatAvailable(performId, round_res['data']['event_info']['list_round'][0]['roundId'])
        
        print("Seat : ", seat)
        
        zoneId = seat['data']['seat_available'][0]['id']
        seatLabel = seat['data']['seat_available'][0]['name']
        seatType = seat['data']['seat_available'][0]['type']
        
        booked = api.reserve(performId, round_res['data']['event_info']['list_round'][0]['roundId'], zoneId, seatLabel, seatType, 1, consentId, consentValue)
        
        
        
        print("BOOK : ", booked)
        
        print(f"Waiting time for booking! {booked['data']['waitTime']} sec")
        
        for i in range(5):
            time.sleep(5)
            check = api.checkBooking(booked['data']['uuid'])
            
            
            
            
            if(check['success']):
                return True
                
            print("Check : ", check)
            
        
        



def on_submit():
    val1 = entry1.get()
    val2 = entry2.get()
    
    
    
    print("Val1 : ", val1)
    print("Val2 : ", val2)
    
    if(val1 == '' or val2 == ''):
        messagebox.showinfo(title="Error", message="กรอกข้อมูลให้ครบถ้วน!")
    else:
        api.setToken(val1)
        
        
        btn.config(text="กำลังรัน... โปรดรอ", state="disabled")
        root.update()
        
        
        
        response = runProgram(val2)
        
        
        print("RESPONSEEeeee : ", response)
    
        if(response):
            messagebox.showinfo(title="Success" ,message=f"จองบัตร {val2} สำเร็จ!")
        else:
            messagebox.showinfo(title="Error", message=f"จองบัตรไม่สำเร็จ!")
            
            
        btn.config(text="เริ่มกดบัตร", state="normal")
    
    
root = tk.Tk()
root.title("บอทกดบัตร AllTicket")
root.geometry("300x200")

tk.Label(root, text="Token Id").pack(pady=(20, 0))
entry1 = tk.Entry(root, width=30)
entry1.pack()

tk.Label(root, text="Perform Name").pack(pady=(10, 0))
entry2 = tk.Entry(root, width=30)
entry2.pack()

btn = tk.Button(root, text="เริ่มกดบัตร", command=on_submit)
btn.pack(pady=20)

root.mainloop()
    
    
    
    
    
    
