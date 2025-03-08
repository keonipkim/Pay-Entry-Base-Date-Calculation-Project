import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime, timedelta
from tkinter import messagebox

def calculate_inclusive_days(start_date, end_date):
    try:
        d1 = datetime.strptime(start_date, '%Y-%m-%d')
        d2 = datetime.strptime(end_date, '%Y-%m-%d')
        raw_days = (d2 - d1).days
        inclusive_days = raw_days + 1
        return inclusive_days
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")

def subtract_days_from_date(reference_date, days_to_subtract):
    ref_date = datetime.strptime(reference_date, '%Y-%m-%d')
    result_date = ref_date - timedelta(days=days_to_subtract)
    return result_date.strftime('%Y-%m-%d')

def add_days_to_date(reference_date, days_to_add):
    ref_date = datetime.strptime(reference_date, '%Y-%m-%d')
    result_date = ref_date + timedelta(days=days_to_add)
    return result_date.strftime('%Y-%m-%d')

def total_days_to_ymd(total_days):
    years = total_days // 365
    remaining_days = total_days % 365
    months = remaining_days // 30
    days = remaining_days % 30
    if months >= 12:
        years += months // 12
        months %= 12
    return f"{years:02d} Years, {months:02d} Months, {days:02d} Days"

class BASDCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BASD Calculator - DoDFMR May 2024")
        self.dep_entries = []  # (start_entry, end_entry, idt_var)
        self.active_entries = []  # (start_entry, end_entry)
        self.inactive_entries = []  # (start_entry, end_entry, points_entry)
        self.lost_entries = []
        
        self.entry_doeaf = tk.Entry(root)
        self.entry_reenlist = tk.Entry(root)
        self.result_text = scrolledtext.ScrolledText(root, width=100, height=20, wrap=tk.WORD, font=("Courier", 10))
        self.result_text.insert(tk.END, "Result will appear here")
        self.result_text.config(state='disabled')
        
        self.add_dep_period()
        self.add_active_period()
        self.add_inactive_period()
        self.add_lost_period()
        self.refresh_layout()

    def refresh_layout(self):
        for widget in self.root.winfo_children():
            widget.grid_forget()
        
        row = 0
        tk.Label(self.root, text="DOEAF (YYYY-MM-DD):").grid(row=row, column=0, padx=5, pady=5)
        self.entry_doeaf.grid(row=row, column=1, padx=5, pady=5)
        tk.Label(self.root, text="Reenlistment Date (YYYY-MM-DD):").grid(row=row, column=2, padx=5, pady=5)
        self.entry_reenlist.grid(row=row, column=3, padx=5, pady=5)
        row += 1

        tk.Label(self.root, text="DEP Periods (Check IDT if applicable):").grid(row=row, column=0, columnspan=6, pady=5)
        row += 1
        tk.Label(self.root, text="Start").grid(row=row, column=0, padx=5, pady=2)
        tk.Label(self.root, text="End").grid(row=row, column=1, padx=5, pady=2)
        tk.Label(self.root, text="IDT Performed").grid(row=row, column=2, padx=5, pady=2)
        row += 1
        for i, (start_entry, end_entry, idt_var) in enumerate(self.dep_entries):
            start_entry.grid(row=row+i, column=0, padx=5, pady=2)
            end_entry.grid(row=row+i, column=1, padx=5, pady=2)
            tk.Checkbutton(self.root, text="IDT", variable=idt_var).grid(row=row+i, column=2, padx=5, pady=2)
        row += len(self.dep_entries)
        tk.Button(self.root, text="Add DEP Period", command=self.add_dep_period).grid(row=row, column=0, columnspan=6, pady=5)
        row += 1

        tk.Label(self.root, text="Active Duty Periods:").grid(row=row, column=0, columnspan=6, pady=5)
        row += 1
        tk.Label(self.root, text="Start").grid(row=row, column=0, padx=5, pady=2)
        tk.Label(self.root, text="End").grid(row=row, column=1, padx=5, pady=2)
        row += 1
        for i, (start_entry, end_entry) in enumerate(self.active_entries):
            start_entry.grid(row=row+i, column=0, padx=5, pady=2)
            end_entry.grid(row=row+i, column=1, padx=5, pady=2)
        row += len(self.active_entries)
        tk.Button(self.root, text="Add Active Period", command=self.add_active_period).grid(row=row, column=0, columnspan=6, pady=5)
        row += 1

        tk.Label(self.root, text="Inactive Periods (Enter Active Duty Points):").grid(row=row, column=0, columnspan=6, pady=5)
        row += 1
        tk.Label(self.root, text="Start").grid(row=row, column=0, padx=5, pady=2)
        tk.Label(self.root, text="End").grid(row=row, column=1, padx=5, pady=2)
        tk.Label(self.root, text="Points").grid(row=row, column=2, padx=5, pady=2)
        row += 1
        for i, (start_entry, end_entry, points_entry) in enumerate(self.inactive_entries):
            start_entry.grid(row=row+i, column=0, padx=5, pady=2)
            end_entry.grid(row=row+i, column=1, padx=5, pady=2)
            points_entry.grid(row=row+i, column=2, padx=5, pady=2)
        row += len(self.inactive_entries)
        tk.Button(self.root, text="Add Inactive Period", command=self.add_inactive_period).grid(row=row, column=0, columnspan=6, pady=5)
        row += 1

        tk.Label(self.root, text="Lost Time Periods (Subtracted):").grid(row=row, column=0, columnspan=6, pady=5)
        row += 1
        tk.Label(self.root, text="Start").grid(row=row, column=0, padx=5, pady=2)
        tk.Label(self.root, text="End").grid(row=row, column=1, padx=5, pady=2)
        row += 1
        for i, (start_entry, end_entry) in enumerate(self.lost_entries):
            start_entry.grid(row=row+i, column=0, padx=5, pady=2)
            end_entry.grid(row=row+i, column=1, padx=5, pady=2)
        row += len(self.lost_entries)
        tk.Button(self.root, text="Add Lost Time Period", command=self.add_lost_period).grid(row=row, column=0, columnspan=6, pady=5)
        row += 1

        tk.Button(self.root, text="Calculate", command=self.calculate).grid(row=row, column=0, columnspan=3, pady=10)
        tk.Button(self.root, text="Reset", command=self.reset).grid(row=row, column=3, columnspan=3, pady=10)
        row += 1

        self.result_text.grid(row=row, column=0, columnspan=6, padx=5, pady=5)

    def add_dep_period(self):
        start_entry = tk.Entry(self.root)
        end_entry = tk.Entry(self.root)
        idt_var = tk.IntVar()
        self.dep_entries.append((start_entry, end_entry, idt_var))
        self.refresh_layout()

    def add_active_period(self):
        start_entry = tk.Entry(self.root)
        end_entry = tk.Entry(self.root)
        self.active_entries.append((start_entry, end_entry))
        self.refresh_layout()

    def add_inactive_period(self):
        start_entry = tk.Entry(self.root)
        end_entry = tk.Entry(self.root)
        points_entry = tk.Entry(self.root)
        self.inactive_entries.append((start_entry, end_entry, points_entry))
        self.refresh_layout()

    def add_lost_period(self):
        start_entry = tk.Entry(self.root)
        end_entry = tk.Entry(self.root)
        self.lost_entries.append((start_entry, end_entry))
        self.refresh_layout()

    def reset(self):
        self.entry_doeaf.delete(0, tk.END)
        self.entry_reenlist.delete(0, tk.END)
        
        for start_entry, end_entry, idt_var in self.dep_entries:
            start_entry.destroy()
            end_entry.destroy()
        for start_entry, end_entry in self.active_entries + self.lost_entries:
            start_entry.destroy()
            end_entry.destroy()
        for start_entry, end_entry, points_entry in self.inactive_entries:
            start_entry.destroy()
            end_entry.destroy()
            points_entry.destroy()
        
        self.dep_entries.clear()
        self.active_entries.clear()
        self.inactive_entries.clear()
        self.lost_entries.clear()
        
        self.add_dep_period()
        self.add_active_period()
        self.add_inactive_period()
        self.add_lost_period()
        
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Result will appear here")
        self.result_text.config(state='disabled')
        self.refresh_layout()

    def calculate(self):
        try:
            doeaf = self.entry_doeaf.get().strip()
            reenlist_date = self.entry_reenlist.get().strip()
            
            if not all([doeaf, reenlist_date]):
                raise ValueError("All main date fields (DOEAF, Reenlistment Date) are required")
            
            doeaf_dt = datetime.strptime(doeaf, '%Y-%m-%d')
            reenlist_dt = datetime.strptime(reenlist_date, '%Y-%m-%d')
            
            if reenlist_dt < doeaf_dt:
                raise ValueError("Reenlistment Date cannot be before DOEAF")
            
            active_periods = []
            inactive_periods = []
            dep_periods = []
            lost_periods = []
            dep_active_days = 0
            inactive_points_days = 0
            
            # DEP Periods
            for start_entry, end_entry, idt_var in self.dep_entries:
                dep_start = start_entry.get().strip()
                dep_end = end_entry.get().strip()
                if dep_start and dep_end:
                    start_dt = datetime.strptime(dep_start, '%Y-%m-%d')
                    end_dt = datetime.strptime(dep_end, '%Y-%m-%d')
                    idt_performed = idt_var.get() == 1
                    dep_periods.append((dep_start, dep_end, idt_performed))
                    if start_dt < datetime(1985, 1, 1):
                        dep_active_days += calculate_inclusive_days(dep_start, dep_end)
            dep_status = [(start, end, "CREDITABLE (Pre-1985)" if datetime.strptime(start, '%Y-%m-%d') < datetime(1985, 1, 1) else "NOT CREDITABLE (Post-1989)") for start, end, _ in dep_periods]

            # Active Periods
            for start_entry, end_entry in self.active_entries:
                active_start = start_entry.get().strip()
                active_end = end_entry.get().strip()
                if active_start:
                    datetime.strptime(active_start, '%Y-%m-%d')
                    if active_end:
                        datetime.strptime(active_end, '%Y-%m-%d')
                        active_periods.append((active_start, active_end))
                    else:
                        active_periods.append((active_start, None))

            # Inactive Periods
            for start_entry, end_entry, points_entry in self.inactive_entries:
                inactive_start = start_entry.get().strip()
                inactive_end = end_entry.get().strip()
                points = points_entry.get().strip()
                if inactive_start and inactive_end and points:
                    datetime.strptime(inactive_start, '%Y-%m-%d')
                    datetime.strptime(inactive_end, '%Y-%m-%d')
                    points_days = int(points)
                    if points_days < 0:
                        raise ValueError("Active Duty Points cannot be negative")
                    period_days = calculate_inclusive_days(inactive_start, inactive_end)
                    if points_days > period_days:
                        raise ValueError(f"Points ({points_days}) exceed period duration ({period_days} days) for inactive period {inactive_start} to {inactive_end}")
                    inactive_periods.append((inactive_start, inactive_end, points_days))
                    inactive_points_days += points_days

            # Lost Periods
            for start_entry, end_entry in self.lost_entries:
                lost_start = start_entry.get().strip()
                lost_end = end_entry.get().strip()
                if lost_start and lost_end:
                    datetime.strptime(lost_start, '%Y-%m-%d')
                    datetime.strptime(lost_end, '%Y-%m-%d')
                    lost_periods.append((lost_start, lost_end))

            total_active_days = 0
            for start, end in active_periods:
                if end:
                    total_active_days += calculate_inclusive_days(start, end)
            
            total_lost_days = sum(calculate_inclusive_days(start, end) for start, end in lost_periods) if lost_periods else 0
            net_active_days = total_active_days + dep_active_days + inactive_points_days - total_lost_days

            # BASD Calculation - Always use reenlistment date as base
            most_recent_active_start = reenlist_date
            basd = subtract_days_from_date(most_recent_active_start, net_active_days)
            basd_note = f"BASD calculated as reenlistment date ({most_recent_active_start}) minus total creditable service ({net_active_days} days)."
            if total_lost_days > 0:
                basd_dt = datetime.strptime(basd, '%Y-%m-%d')
                basd_dt += timedelta(days=total_lost_days)
                basd = basd_dt.strftime('%Y-%m-%d')
                basd_note += f" Adjusted forward by {total_lost_days} days for lost time per 2.4.1.4."

            active_status = [(start, end if end else "Ongoing", "CREDITABLE") for start, end in active_periods]
            inactive_status = [(start, end, points, "CREDITABLE (Points)") for start, end, points in inactive_periods]
            lost_status = [(start, end, "NOT CREDITABLE") for start, end in lost_periods]
            
            # Result Output - Removed EOS-related lines
            result_text_content = (
                f"{'Field':<25} | {'Value':<20}\n"
                f"{'-'*25} | {'-'*20}\n"
                f"{'DOEAF':<25} | {doeaf:<20}\n"
                f"{'Reenlistment Date':<25} | {reenlist_date:<20}\n"
                f"{'Total Creditable Service':<25} | {total_days_to_ymd(net_active_days):<20}\n"
                f"{'Base Date for BASD':<25} | {most_recent_active_start:<20}\n"
                f"{'Basic Active Service Date':<25} | {basd:<20}\n\n"
                f"{'DEP Periods':<25} | {'Start':<15} | {'End':<15} | {'Status':<25}\n"
                f"{'-'*25} | {'-'*15} | {'-'*15} | {'-'*25}\n"
            )
            for start, end, status in dep_status:
                result_text_content += f"{'':<25} | {start:<15} | {end:<15} | {status:<25}\n"
            
            result_text_content += (
                f"\n{'Active Duty Periods':<25} | {'Start':<15} | {'End':<15} | {'Status':<25}\n"
                f"{'-'*25} | {'-'*15} | {'-'*15} | {'-'*25}\n"
            )
            for i, (start, end, status) in enumerate(active_status, 1):
                result_text_content += f"{'Active Period ' + str(i):<25} | {start:<15} | {end:<15} | {status:<25}\n"
            
            result_text_content += (
                f"\n{'Inactive Periods':<25} | {'Start':<15} | {'End':<15} | {'Points':<10} | {'Status':<25}\n"
                f"{'-'*25} | {'-'*15} | {'-'*15} | {'-'*10} | {'-'*25}\n"
            )
            for i, (start, end, points, status) in enumerate(inactive_status, 1):
                result_text_content += f"{'Inactive Period ' + str(i):<25} | {start:<15} | {end:<15} | {str(points):<10} | {status:<25}\n"
            
            result_text_content += (
                f"\n{'Lost Time Periods':<25} | {'Start':<15} | {'End':<15} | {'Status':<25}\n"
                f"{'-'*25} | {'-'*15} | {'-'*15} | {'-'*25}\n"
            )
            for start, end, status in lost_status:
                result_text_content += f"{'':<25} | {start:<15} | {end:<15} | {status:<25}\n"
            
            result_text_content += (
                f"\n\nNote: {basd_note} BASD reflects total creditable service (active periods + points) subtracted from reenlistment date."
            )

            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result_text_content)
            self.result_text.config(state='disabled')
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}. Use 'YYYY-MM-DD' for dates or valid points.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BASDCalculator(root)
    root.mainloop()