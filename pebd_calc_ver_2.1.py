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

class PayDateCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("PEBD Calculator - Creditable Service for Pay (DoDFMR May 2024)")
        self.dep_entries = []  # (start_entry, end_entry, idt_var)
        self.active_entries = []
        self.inactive_entries = []
        self.lost_entries = []
        
        self.entry_doeaf = tk.Entry(root)
        self.entry_reenlist = tk.Entry(root)
        self.entry_eos = tk.Entry(root)
        self.entry_constructive = tk.Entry(root)
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
        tk.Label(self.root, text="EOS (YYYY-MM-DD):").grid(row=row, column=4, padx=5, pady=5)
        self.entry_eos.grid(row=row, column=5, padx=5, pady=5)
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

        tk.Label(self.root, text="Inactive Duty Periods:").grid(row=row, column=0, columnspan=6, pady=5)
        row += 1
        tk.Label(self.root, text="Start").grid(row=row, column=0, padx=5, pady=2)
        tk.Label(self.root, text="End").grid(row=row, column=1, padx=5, pady=2)
        row += 1
        for i, (start_entry, end_entry) in enumerate(self.inactive_entries):
            start_entry.grid(row=row+i, column=0, padx=5, pady=2)
            end_entry.grid(row=row+i, column=1, padx=5, pady=2)
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

        tk.Label(self.root, text="Constructive Service Years:").grid(row=row, column=0, padx=5, pady=5)
        self.entry_constructive.grid(row=row, column=1, padx=5, pady=5)
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
        self.inactive_entries.append((start_entry, end_entry))
        self.refresh_layout()

    def add_lost_period(self):
        start_entry = tk.Entry(self.root)
        end_entry = tk.Entry(self.root)
        self.lost_entries.append((start_entry, end_entry))
        self.refresh_layout()

    def reset(self):
        self.entry_doeaf.delete(0, tk.END)
        self.entry_reenlist.delete(0, tk.END)
        self.entry_eos.delete(0, tk.END)
        self.entry_constructive.delete(0, tk.END)
        
        for start_entry, end_entry, idt_var in self.dep_entries:
            start_entry.destroy()
            end_entry.destroy()
        for start_entry, end_entry in self.active_entries + self.inactive_entries + self.lost_entries:
            start_entry.destroy()
            end_entry.destroy()
        
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
            eos = self.entry_eos.get().strip()
            reenlist_date = self.entry_reenlist.get().strip()
            
            if not all([doeaf, reenlist_date, eos]):
                raise ValueError("All main date fields (DOEAF, Reenlistment Date, EOS) are required")
            
            doeaf_dt = datetime.strptime(doeaf, '%Y-%m-%d')
            reenlist_dt = datetime.strptime(reenlist_date, '%Y-%m-%d')
            eos_dt = datetime.strptime(eos, '%Y-%m-%d')
            
            if reenlist_dt < doeaf_dt:
                raise ValueError("Reenlistment Date cannot be before DOEAF")
            
            active_periods = []
            inactive_periods = []
            dep_periods = []
            lost_periods = []
            constructive_years = 0
            dep_creditable_days = 0
            
            # DEP Periods - Check IDT or pre-1985
            for start_entry, end_entry, idt_var in self.dep_entries:
                dep_start = start_entry.get().strip()
                dep_end = end_entry.get().strip()
                if dep_start and dep_end:
                    start_dt = datetime.strptime(dep_start, '%Y-%m-%d')
                    end_dt = datetime.strptime(dep_end, '%Y-%m-%d')
                    idt_performed = idt_var.get() == 1
                    dep_periods.append((dep_start, dep_end, idt_performed))
                    if start_dt < datetime(1985, 1, 1) or (start_dt >= datetime(1989, 11, 29) and idt_performed):
                        dep_creditable_days += calculate_inclusive_days(dep_start, dep_end)
            dep_status = [(start, end, "CREDITABLE (Pre-1985 or IDT)" if (datetime.strptime(start, '%Y-%m-%d') < datetime(1985, 1, 1) or idt) else "NOT CREDITABLE") for start, end, idt in dep_periods]

            # Active Periods
            for start_entry, end_entry in self.active_entries:
                active_start = start_entry.get().strip()
                active_end = end_entry.get().strip()
                if active_start and active_end:
                    datetime.strptime(active_start, '%Y-%m-%d')
                    datetime.strptime(active_end, '%Y-%m-%d')
                    active_periods.append((active_start, active_end))

            # Inactive Periods
            for start_entry, end_entry in self.inactive_entries:
                inactive_start = start_entry.get().strip()
                inactive_end = end_entry.get().strip()
                if inactive_start and inactive_end:
                    datetime.strptime(inactive_start, '%Y-%m-%d')
                    datetime.strptime(inactive_end, '%Y-%m-%d')
                    inactive_periods.append((inactive_start, inactive_end))

            # Lost Periods
            for start_entry, end_entry in self.lost_entries:
                lost_start = start_entry.get().strip()
                lost_end = end_entry.get().strip()
                if lost_start and lost_end:
                    datetime.strptime(lost_start, '%Y-%m-%d')
                    datetime.strptime(lost_end, '%Y-%m-%d')
                    lost_periods.append((lost_start, lost_end))

            # Constructive Service
            if self.entry_constructive.get().strip():
                constructive_years = int(self.entry_constructive.get())
                if constructive_years < 0:
                    raise ValueError("Constructive Service Years cannot be negative")
            constructive_days = constructive_years * 365

            total_active_days = sum(calculate_inclusive_days(start, end) for start, end in active_periods) if active_periods else 0
            total_inactive_days = sum(calculate_inclusive_days(start, end) for start, end in inactive_periods) if inactive_periods else 0
            total_lost_days = sum(calculate_inclusive_days(start, end) for start, end in lost_periods) if lost_periods else 0
            
            net_service_days = total_active_days + total_inactive_days + dep_creditable_days - total_lost_days + constructive_days

            # PEBD Calculation
            all_periods = [(start, end) for start, end, _ in dep_periods if datetime.strptime(start, '%Y-%m-%d') < datetime(1985, 1, 1) or _] + active_periods + inactive_periods
            sorted_periods = sorted(all_periods, key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'))
            
            has_break = False
            if sorted_periods:
                for i in range(1, len(sorted_periods)):
                    prev_end = datetime.strptime(sorted_periods[i-1][1], '%Y-%m-%d')
                    curr_start = datetime.strptime(sorted_periods[i][0], '%Y-%m-%d')
                    if (curr_start - prev_end).days > 90:
                        has_break = True
                        break
                last_end = datetime.strptime(sorted_periods[-1][1], '%Y-%m-%d')
                if (reenlist_dt - last_end).days > 90:
                    has_break = True

            if not has_break and sorted_periods:
                pebd = sorted_periods[0][0]
                pebd_note = "No break in creditable service (gap ≤ 90 days): PEBD set to earliest period start."
            elif has_break and sorted_periods:
                pebd = subtract_days_from_date(reenlist_date, net_service_days)
                pebd_note = f"Break > 90 days detected: PEBD calculated from reenlistment date ({reenlist_date}) minus total creditable service days ({net_service_days})."
            else:
                pebd = reenlist_date
                pebd_note = "No creditable periods: PEBD set to reenlistment date."

            # Lost Time adjustment for enlisted
            if total_lost_days > 0 and not inactive_periods:  # Simplified enlisted check
                pebd_dt = datetime.strptime(pebd, '%Y-%m-%d')
                pebd_dt += timedelta(days=total_lost_days)
                pebd = pebd_dt.strftime('%Y-%m-%d')
                pebd_note += f" Adjusted forward by {total_lost_days} days for lost time per 2.4.1.4."

            active_status = [(start, end, "CREDITABLE") for start, end in active_periods]
            inactive_status = [(start, end, "CREDITABLE") for start, end in inactive_periods]
            lost_status = [(start, end, "NOT CREDITABLE") for start, end in lost_periods]
            
            # MSO and New EOS (kept for completeness, not PEBD-related)
            mso_cutoff = datetime(1984, 6, 1)
            expected_mso_years = 6 if doeaf_dt < mso_cutoff else 8
            expected_mso_days = expected_mso_years * 365 + (expected_mso_years // 4)
            expected_eos = add_days_to_date(doeaf, expected_mso_days)
            break_in_service = eos_dt < datetime.strptime(expected_eos, '%Y-%m-%d')

            if break_in_service:
                remaining_mso_days = (datetime.strptime(expected_eos, '%Y-%m-%d') - eos_dt).days
                new_eos = add_days_to_date(reenlist_date, remaining_mso_days)
                offset_note = f"Expected {expected_mso_years}-year MSO ends {expected_eos}. EOS {eos} indicates a break in service. New EOS {new_eos} fulfills remaining MSO."
            else:
                new_eos = expected_eos if eos_dt > datetime.strptime(expected_eos, '%Y-%m-%d') else eos
                offset_note = f"Expected {expected_mso_years}-year MSO ends {expected_eos}. No break in service detected."

            # Result Output
            result_text_content = (
                f"{'Field':<25} | {'Value':<20}\n"
                f"{'-'*25} | {'-'*20}\n"
                f"{'DOEAF':<25} | {doeaf:<20}\n"
                f"{'Reenlistment Date':<25} | {reenlist_date:<20}\n"
                f"{'Total Creditable Service':<25} | {total_days_to_ymd(net_service_days):<20}\n"
                f"{'Pay Entry Base Date':<25} | {pebd:<20}\n"
                f"{'EOS':<25} | {eos:<20}\n"
                f"{'New EOS':<25} | {new_eos:<20}\n\n"
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
                f"\n{'Inactive Duty Periods':<25} | {'Start':<15} | {'End':<15} | {'Status':<25}\n"
                f"{'-'*25} | {'-'*15} | {'-'*15} | {'-'*25}\n"
            )
            for i, (start, end, status) in enumerate(inactive_status, 1):
                result_text_content += f"{'Inactive Period ' + str(i):<25} | {start:<15} | {end:<15} | {status:<25}\n"
            
            result_text_content += (
                f"\n{'Lost Time Periods':<25} | {'Start':<15} | {'End':<15} | {'Status':<25}\n"
                f"{'-'*25} | {'-'*15} | {'-'*15} | {'-'*25}\n"
            )
            for start, end, status in lost_status:
                result_text_content += f"{'':<25} | {start:<15} | {end:<15} | {status:<25}\n"
            
            result_text_content += (
                f"\n\nNote: {offset_note}\n"
                f"Note: {pebd_note} DEP creditable pre-1985 or with IDT post-1989 per 2.1.4.12. This calculates PEBD for pay longevity per DoDFMR 2.1."
            )
            if eos_dt < reenlist_dt:
                result_text_content += f"\nWarning: EOS ({eos}) is before Reenlistment Date ({reenlist_date}), which may indicate an error."

            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result_text_content)
            self.result_text.config(state='disabled')
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}. Use 'YYYY-MM-DD' for dates.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PayDateCalculator(root)
    root.mainloop()