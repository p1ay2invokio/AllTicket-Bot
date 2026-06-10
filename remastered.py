import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

# ============================================================
# Mock API — สลับกับ import remastered_api as api_module
# ============================================================
class MockAPI:
    def getShowTime(self, perform_id):
        return {
            'success': True,
            'data': {
                'event_info': {
                    'name': 'MILLI WORLD TOUR 2025 — BANGKOK',
                    'list_round': [
                        {'roundId': 'R001', 'roundLabel': 'ศุกร์ 18 ก.ค. 68  18:00 น.'},
                        {'roundId': 'R002', 'roundLabel': 'เสาร์ 19 ก.ค. 68  18:00 น.'},
                        {'roundId': 'R003', 'roundLabel': 'อาทิตย์ 20 ก.ค. 68  15:00 น.'},
                    ]
                }
            }
        }
    def getShowZoneAvailable(self, pid, rid):
        return {
            'success': True,
            'data': {
                'seat_available': [
                    {'name': 'GA',  'type': 'STAND', 'amount': 'AVAILABLE'},
                    {'name': 'A1',  'type': 'SEAT',  'amount': 42},
                    {'name': 'A2',  'type': 'SEAT',  'amount': 0},
                    {'name': 'B1',  'type': 'SEAT',  'amount': 15},
                    {'name': 'VIP', 'type': 'VIP',   'amount': 8},
                ]
            }
        }
    def getSeat(self, pid, rid, zone):
        import random
        sub = {'zoneId': zone, 'seat': []}
        rows = ['A','B','C','D','E','F','G']
        for ri, row in enumerate(rows):
            for col in range(1, 14):
                s = random.choice(['A','A','A','P','R'])
                sub['seat'].append({
                    'rowNo': str(ri), 'colNo': str(col),
                    'status': s, 'seatNo': str(col),
                    'rowName': row, 'priceAmt': '1500'
                })
        return {'success': True, 'data': {'seats_available': [sub]}}

try:
    import remastered_api as api_module
except ImportError:
    api_module = MockAPI()

# ============================================================
# THEME
# ============================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

C_BG       = "#0F0F13"
C_SURFACE  = "#1A1A24"
C_SURFACE2 = "#22222F"
C_BORDER   = "#2E2E42"
C_ACCENT   = "#7C6EFA"
C_ACCENT2  = "#A78BFA"
C_CYAN     = "#22D3EE"
C_GREEN    = "#34D399"
C_YELLOW   = "#FCD34D"
C_RED      = "#F87171"
C_WHITE    = "#F1F0FF"
C_MUTED    = "#6B6B8A"

# ============================================================
# STATE
# ============================================================
all_seats_dict     = {}
selected_seats_data = {}
round_radio_refs   = []
pulse_jobs         = {}   # seat_id -> after job id

# ============================================================
# APP
# ============================================================
app = ctk.CTk()
app.title("Concert Seat Picker")
app.geometry("860x920")
app.configure(fg_color=C_BG)
app.resizable(True, True)

selected_round_var = ctk.StringVar(value="")

# ── HELPERS ─────────────────────────────────────────────────
def log(msg, clear=True):
    txt_log.configure(state="normal")
    if clear:
        txt_log.delete("1.0", "end")
    txt_log.insert("end", msg + "\n")
    txt_log.see("end")
    txt_log.configure(state="disabled")

def log_append(msg):
    log(msg, clear=False)

def update_counter():
    n = len(selected_seats_data)
    if n == 0:
        lbl_counter.configure(text="ยังไม่ได้เลือก", text_color=C_MUTED)
        btn_confirm.configure(state="disabled", fg_color=C_SURFACE2)
    else:
        lbl_counter.configure(text=f"{n} ที่นั่ง", text_color=C_YELLOW)
        btn_confirm.configure(state="normal", fg_color=C_ACCENT)

# ── SEAT CANVAS ANIMATION ────────────────────────────────────
def pulse_ring(seat_id, radius, step=0):
    """วาด expanding ring animation รอบที่นั่งที่เลือก"""
    tag = f"pulse_{seat_id}"
    seat_canvas.delete(tag)
    if seat_id not in selected_seats_data:
        return
    info = all_seats_dict.get(seat_id)
    if not info:
        return
    cx, cy = info.get('_cx', 0), info.get('_cy', 0)
    alpha  = max(0, 1.0 - step / 20)
    r      = radius + step * 1.2
    # simulate opacity via color mix between accent and bg
    def lerp_hex(c1, c2, t):
        r1,g1,b1 = int(c1[1:3],16),int(c1[3:5],16),int(c1[5:7],16)
        r2,g2,b2 = int(c2[1:3],16),int(c2[3:5],16),int(c2[5:7],16)
        rr = int(r1 + (r2-r1)*t)
        gg = int(g1 + (g2-g1)*t)
        bb = int(b1 + (b2-b1)*t)
        return f"#{rr:02x}{gg:02x}{bb:02x}"
    color = lerp_hex(C_ACCENT, "#0A0A12", 1 - alpha)
    seat_canvas.create_oval(
        cx-r, cy-r, cx+r, cy+r,
        outline=color, width=1.5, fill="", tags=tag
    )
    if step < 20:
        job = seat_canvas.after(40, lambda: pulse_ring(seat_id, radius, step+1))
        pulse_jobs[seat_id] = job
    else:
        # restart loop
        job = seat_canvas.after(600, lambda: pulse_ring(seat_id, radius, 0))
        pulse_jobs[seat_id] = job

def stop_pulse(seat_id):
    if seat_id in pulse_jobs:
        seat_canvas.after_cancel(pulse_jobs.pop(seat_id))
    seat_canvas.delete(f"pulse_{seat_id}")

# ── LOGIC ────────────────────────────────────────────────────
def fetch_data():
    pid = entry_id.get().strip()
    if not pid:
        messagebox.showwarning("แจ้งเตือน", "กรุณาใส่ Perform ID ก่อนครับ")
        return
    try:
        data = api_module.getShowTime(pid)
        # clear rounds
        for w in frame_rounds.winfo_children():
            w.destroy()
        round_radio_refs.clear()
        selected_round_var.set("")
        combo_zone.set("")
        combo_zone.configure(values=[])
        seat_canvas.delete("all")
        selected_seats_data.clear()
        all_seats_dict.clear()
        for jid in list(pulse_jobs.keys()):
            stop_pulse(jid)
        update_counter()
        _draw_canvas_placeholder()

        if data.get('success'):
            info   = data['data']['event_info']
            rounds = info['list_round']
            lbl_event.configure(text=info['name'])
            for i, r in enumerate(rounds):
                rb = ctk.CTkRadioButton(
                    frame_rounds,
                    text=r['roundLabel'],
                    variable=selected_round_var,
                    value=r['roundId'],
                    font=ctk.CTkFont(size=13),
                    fg_color=C_ACCENT,
                    hover_color=C_ACCENT2,
                    border_color=C_BORDER,
                )
                rb.pack(anchor="w", padx=12, pady=5)
                round_radio_refs.append(rb)
                if i == 0:
                    rb.select()
            log(f"✨ พบ {len(rounds)} รอบการแสดง\nเลือกรอบ แล้วกด  โหลดโซน")
        else:
            messagebox.showerror("Error", data.get('message', ''))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def get_zone_data():
    pid   = entry_id.get().strip()
    round_ = selected_round_var.get()
    if not round_:
        messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกรอบก่อนครับ")
        return
    log("⏳  กำลังโหลดข้อมูลโซน...")
    app.update()
    try:
        result = api_module.getShowZoneAvailable(pid, round_)
        if result.get('success'):
            seats     = result['data']['seat_available']
            zone_list = []
            log(f"📊  สถานะโซน — รอบ {round_}\n{'─'*34}")
            for s in seats:
                nm  = s['name']
                amt = s['amount']
                if str(amt).upper() == "AVAILABLE":
                    icon = "🟢"; zone_list.append(nm)
                elif isinstance(amt, int) and amt > 0:
                    icon = "🟡"; zone_list.append(nm)
                else:
                    icon = "🔴"
                status = "ว่าง" if str(amt).upper()=="AVAILABLE" else (f"เหลือ {amt} ที่" if isinstance(amt,int) and amt>0 else "เต็ม")
                log_append(f"  {icon}  โซน {nm:<4}  {s['type']:<6}  {status}")
            log_append("─"*34)
            combo_zone.configure(values=zone_list)
            if zone_list:
                combo_zone.set(zone_list[0])
        else:
            log(f"❌  {result.get('message','')}")
    except Exception as e:
        log(f"❌  {e}")

def toggle_seat(seat_id):
    oval_tag = f"oval_{seat_id}"
    if seat_id in selected_seats_data:
        del selected_seats_data[seat_id]
        seat_canvas.itemconfig(oval_tag, fill=C_GREEN, outline="#0D9E6A")
        stop_pulse(seat_id)
    else:
        selected_seats_data[seat_id] = all_seats_dict[seat_id]
        seat_canvas.itemconfig(oval_tag, fill=C_YELLOW, outline="#B8963A")
        cx = all_seats_dict[seat_id].get('_cx', 0)
        cy = all_seats_dict[seat_id].get('_cy', 0)
        pulse_ring(seat_id, 13)
    update_counter()

def fetch_seats():
    pid    = entry_id.get().strip()
    round_ = selected_round_var.get()
    zone   = combo_zone.get()
    if not zone:
        messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกโซนก่อนครับ")
        return
    seat_canvas.delete("all")
    selected_seats_data.clear()
    for jid in list(pulse_jobs.keys()):
        stop_pulse(jid)
    all_seats_dict.clear()
    update_counter()
    log(f"🗺️  กำลังวาดผัง โซน {zone} ...")
    app.update()
    try:
        result = api_module.getSeat(pid, round_, zone)
        if result.get('success'):
            sub_zones = result['data'].get('seats_available', [])
            avail = 0
            row_min_x = {}

            # Stage bar
            seat_canvas.create_rectangle(70, 6, 510, 24,
                fill=C_ACCENT, outline="", tags="stage")
            seat_canvas.create_text(290, 15,
                text="▼   S T A G E   ▼", fill=C_WHITE,
                font=("Tahoma", 8, "bold"), tags="stage")

            for sub in sub_zones:
                z_id = sub.get('zoneId', '')
                for s in sub.get('seat', []):
                    try:
                        r = int(s.get('rowNo', 0))
                        c = int(s.get('colNo', 0))
                    except ValueError:
                        continue
                    st       = s.get('status')
                    seat_no  = s.get('seatNo', '')
                    row_name = s.get('rowName', '')
                    price    = s.get('priceAmt', '')
                    x = c * 38 + 90
                    y = r * 38 + 50
                    R = 14
                    uid = f"{z_id}_{row_name}_{seat_no}"
                    all_seats_dict[uid] = {
                        "zone": z_id, "row": row_name,
                        "seat": seat_no, "price": price,
                        "status": st, "_cx": x, "_cy": y
                    }
                    if st == 'A':   fill, out = C_GREEN,    "#0D9E6A"
                    elif st == 'P': fill, out = "#2A2A3E",  "#3A3A5A"
                    elif st == 'R': fill, out = C_RED,      "#A03030"
                    else:           fill, out = "#333348",  "#444460"

                    ot = f"oval_{uid}"
                    tt = f"tag_{uid}"
                    seat_canvas.create_oval(
                        x-R, y-R, x+R, y+R,
                        fill=fill, outline=out, width=1.5,
                        tags=(tt, ot)
                    )
                    seat_canvas.create_text(x, y, text=seat_no,
                        font=("Tahoma", 7, "bold"),
                        fill="#0A0A12" if st in ('A','R') else C_MUTED,
                        tags=(tt,)
                    )
                    if st == 'A':
                        seat_canvas.tag_bind(tt, "<Button-1>",
                            lambda e, sid=uid: toggle_seat(sid))
                        seat_canvas.tag_bind(tt, "<Enter>",
                            lambda e, sid=uid: seat_canvas.itemconfig(
                                f"oval_{sid}", outline=C_WHITE))
                        seat_canvas.tag_bind(tt, "<Leave>",
                            lambda e, sid=uid: seat_canvas.itemconfig(
                                f"oval_{sid}",
                                outline="#0D9E6A" if sid not in selected_seats_data else "#B8963A"))
                        avail += 1
                    if y not in row_min_x or x < row_min_x[y][0]:
                        row_min_x[y] = (x, row_name)

            for y, (mx, rn) in row_min_x.items():
                seat_canvas.create_text(mx-30, y, text=rn,
                    font=("Tahoma", 9, "bold"), fill=C_ACCENT2)

            bbox = seat_canvas.bbox("all")
            if bbox:
                seat_canvas.configure(
                    scrollregion=(bbox[0]-30, bbox[1]-20, bbox[2]+30, bbox[3]+30))

            if avail > 0:
                log(f"✅  โซน {zone} — พบที่นั่งว่าง {avail} ที่\n"
                    f"👆  คลิกวงกลมสีเขียวเพื่อเลือก")
            else:
                log(f"❌  โซน {zone} — เต็มหมดแล้วครับ")
        else:
            log(f"❌  {result.get('message','')}")
    except Exception as e:
        log(f"❌  {e}")

def confirm_selection():
    if not selected_seats_data:
        messagebox.showwarning("แจ้งเตือน", "ยังไม่ได้เลือกที่นั่งเลยครับ")
        return
    lines = []
    total = 0
    for sid, info in selected_seats_data.items():
        p = int(info['price'])
        total += p
        lines.append(f"  โซน {info['zone']}  แถว {info['row']}  ที่ {info['seat']}   {p:,} ฿")
    messagebox.showinfo(
        "🎟️  สรุปรายการ",
        f"เลือก {len(selected_seats_data)} ที่นั่ง\n\n" +
        "\n".join(lines) +
        f"\n\n{'─'*36}\nรวมทั้งสิ้น  {total:,} บาท"
    )

def _draw_canvas_placeholder():
    seat_canvas.delete("all")
    seat_canvas.create_text(
        300, 160,
        text="เลือกโซน แล้วกด  วาดผังที่นั่ง",
        fill=C_MUTED, font=("Tahoma", 12)
    )

# ============================================================
# LAYOUT
# ============================================================

# ── TOP HEADER ───────────────────────────────────────────────
hdr = ctk.CTkFrame(app, fg_color=C_SURFACE, corner_radius=0, height=64)
hdr.pack(fill="x", side="top")
hdr.pack_propagate(False)

ctk.CTkLabel(hdr, text="🎵", font=ctk.CTkFont(size=22),
             text_color=C_ACCENT).pack(side="left", padx=(20,6), pady=14)
ctk.CTkLabel(hdr, text="Concert Seat Picker",
             font=ctk.CTkFont(size=17, weight="bold"),
             text_color=C_WHITE).pack(side="left")

lbl_event = ctk.CTkLabel(hdr, text="กรุณาค้นหา Perform ID",
                          font=ctk.CTkFont(size=12),
                          text_color=C_MUTED)
lbl_event.pack(side="right", padx=20)

# accent underline
ctk.CTkFrame(app, fg_color=C_ACCENT, corner_radius=0, height=2).pack(fill="x")

# ── BODY ─────────────────────────────────────────────────────
body = ctk.CTkFrame(app, fg_color=C_BG, corner_radius=0)
body.pack(fill="both", expand=True, padx=14, pady=12)
body.columnconfigure(1, weight=1)
body.rowconfigure(0, weight=1)

# ── LEFT SIDEBAR ─────────────────────────────────────────────
sidebar = ctk.CTkScrollableFrame(body, fg_color=C_SURFACE,
                                  corner_radius=14, width=220)
sidebar.grid(row=0, column=0, sticky="ns", padx=(0,12))

def sec(parent, title):
    ctk.CTkLabel(parent, text=title, font=ctk.CTkFont(size=11, weight="bold"),
                 text_color=C_MUTED).pack(anchor="w", padx=14, pady=(16,4))

# STEP 1
sec(sidebar, "STEP 1 — ค้นหางาน")

ctk.CTkLabel(sidebar, text="Perform ID",
             font=ctk.CTkFont(size=12), text_color=C_WHITE).pack(anchor="w", padx=14)
entry_id = ctk.CTkEntry(sidebar, placeholder_text="เช่น 26933",
                         fg_color=C_SURFACE2, border_color=C_BORDER,
                         text_color=C_WHITE, height=36,
                         font=ctk.CTkFont(size=13))
entry_id.pack(fill="x", padx=14, pady=(4,8))
entry_id.insert(0, "26933")

ctk.CTkButton(sidebar, text="🔍  ดึงข้อมูลรอบ", command=fetch_data,
              fg_color=C_ACCENT, hover_color=C_ACCENT2, height=36,
              font=ctk.CTkFont(size=13, weight="bold"),
              corner_radius=8).pack(fill="x", padx=14, pady=(0,8))

# Divider
ctk.CTkFrame(sidebar, fg_color=C_BORDER, height=1, corner_radius=0).pack(fill="x", padx=14, pady=6)

# STEP 2
sec(sidebar, "STEP 2 — เลือกรอบ")

frame_rounds = ctk.CTkFrame(sidebar, fg_color=C_SURFACE2, corner_radius=10)
frame_rounds.pack(fill="x", padx=14, pady=(0,4))
ctk.CTkLabel(frame_rounds, text="  (ยังไม่มีข้อมูล)", text_color=C_MUTED,
             font=ctk.CTkFont(size=12)).pack(pady=10)

ctk.CTkButton(sidebar, text="📋  โหลดโซน", command=get_zone_data,
              fg_color=C_SURFACE2, hover_color=C_BORDER, height=36,
              text_color=C_CYAN, border_width=1, border_color=C_CYAN,
              font=ctk.CTkFont(size=13, weight="bold"),
              corner_radius=8).pack(fill="x", padx=14, pady=(4,8))

ctk.CTkFrame(sidebar, fg_color=C_BORDER, height=1, corner_radius=0).pack(fill="x", padx=14, pady=6)

# STEP 3
sec(sidebar, "STEP 3 — เลือกโซน")

combo_zone = ctk.CTkComboBox(sidebar, values=[], state="readonly",
                              fg_color=C_SURFACE2, border_color=C_BORDER,
                              button_color=C_ACCENT, button_hover_color=C_ACCENT2,
                              text_color=C_WHITE, dropdown_fg_color=C_SURFACE2,
                              dropdown_text_color=C_WHITE,
                              font=ctk.CTkFont(size=13), height=36)
combo_zone.pack(fill="x", padx=14, pady=(0,8))
combo_zone.set("")

ctk.CTkButton(sidebar, text="🗺️  วาดผังที่นั่ง", command=fetch_seats,
              fg_color=C_GREEN, hover_color="#22A070", height=36,
              text_color="#0A0A12",
              font=ctk.CTkFont(size=13, weight="bold"),
              corner_radius=8).pack(fill="x", padx=14, pady=(0,8))

ctk.CTkFrame(sidebar, fg_color=C_BORDER, height=1, corner_radius=0).pack(fill="x", padx=14, pady=6)

# LEGEND
ctk.CTkLabel(sidebar, text="สัญลักษณ์",
             font=ctk.CTkFont(size=11, weight="bold"),
             text_color=C_MUTED).pack(anchor="w", padx=14, pady=(4,6))

def legend_dot(parent, color, label):
    f = ctk.CTkFrame(parent, fg_color="transparent")
    f.pack(anchor="w", padx=16, pady=2)
    c = tk.Canvas(f, width=12, height=12,
                  bg=C_SURFACE, bd=0, highlightthickness=0)
    c.create_oval(1,1,11,11, fill=color, outline="")
    c.pack(side="left")
    ctk.CTkLabel(f, text=f"  {label}", font=ctk.CTkFont(size=12),
                 text_color=C_MUTED).pack(side="left")

legend_dot(sidebar, C_GREEN,   "ว่าง (คลิกได้)")
legend_dot(sidebar, C_YELLOW,  "เลือกแล้ว ✦ pulse")
legend_dot(sidebar, "#2A2A3E", "ถูกจองแล้ว")
legend_dot(sidebar, C_RED,     "ไม่พร้อมขาย")

# ── RIGHT PANEL ──────────────────────────────────────────────
right = ctk.CTkFrame(body, fg_color=C_BG, corner_radius=0)
right.grid(row=0, column=1, sticky="nsew")
right.rowconfigure(1, weight=1)
right.columnconfigure(0, weight=1)

# Log box
log_card = ctk.CTkFrame(right, fg_color=C_SURFACE, corner_radius=12)
log_card.grid(row=0, column=0, sticky="ew", pady=(0,10))

ctk.CTkLabel(log_card, text="  📡  ผลลัพธ์",
             font=ctk.CTkFont(size=11, weight="bold"),
             text_color=C_MUTED).pack(anchor="w", padx=14, pady=(10,4))

txt_log = ctk.CTkTextbox(log_card, height=130, fg_color=C_SURFACE2,
                          text_color=C_CYAN, corner_radius=8,
                          font=ctk.CTkFont(family="Courier New", size=12),
                          state="disabled")
txt_log.pack(fill="x", padx=12, pady=(0,12))

# Canvas card
map_card = ctk.CTkFrame(right, fg_color=C_SURFACE, corner_radius=12)
map_card.grid(row=1, column=0, sticky="nsew")
map_card.rowconfigure(1, weight=1)
map_card.columnconfigure(0, weight=1)

map_hdr = ctk.CTkFrame(map_card, fg_color="transparent")
map_hdr.grid(row=0, column=0, columnspan=2, sticky="ew", padx=14, pady=(12,6))

ctk.CTkLabel(map_hdr, text="ผังที่นั่ง",
             font=ctk.CTkFont(size=14, weight="bold"),
             text_color=C_WHITE).pack(side="left")

lbl_counter = ctk.CTkLabel(map_hdr, text="ยังไม่ได้เลือก",
                            font=ctk.CTkFont(size=12),
                            text_color=C_MUTED)
lbl_counter.pack(side="right")

# Canvas + scrollbars (must use tk here — CTk has no Canvas)
canvas_wrap = tk.Frame(map_card, bg=C_SURFACE, bd=0)
canvas_wrap.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0,12))
canvas_wrap.rowconfigure(0, weight=1)
canvas_wrap.columnconfigure(0, weight=1)
map_card.rowconfigure(1, weight=1)
map_card.columnconfigure(0, weight=1)

vscroll = tk.Scrollbar(canvas_wrap, orient="vertical",   bg=C_SURFACE2, troughcolor=C_SURFACE)
hscroll = tk.Scrollbar(canvas_wrap, orient="horizontal", bg=C_SURFACE2, troughcolor=C_SURFACE)
vscroll.grid(row=0, column=1, sticky="ns")
hscroll.grid(row=1, column=0, sticky="ew")

seat_canvas = tk.Canvas(canvas_wrap, bg="#09090F",
                         xscrollcommand=hscroll.set,
                         yscrollcommand=vscroll.set,
                         highlightthickness=0, bd=0)
seat_canvas.grid(row=0, column=0, sticky="nsew")
vscroll.config(command=seat_canvas.yview)
hscroll.config(command=seat_canvas.xview)

_draw_canvas_placeholder()

# ── BOTTOM BAR ───────────────────────────────────────────────
bot = ctk.CTkFrame(app, fg_color=C_SURFACE, corner_radius=0, height=68)
bot.pack(fill="x", side="bottom")
bot.pack_propagate(False)

ctk.CTkFrame(bot, fg_color=C_BORDER, height=1, corner_radius=0).pack(fill="x", side="top")

btn_confirm = ctk.CTkButton(
    bot, text="🎟️   ยืนยันที่นั่งที่เลือก", command=confirm_selection,
    fg_color=C_SURFACE2, hover_color=C_ACCENT, height=42,
    font=ctk.CTkFont(size=14, weight="bold"), text_color=C_MUTED,
    corner_radius=10, state="disabled",
)
btn_confirm.pack(pady=12, ipadx=20)

update_counter()
app.mainloop()