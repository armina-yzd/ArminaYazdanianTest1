import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ChecklistApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Checklist App")
        self.geometry("600x600")
        self.configure(bg="#f0f8ff")
        
        self.tasks = {}
        
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f0f8ff")
        style.configure("Custom.TButton", font=("Arial", 10, "bold"), padding=6)
        style.configure("Title.TLabel", font=("Arial", 16, "bold"), background="#f0f8ff", foreground="#2c3e50")
        
        header_frame = ttk.Frame(self, style="Custom.TFrame", padding=15)
        header_frame.pack(fill="x")
        
        title_label = ttk.Label(header_frame, text="My Checklist", style="Title.TLabel")
        title_label.pack()
        
        input_frame = ttk.Frame(self, style="Custom.TFrame", padding=15)
        input_frame.pack(fill="x", padx=20)
        
        self.entry_task = ttk.Entry(input_frame, font=("Arial", 12), width=30)
        self.entry_task.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_task.bind("<Return>", lambda e: self.add_task())
        
        add_btn = ttk.Button(input_frame, text="➕ Add Task", command=self.add_task, style="Custom.TButton")
        add_btn.pack(side="left")
        
        self.tasks_frame = ttk.Frame(self, style="Custom.TFrame", padding=15)
        self.tasks_frame.pack(fill="both", expand=True, padx=20)
        
        button_frame = ttk.Frame(self, style="Custom.TFrame", padding=15)
        button_frame.pack(fill="x", pady=10, padx=20)
        
        self.btn_done = tk.Button(button_frame, text="✅ Mark Done", command=self.mark_done, 
                                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"), 
                                 width=12, height=1, bd=0, relief="flat", cursor="hand2")
        self.btn_done.pack(side="left", padx=5)
        
        self.btn_delete = tk.Button(button_frame, text="🗑️ Delete", command=self.delete_selected, 
                                   bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), 
                                   width=10, height=1, bd=0, relief="flat", cursor="hand2")
        self.btn_delete.pack(side="left", padx=5)
        
        self.btn_clear = tk.Button(button_frame, text="🧹 Clear All", command=self.clear_all, 
                                  bg="#95a5a6", fg="white", font=("Arial", 10, "bold"), 
                                  width=10, height=1, bd=0, relief="flat", cursor="hand2")
        self.btn_clear.pack(side="right", padx=5)

    def add_task(self):
        task_text = self.entry_task.get().strip()
        if not task_text:
            messagebox.showwarning("Input Required", "Please enter a task description!")
            return
        
        self.entry_task.delete(0, tk.END)
        
        task_frame = ttk.Frame(self.tasks_frame, relief="solid", borderwidth=1)
        task_frame.pack(fill="x", pady=3, padx=5)
        
        var = tk.BooleanVar()
        check_btn = ttk.Checkbutton(task_frame, variable=var)
        check_btn.pack(side="left", padx=8)
        
        task_label = ttk.Label(task_frame, text=task_text, font=("Arial", 11), 
                              background="white", width=35, anchor="w")
        task_label.pack(side="left", fill="x", expand=True, padx=5, pady=8)
        
        datetime_label = ttk.Label(task_frame, text="", foreground="#7f8c8d", 
                                  font=("Arial", 7))
        datetime_label.pack(side="right", padx=5)
        
        status_label = ttk.Label(task_frame, text="⏳ Pending", foreground="#e67e22", 
                                font=("Arial", 9, "bold"))
        status_label.pack(side="right", padx=8)
        
        def toggle_task(event=None):
            if not self.tasks[task_frame]["done"]:
                var.set(not var.get())
        
        task_frame.bind("<Button-1>", toggle_task)
        task_label.bind("<Button-1>", toggle_task)
        status_label.bind("<Button-1>", toggle_task)
        datetime_label.bind("<Button-1>", toggle_task)
        
        self.tasks[task_frame] = {
            "text": task_text, 
            "done": False, 
            "var": var, 
            "label": task_label, 
            "status": status_label,
            "datetime": datetime_label
        }

    def mark_done(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        any_marked = False
        
        for task_frame, info in self.tasks.items():
            if info["var"].get() and not info["done"]:
                info["done"] = True
                info["label"].config(foreground="#7f8c8d")
                info["status"].config(text="✅ Done", foreground="#27ae60")
                info["datetime"].config(text=f"{now}")
                info["var"].set(False)
                task_frame.config(relief="flat", background="#d5f5e3")
                any_marked = True
        
        if not any_marked:
            messagebox.showinfo("No Selection", "Please select tasks to mark as done!")

    def delete_selected(self):
        tasks_to_delete = []
        for task_frame, info in self.tasks.items():
            if info["var"].get():
                tasks_to_delete.append(task_frame)
        
        if not tasks_to_delete:
            messagebox.showinfo("No Selection", "Please select tasks to delete!")
            return
        
        for task_frame in tasks_to_delete:
            self._remove_task(task_frame)

    def _remove_task(self, task_frame):
        task_frame.destroy()
        del self.tasks[task_frame]

    def clear_all(self):
        if not self.tasks:
            messagebox.showinfo("Empty List", "Your checklist is already empty!")
            return
        
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to delete all tasks?"):
            for task_frame in list(self.tasks.keys()):
                self._remove_task(task_frame)

if __name__ == "__main__":
    app = ChecklistApp()
    app.mainloop()