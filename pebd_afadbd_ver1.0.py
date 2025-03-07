import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime, timedelta
from tkinter import messagebox

def calculate_inclusive_days(start_date, end_date):
    try:
        d1 = datetime.strptime(start_date, '%Y-%m-%d')
        d2 = datetime.strptime(end_date, '%Y-%m-%d')
        if d2.day == 31:
            d2 = d2.replace(day=30)
        elif d2.month == 2 and d2.day == 29 and not (d2.year % 4 == 0 and (d2.year % 100 != 0 or d2.year % 400 == 0)):
            d2 = d2.replace(day=28)
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
    years = total_days // 360
    remaining_days = total_days % 360
    months = remaining_days // 30
    days = remaining_days % 30
    if months >= 12:
        years += months // 12
        months %= 12
    return f"{years:02d} Years, {months:02d} Months, {days:02d} Days"

class PayDateCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("PEBD and AFADBD Calculator with Retirement Points")
        
        self.dep_entries = []
        self.active_entries = []
        self.inactive_entries = []
        self.lost_entries = []
        
        tk.Label(root, text="DOEAF (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_doeaf = tk.Entry(root)
        self.entry_doeaf.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(root, text="Reenlistment Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5)
        self.entry_reenlist = tk.Entry(root)
        self.entry_reenlist.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(root, text="EOS (YYYY-MM-DD):").grid(row=0, column=4, padx=5, pady=5)
        self.entry_eos = tk.Entry(root)
        self.entry_eos.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Label(root, text="DEP Periods (Not Included in Creditable Service):").grid(row=2, column=0, columnspan=6, pady=5)
        tk.Label(root, text="Start").grid(row=3, column=0, padx=5, pady=2)
        tk.Label(root, text="End").grid(row=3, column=1, padx=5, pady=2)
        self.add_dep_period(row=4)
        tk.Button(root, text="Add DEP Period", command=lambda: self.add_dep_period(row=4+len(self.dep_entries))).grid(row=5, column=0, columnspan=6, pady=5)
        
        tk.Label(root, text="Active Periods (Active Duty):").grid(row=6+len(self.dep_entries), column=0, columnspan=6, pady=5)
        tk.Label(root, text="Start").grid(row=7+len(self.dep_entries), column=0, padx=5, pady=2)
        tk.Label(root, text="End").grid(row=7+len(self.dep_entries), column=1, padx=5, pady=2)
        self.add_active_period(row=8+len(self.dep_entries))
        tk.Button(root, text="Add Active Period", command=lambda: self.add_active_period(row=8+len(self.dep_entries)+len(self.active_entries))).grid(row=9+len(self.dep_entries), column=0, columnspan=3, pady=5)
        
        tk.Label(root, text="Inactive Periods (Reserve Points):").grid(row=10+len(self.dep_entries)+len(self.active_entries), column=0, columnspan=6, pady=5)
        tk.Label(root, text="Start").grid(row=11+len(self.dep_entries)+len(self.active_entries), column=0, padx=5, pady=2)
        tk.Label(root, text="End").grid(row=11+len(self.dep_entries)+len(self.active_entries), column=1, padx=5, pady=2)
        self.add_inactive_period(row=12+len(self.dep_entries)+len(self.active_entries))
        tk.Button(root, text="Add Inactive Period", command=lambda: self.add_inactive_period(row=12+len(self.dep_entries)+len(self.active_entries)+len(self.inactive_entries))).grid(row=13+len(self.dep_entries)+len(self.active_entries), column=0, columnspan=6, pady=5)
        
        tk.Label(root, text="Lost Time Periods (Subtracted from Creditable Service):").grid(row=14+len(self.dep_entries)+len(self.active_entries)+len(self.inactive_entries), column=0, columnspan=6, pady=5)
        tk.Label(root, text="Start").grid(row=15+len(self.dep_entries)+len(self.active_entries)+len(self.inactive_entries), column=0, padx=5, pady=2)
        tk.Label(root, text="End").grid(row=15+len(self.dep_entries)+len(self.active_entries)+len(self.inactive_entries), column=1, padx=5, pady=2)
        self.add_lost_period(row=16+len(self.dep_entries)+len(self.active_entries)+len(self.inactive_entries))
        tk.Button(root, text="Add Lost Time Period", command=lambda: self.add_lost_period(row=16+len(self.dep_entries)+len(self.active_entries)+len(self.inactive_entries)+len(self.lost_entries))).grid(row=17+len(self.dep_entries)+len(self.active_entries)+len(self.inactive_entries), column=0, columnspan=6, pady=5)
        
        tk.Label(root, text="Constructive Service Years:").grid(row=18+len(self.dep_entries)+len(self.active_entries)+len(self.inactive_entries)+len(self.lost_entries), column=0, padx=5, pady=5)
        self.entry_constructive = tk.Entry(root)
        self.entry_constructive.grid(row=18+len(self.dep_entries)+len(self.active_entries)+len(self.inactive_entries)+len(self.lost_entries), column=1, padx=5, pady=5)
        
        tk.Button(root, text="Calculate", command=self.calculate).grid(row=19+len(self.dep_entries)+len(self.active_entries)+len(self.inactive_entries)+len(self.lost_entries), column=0, columnspan=3, pady=10)
        tk.Button(root, text="Reset", command=self.reset).grid(row=19+len(self.dep_entries)+len(self.active_entries)+len(self.inactive_entries)+len(self.lost_entries), column=3, columnspan=3, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(root, width=100, height=25, wrap=tk.WORD, font=("Courier", 10))
        self.result_text.grid(row=20+len(self.dep_entries)+len(self.active_entries)+len(self.inactive_entries)+len(self.lost_entries), column=0, columnspan=6, padx=5, pady=5)
        self.result_text.insert(tk.END, "Result will appear here")
        self.result_text.config(state='disabled')
    
    def add_dep_period(self, row):
        start_entry = tk.Entry(self.root)
        start_entry.grid(row=row, column=0, padx=5, pady=2)
        end_entry = tk.Entry(self.root)
        end_entry.grid(row=row, column=1, padx=5, pady=2)
        self.dep_entries.append((start_entry, end_entry))
    
    def add_active_period(self, row):
        start_entry = tk.Entry(self.root)
        start_entry.grid(row=row, column=0, padx=5, pady=2)
        end_entry = tk.Entry(self.root)
        end_entry.grid(row=row, column=1, padx=5, pady=2)
        self.active_entries.append((start_entry, end_entry))
    
    def add_inactive_period(self, row):
        start_entry = tk.Entry(self.root)
        start_entry.grid(row=row, column=0, padx=5, pady=2)
        end_entry = tk.Entry(self.root)
        end_entry.grid(row=row, column=1, padx=5, pady=2)
        self.inactive_entries.append((start_entry, end_entry))
    
    def add_lost_period(self, row):
        start_entry = tk.Entry(self.root)
        start_entry.grid(row=row, column=0, padx=5, pady=2)
        end_entry = tk.Entry(self.root)
        end_entry.grid(row=row, column=1, padx=5, pady=2)
        self.lost_entries.append((start_entry, end_entry))
    
    def reset(self):
        self.entry_doeaf.delete(0, tk.END)
        self.entry_reenlist.delete(0, tk.END)
        self.entry_eos.delete(0, tk.END)
        self.entry_constructive.delete(0, tk.END)
        
        for start_entry, end_entry in self.dep_entries:
            start_entry.destroy()
            end_entry.destroy()
        self.dep_entries.clear()
        self.add_dep_period(row=4)
        
        for start_entry, end_entry in self.active_entries:
            start_entry.destroy()
            end_entry.destroy()
        self.active_entries.clear()
        self.add_active_period(row=8)
        
        for start_entry, end_entry in self.inactive_entries:
            start_entry.destroy()
            end_entry.destroy()
        self.inactive_entries.clear()
        self.add_inactive_period(row=12+len(self.active_entries))
        
        for start_entry, end_entry in self.lost_entries:
            start_entry.destroy()
            end_entry.destroy()
        self.lost_entries.clear()
        self.add_lost_period(row=16+len(self.active_entries)+len(self.inactive_entries))
        
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Result will appear here")
        self.result_text.config(state='disabled')
    
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
            
            # AFADBD is Reenlistment Date
            afadbd = reenlist_date
            
            if reenlist_dt < doeaf_dt:
                raise ValueError("Reenlistment Date cannot be before DOEAF")
            
            active_periods = []
            inactive_periods = []
            dep_periods = []
            lost_periods = []
            constructive_years = 0
            
            for start_entry, end_entry in self.dep_entries:
                dep_start = start_entry.get().strip()
                dep_end = end_entry.get().strip()
                if dep_start and dep_end:
                    datetime.strptime(dep_start, '%Y-%m-%d')
                    datetime.strptime(dep_end, '%Y-%m-%d')
                    dep_periods.append((dep_start, dep_end))
            
            for start_entry, end_entry in self.active_entries:
                active_start = start_entry.get().strip()
                active_end = end_entry.get().strip()
                if active_start and active_end:
                    datetime.strptime(active_start, '%Y-%m-%d')
                    end_dt = datetime.strptime(active_end, '%Y-%m-%d')
                    effective_end = active_end if end_dt <= eos_dt else eos
                    active_periods.append((active_start, effective_end))
            
            for start_entry, end_entry in self.inactive_entries:
                inactive_start = start_entry.get().strip()
                inactive_end = end_entry.get().strip()
                if inactive_start and inactive_end:
                    datetime.strptime(inactive_start, '%Y-%m-%d')
                    end_dt = datetime.strptime(inactive_end, '%Y-%m-%d')
                    effective_end = inactive_end if end_dt <= eos_dt else eos
                    inactive_periods.append((inactive_start, effective_end))
            
            for start_entry, end_entry in self.lost_entries:
                lost_start = start_entry.get().strip()
                lost_end = end_entry.get().strip()
                if lost_start and lost_end:
                    datetime.strptime(lost_start, '%Y-%m-%d')
                    end_dt = datetime.strptime(lost_end, '%Y-%m-%d')
                    effective_end = lost_end if end_dt <= eos_dt else eos
                    lost_periods.append((lost_start, effective_end))
            
            if self.entry_constructive.get().strip():
                constructive_years = int(self.entry_constructive.get())
            
            dep_status = [(dep_start, dep_end, "NOT CREDITABLE") for dep_start, dep_end in dep_periods]
            for dep_start, dep_end in dep_periods:
                messagebox.showinfo("DEP Note", f"DEP {dep_start} to {dep_end} is NOT CREDITABLE (labeled as DEP).")

            total_active_days = sum(calculate_inclusive_days(start, end) for start, end in active_periods) if active_periods else 0
            total_inactive_days = sum(calculate_inclusive_days(start, end) for start, end in inactive_periods) if inactive_periods else 0
            total_lost_days = sum(calculate_inclusive_days(start, end) for start, end in lost_periods) if lost_periods else 0
            constructive_days = constructive_years * 360
            
            # Creditable service includes active and inactive
            net_service_days = total_active_days + total_inactive_days - total_lost_days + constructive_days
            
            # PEBD: Two paths based on Reenlistment Date vs EOS
            if reenlist_dt < eos_dt:
                pebd = min((start for start, _ in active_periods), default=reenlist_date) if active_periods else reenlist_date  # Earliest active start
            else:  # Reenlistment >= EOS
                pebd = subtract_days_from_date(reenlist_date, total_active_days + 1)  # Historical reenlistment
            
            # AFADBD is Reenlistment Date; Active Service Start aligned with PEBD when Reenlistment >= EOS
            active_service_start = pebd if reenlist_dt >= eos_dt else subtract_days_from_date(afadbd, total_active_days)
            
            # Retirement Points Calculation
            active_points = total_active_days  # Active periods: 1 point/day
            reserve_points_by_year = {}
            total_reserve_points = 0
            
            if inactive_periods:
                anniversary_date = doeaf  # Use DOEAF as anniversary start
                anniv_start = datetime.strptime(anniversary_date, '%Y-%m-%d')
                for start, end in inactive_periods:
                    start_dt = datetime.strptime(start, '%Y-%m-%d')
                    end_dt = datetime.strptime(end, '%Y-%m-%d')
                    # Start from the DOEAF anniversary year that precedes the inactive period
                    current = anniv_start
                    while current < end_dt:
                        next_anniv = anniv_start.replace(year=current.year + 1)
                        period_start = max(current, start_dt)
                        period_end = min(next_anniv, end_dt)
                        if period_start <= period_end:  # Only count if there's overlap
                            days = (period_end - period_start).days + 1
                            months = days / 30.44
                            drill_points = int(months * 1.85)  # ~1.85 drills/month
                            membership_points = int((days / 365.25) * 15)
                            total_for_year = drill_points + membership_points
                            year_key = f"{period_start.year}-{period_start.year+1}"
                            if total_for_year > 0:  # Only include non-zero points
                                reserve_points_by_year[year_key] = total_for_year
                                total_reserve_points += total_for_year
                        current = next_anniv
                        anniv_start = next_anniv
            
            total_retirement_points = active_points + total_reserve_points
            
            # Define status lists for output
            active_status = [(start, end, "CREDITABLE") for start, end in active_periods]
            inactive_status = [(start, end, "CREDITABLE") for start, end in inactive_periods]
            lost_status = [(start, end, "NOT CREDITABLE") for start, end in lost_periods]
            
            # MSO and New EOS Calculation
            mso_cutoff = datetime(1984, 6, 1)
            expected_mso_years = 6 if doeaf_dt < mso_cutoff else 8
            expected_eos = add_days_to_date(doeaf, expected_mso_years * 365 + (expected_mso_years // 4))
            break_in_service = eos_dt < datetime.strptime(expected_eos, '%Y-%m-%d')
            
            if break_in_service:
                remaining_mso_days = (datetime.strptime(expected_eos, '%Y-%m-%d') - eos_dt).days
                new_eos = add_days_to_date(reenlist_date, remaining_mso_days)
                offset_note = f"Expected {expected_mso_years}-year MSO ends {expected_eos}. EOS {eos} is earlier than expected, indicating a break in service. New EOS {new_eos} fulfills remaining MSO from Reenlistment Date ({reenlist_date})."
            else:
                new_eos = expected_eos if eos_dt > datetime.strptime(expected_eos, '%Y-%m-%d') else eos
                offset_note = f"Expected {expected_mso_years}-year MSO ends {expected_eos}. No break in service detected."
            
            result_text_content = (
                f"{'Field':<25} | {'Value':<20}\n"
                f"{'-'*25} | {'-'*20}\n"
                f"{'DOEAF':<25} | {doeaf:<20}\n"
                f"{'Reenlistment Date':<25} | {reenlist_date:<20}\n"
                f"{'Total Creditable Service':<25} | {total_days_to_ymd(net_service_days):<20}\n"
                f"{'Pay Entry Base Date':<25} | {pebd:<20}\n"
                f"{'AF Active Duty Base Date':<25} | {afadbd:<20}\n"
                f"{'Active Service Start':<25} | {active_service_start:<20}\n"
                f"{'EOS':<25} | {eos:<20}\n"
                f"{'New EOS':<25} | {new_eos:<20}\n\n"
                f"{'DEP Periods':<25} | {'Start':<15} | {'End':<15} | {'Status':<15}\n"
                f"{'-'*25} | {'-'*15} | {'-'*15} | {'-'*15}\n"
            )
            if dep_status:
                for start, end, status in dep_status:
                    result_text_content += f"{'':<25} | {start:<15} | {end:<15} | {status:<15}\n"
            else:
                result_text_content += f"{'':<25} | {'None':<15} | {'':<15} | {'':<15}\n"
            
            result_text_content += (
                f"\n{'Service Periods':<25} | {'Start':<15} | {'End':<15} | {'Status':<15}\n"
                f"{'-'*25} | {'-'*15} | {'-'*15} | {'-'*15}\n"
            )
            if active_status:
                for i, (start, end, status) in enumerate(active_status, 1):
                    result_text_content += f"{'Active Period ' + str(i):<25} | {start:<15} | {end:<15} | {status:<15}\n"
            if inactive_status:
                for i, (start, end, status) in enumerate(inactive_status, 1):
                    result_text_content += f"{'Inactive Period ' + str(i):<25} | {start:<15} | {end:<15} | {status:<15}\n"
            if not active_status and not inactive_status:
                result_text_content += f"{'':<25} | {'None':<15} | {'':<15} | {'':<15}\n"
            
            result_text_content += (
                f"\n{'Lost Time Periods':<25} | {'Start':<15} | {'End':<15} | {'Status':<15}\n"
                f"{'-'*25} | {'-'*15} | {'-'*15} | {'-'*15}\n"
            )
            if lost_status:
                for start, end, status in lost_status:
                    result_text_content += f"{'':<25} | {start:<15} | {end:<15} | {status:<15}\n"
            else:
                result_text_content += f"{'':<25} | {'None':<15} | {'':<15} | {'':<15}\n"
            
            result_text_content += (
                f"\n{'Points Breakdown':<25} | {'Points':<20}\n"
                f"{'-'*25} | {'-'*20}\n"
                f"{'Active Duty Points':<25} | {active_points:<20}\n"
            )
            for year, points in reserve_points_by_year.items():
                result_text_content += f"{'Reserve Points (' + year + ')':<25} | {points:<20}\n"
            result_text_content += (
                f"{'Total Reserve Points':<25} | {total_reserve_points:<20}\n"
                f"{'Total Retirement Points':<25} | {total_retirement_points:<20}\n"
            )
            
            result_text_content += (
                f"\n\nNote: {offset_note}\n"
                f"Note: PEBD is {'earliest active start' if reenlist_dt < eos_dt else 'Reenlistment Date minus (active days + 1)'}.\n"
                f"Note: Total Creditable Service includes active and inactive periods.\n"
                f"Note: Active Service Start is {'PEBD' if reenlist_dt >= eos_dt else 'AFADBD minus total active days'}.\n"
                f"Note: Reserve points use anniversary date {doeaf} for prorating, with ~1.85 drills/month."
            )
            if eos_dt < reenlist_dt:
                result_text_content += f"\nWarning: EOS ({eos}) is before Reenlistment Date ({reenlist_date}), which may indicate a historical calculation or data entry error."
            
            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result_text_content)
            self.result_text.config(state='disabled')
            
            if reenlist_date.endswith('-02-29'):
                messagebox.showinfo("Note", "Feb 29 Reenlistment Date: Longevity increases begin on March 1 in non-leap years or Feb 29 in leap years.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date format or input: {e}. Use 'YYYY-MM-DD'.")

root = tk.Tk()
app = PayDateCalculator(root)
root.mainloop()