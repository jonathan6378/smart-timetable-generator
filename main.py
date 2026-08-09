import os, tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.ga_engine import TimetableGA
from src.utils import load_csv, initialize_database, save_schedule
from src.exporters import export_excel, export_pdf

BASE=os.path.dirname(os.path.abspath(__file__)); DATA=os.path.join(BASE,"data")
class App:
    def __init__(self,root):
        self.root=root; root.title("Smart Timetable Generator"); root.geometry("1050x700")
        self.courses=load_csv(os.path.join(DATA,"courses.csv")); self.rooms=load_csv(os.path.join(DATA,"rooms.csv"))
        self.slots=load_csv(os.path.join(DATA,"time_slots.csv"))
        self.teachers={x["teacher_id"]:x["name"] for x in load_csv(os.path.join(DATA,"teachers.csv"))}
        self.con=initialize_database(os.path.join(BASE,"timetable.db")); self.rows=[]
        top=ttk.Frame(root,padding=12); top.pack(fill="x")
        ttk.Label(top,text="Smart Timetable Generator",font=("Segoe UI",20,"bold")).pack(anchor="w")
        ttk.Label(top,text="Genetic Algorithm • SQLite • Excel/PDF Export").pack(anchor="w")
        bar=ttk.Frame(root,padding=12); bar.pack(fill="x")
        ttk.Label(bar,text="Population").pack(side="left"); self.pop=tk.IntVar(value=80); ttk.Entry(bar,textvariable=self.pop,width=7).pack(side="left",padx=5)
        ttk.Label(bar,text="Generations").pack(side="left"); self.gen=tk.IntVar(value=150); ttk.Entry(bar,textvariable=self.gen,width=7).pack(side="left",padx=5)
        ttk.Button(bar,text="Generate Timetable",command=self.generate).pack(side="left",padx=8)
        ttk.Button(bar,text="Export Excel",command=self.excel).pack(side="left",padx=3)
        ttk.Button(bar,text="Export PDF",command=self.pdf).pack(side="left",padx=3)
        self.status=tk.StringVar(value="Ready"); ttk.Label(bar,textvariable=self.status).pack(side="left",padx=12)
        cols=("id","course","teacher","day","time","room"); self.tree=ttk.Treeview(root,columns=cols,show="headings",height=15)
        for c,h in zip(cols,["Course ID","Course","Teacher","Day","Time","Room"]): self.tree.heading(c,text=h); self.tree.column(c,width=150)
        self.tree.pack(fill="x",padx=12)
        self.fig=Figure(figsize=(8,3)); self.ax=self.fig.add_subplot(111); self.canvas=FigureCanvasTkAgg(self.fig,root); self.canvas.get_tk_widget().pack(fill="both",expand=True,padx=12,pady=8)
    def generate(self):
        try:
            ga=TimetableGA(self.courses,self.slots,self.rooms,self.pop.get(),self.gen.get())
            best,fit=ga.evolve(); sm={s["slot_id"]:s for s in self.slots}; rm={r["room_id"]:r["room_name"] for r in self.rooms}
            self.rows=[]
            for g in best:
                c=next(x for x in self.courses if x["course_id"]==g.course_id); s=sm[g.slot_id]
                self.rows.append({"course_id":c["course_id"],"course_name":c["course_name"],"teacher":self.teachers[c["teacher_id"]],"day":s["day"],"time":s["time"],"room":rm[g.room_id]})
            save_schedule(self.con,self.rows,fit)
            for x in self.tree.get_children(): self.tree.delete(x)
            for r in self.rows: self.tree.insert("", "end", values=(r["course_id"],r["course_name"],r["teacher"],r["day"],r["time"],r["room"]))
            self.ax.clear(); self.ax.plot(ga.best_history,label="Best"); self.ax.plot(ga.avg_history,label="Average"); self.ax.set_title(f"Fitness Progress — Final: {fit:.3f}"); self.ax.set_xlabel("Generation"); self.ax.set_ylabel("Fitness"); self.ax.legend(); self.ax.grid(alpha=.25); self.fig.tight_layout(); self.canvas.draw()
            self.fig.savefig(os.path.join(BASE,"results","fitness_progress.png"),dpi=150); self.status.set(f"Generated • Fitness {fit:.3f}")
        except Exception as e: messagebox.showerror("Error",str(e))
    def excel(self):
        if not self.rows: return messagebox.showinfo("Export","Generate a timetable first.")
        p=filedialog.asksaveasfilename(defaultextension=".xlsx",filetypes=[("Excel","*.xlsx")])
        if p: export_excel(self.rows,p); messagebox.showinfo("Export","Excel exported.")
    def pdf(self):
        if not self.rows: return messagebox.showinfo("Export","Generate a timetable first.")
        p=filedialog.asksaveasfilename(defaultextension=".pdf",filetypes=[("PDF","*.pdf")])
        if p: export_pdf(self.rows,p); messagebox.showinfo("Export","PDF exported.")
if __name__=="__main__":
    root=tk.Tk(); App(root); root.mainloop()
