import customtkinter as ctk
from tkinter import messagebox
import api
import json
import os
import base64
import json
import time


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

TOKEN_FILE = os.path.join(os.path.dirname(__file__), ".token.json")

def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": token}, f)
        
def decode_token_exp(token):
    try:
        payload = token.split(".")[1]
        # เติม padding ให้ครบ
        payload += "=" * (4 - len(payload) % 4)
        decoded = json.loads(base64.b64decode(payload))
        return decoded.get("exp", 0)
    except Exception:
        return 0

def is_token_valid(token):
    exp = decode_token_exp(token)
    return time.time() < exp

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f).get("token", "")
    return ""

# ─── App ──────────────────────────────────────────────────
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AllTicket Bot")
        self.geometry("420x520")
        self.resizable(False, False)

        self.current_frame = None
        saved_token = load_token()

        if saved_token and is_token_valid(saved_token):
            api.setToken(saved_token)
            self.show_home()
        else:
            # token หมดอายุหรือไม่มี → ลบทิ้งแล้วไป login
            if os.path.exists(TOKEN_FILE):
                os.remove(TOKEN_FILE)
            self.show_login()

    def switch_frame(self, frame_class, *args):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True, padx=32, pady=24)

    def show_login(self):
        self.switch_frame(LoginFrame)

    def show_home(self):
        self.switch_frame(HomeFrame)


# ─── Login Frame ──────────────────────────────────────────
class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        ctk.CTkLabel(self, text="🎟  AllTicket Bot", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(8, 4))
        ctk.CTkLabel(self, text="ใส่ Token เพื่อเข้าใช้งาน", font=ctk.CTkFont(size=12), text_color="gray").pack()

        ctk.CTkLabel(self, text="Token ID", anchor="w").pack(fill="x", pady=(24, 4))
        self.entry_token = ctk.CTkEntry(self, placeholder_text="วาง token ที่นี่...", height=38, show="•")
        self.entry_token.pack(fill="x")

        self.btn = ctk.CTkButton(self, text="เข้าสู่ระบบ", height=40, font=ctk.CTkFont(size=14, weight="bold"), command=self.on_login)
        self.btn.pack(fill="x", pady=(20, 0))

    def on_login(self):
        token = self.entry_token.get().strip()
        if not token:
            messagebox.showerror("ข้อผิดพลาด", "กรุณาใส่ Token ก่อน!")
            return
        save_token(token)
        api.setToken(token)
        self.master.show_home()


# ─── Home Frame ───────────────────────────────────────────
class HomeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(header, text="🎟  AllTicket Bot", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        ctk.CTkButton(header, text="ออกจากระบบ", width=90, height=28, font=ctk.CTkFont(size=12), fg_color="transparent", border_width=1, command=self.on_logout).pack(side="right")

        # Input
        ctk.CTkLabel(self, text="Perform ID", anchor="w").pack(fill="x", pady=(20, 4))
        self.entry_perform = ctk.CTkEntry(self, placeholder_text="ใส่ Perform ID...", height=38)
        self.entry_perform.pack(fill="x")

        self.btn_fetch = ctk.CTkButton(self, text="ดึงข้อมูล", height=40, font=ctk.CTkFont(size=14, weight="bold"), command=self.on_fetch)
        self.btn_fetch.pack(fill="x", pady=(16, 0))

        # Result area
        self.result_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.result_frame.pack(fill="x", pady=(16, 0))

    def on_logout(self):
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
        self.master.show_login()

    def on_fetch(self):
        perform_id = self.entry_perform.get().strip()
        if not perform_id:
            messagebox.showerror("ข้อผิดพลาด", "กรุณาใส่ Perform ID!")
            return

        self.btn_fetch.configure(text="⏳ กำลังดึงข้อมูล...", state="disabled")
        self.master.update()

        try:
            round_res = api.getRound(perform_id)
            print("round_res:", round_res)
            if not round_res.get('success'):
                messagebox.showerror("Error", f"ดึงข้อมูล round ไม่สำเร็จ: {round_res.get('message', 'Unknown Error')}")
                return

            data = round_res.get('data', {})
            event_info = data.get('event_info', {})
            rounds = event_info.get('list_round', [])

            if not rounds:
                messagebox.showwarning("Warning", "ไม่พบรอบการแสดงสำหรับงานนี้")
                self.show_results(event_info, [], [])
                return

            # ดึง seat ของ round แรก
            round_id = rounds[0]['roundId'] if rounds else None
            seat_res = api.seatAvailable(perform_id, round_id)
            print("seat_res:", seat_res)
            
            seats = []
            if seat_res.get('success'):
                seats = seat_res.get('data', {}).get('seat_available', [])

            self.show_results(event_info, rounds, seats)

        except Exception as e:
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {str(e)}")
        finally:
            self.btn_fetch.configure(text="ดึงข้อมูล", state="normal")

    def show_results(self, event_info, rounds, seats):
        for w in self.result_frame.winfo_children():
            w.destroy()

        # ชื่องาน
        ctk.CTkLabel(
            self.result_frame,
            text=event_info.get('name', 'ไม่ระบุชื่อ'),
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            self.result_frame,
            text=f"จองสูงสุด: {event_info.get('maxReserve', '-')} ที่นั่ง  |  ต่อคน: {event_info.get('maxSelectSeatPerUser', '-')} ที่นั่ง",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        ).pack(fill="x", pady=(2, 0))

        # Divider
        ctk.CTkFrame(self.result_frame, height=1, fg_color=("gray80", "gray30")).pack(fill="x", pady=10)

        # Rounds
        ctk.CTkLabel(
            self.result_frame,
            text="รอบการแสดง",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray",
            anchor="w"
        ).pack(fill="x")

        for r in rounds:
            ctk.CTkLabel(
                self.result_frame,
                text=f"  🗓  {r.get('roundLabel', r['roundId'])}",
                font=ctk.CTkFont(size=12),
                anchor="w"
            ).pack(fill="x", pady=1)

        # Divider
        ctk.CTkFrame(self.result_frame, height=1, fg_color=("gray80", "gray30")).pack(fill="x", pady=10)

        # Seats
        ctk.CTkLabel(
            self.result_frame,
            text="ที่นั่งว่าง",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray",
            anchor="w"
        ).pack(fill="x")

        if seats:
            for s in seats:
                row = ctk.CTkFrame(self.result_frame, fg_color=("gray90", "gray20"), corner_radius=8)
                row.pack(fill="x", pady=3)
                ctk.CTkLabel(
                    row,
                    text=f"  {s['name']}",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    anchor="w"
                ).pack(side="left", padx=8, pady=6)
                ctk.CTkLabel(
                    row,
                    text=f"{s.get('type', '')}  •  {s.get('amount', '0')}",
                    font=ctk.CTkFont(size=12),
                    text_color="gray",
                    anchor="e"
                ).pack(side="right", padx=8, pady=6)
        else:
            ctk.CTkLabel(
                self.result_frame,
                text="  ไม่มีที่นั่งว่าง หรือดึงข้อมูลไม่ได้",
                font=ctk.CTkFont(size=12),
                text_color="gray",
                anchor="w"
            ).pack(fill="x")



if __name__ == "__main__":
    app = App()
    app.mainloop()