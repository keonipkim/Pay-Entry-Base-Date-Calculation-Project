#!/usr/bin/env python3
"""
PEBD Calculator per DoDFMR Volume 7A, Chapter 1, Section 2.4 (May 2024).
With Tkinter GUI, includes DEP service (post-1985 restrictions) and officer/enlisted handling.
"""

import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox

class PEBDCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("PEBD Calculator (DoDFMR Vol 7A, Ch 1)")
        self.date_periods = []
        self.lost_periods = []
        self.entries = {}

        # Core date entries
        self.create_label_entry("Date of Original Entry Armed Forces (DOEAF):", 0)
        self.create_label_entry("1st Day of Active Duty (initial PEBD):", 1)
        self.create_label_entry("End of Obligated Service Date (EOS):", 2)
        self.create_label_entry("Reentry Date:", 3)
        tk.Label(root, text="Member Type:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.member_type = tk.StringVar(value="Enlisted")
        tk.OptionMenu(root, self.member_type, "Enlisted", "Officer").grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(root, text="Add Creditable Service Period", command=self.add_service_period).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Add Time Lost Period", command=self.add_lost_period).grid(row=6, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Add DEP Service", command=self.add_dep_service).grid(row=7, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Calculate PEBD", command=self.calculate_pebd).grid(row=8, column=0, pady=10)
        tk.Button(root, text="Reset", command=self.reset).grid(row=8, column=1, pady=10)

    def create_label_entry(self, label_text, row):
        tk.Label(self.root, text=label_text).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        entry = tk.Entry(self.root)
        entry.grid(row=row, column=1, padx=5, pady=5)
        self.entries[label_text.strip(":")] = entry

    def add_service_period(self):
        self.add_period_window("Add Creditable Service Period", self.date_periods)

    def add_lost_period(self):
        self.add_period_window("Add Time Lost Period", self.lost_periods)

    def add_dep_service(self):
        window = tk.Toplevel(self.root)
        window.title("Add DEP Service")
        tk.Label(window, text="DEP Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        start_entry = tk.Entry(window)
        start_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(window, text="DEP End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        end_entry = tk.Entry(window)
        end_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(window, text="Performed IDT? (post-Nov 28, 1989):").grid(row=2, column=0, padx=5, pady=5)
        idt_var = tk.StringVar(value="No")
        tk.OptionMenu(window, idt_var, "Yes", "No").grid(row=2, column=1, padx=5, pady=5)
        tk.Button(window, text="Save", command=lambda: self.save_dep(window, start_entry, end_entry, idt_var)).grid(row=3, column=0, columnspan=2, pady=10)

    def add_period_window(self, title, period_list):
        window = tk.Toplevel(self.root)
        window.title(title)
        tk.Label(window, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        start_entry = tk.Entry(window)
        start_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(window, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        end_entry = tk.Entry(window)
        end_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(window, text="Save", command=lambda: self.save_period(window, start_entry, end_entry, period_list)).grid(row=2, column=0, columnspan=2, pady=10)

    def save_period(self, window, start_entry, end_entry, period_list):
        start = start_entry.get()
        end = end_entry.get()
        try:
            datetime.strptime(start, '%Y-%m-%d')
            datetime.strptime(end, '%Y-%m-%d')
            period_list.append((start, end))
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use 'YYYY-MM-DD'.")

    def save_dep(self, window, start_entry, end_entry, idt_var):
        start = start_entry.get()
        end = end_entry.get()
        idt = idt_var.get()
        try:
            start_dt = datetime.strptime(start, '%Y-%m-%d')
            end_dt = datetime.strptime(end, '%Y-%m-%d')
            dep_start_1985 = datetime(1985, 1, 1)
            dep_cutoff_1989 = datetime(1989, 11, 29)

            if start_dt < dep_start_1985:
                self.date_periods.append((start, end))
                print(f"DEP service {start} to {end} added (pre-1985, creditable).")
            elif dep_start_1985 <= start_dt < dep_cutoff_1989:
                print(f"DEP service {start} to {end} not added (1985–1989, not creditable).")
            elif start_dt >= dep_cutoff_1989 and idt == "Yes":
                self.date_periods.append((start, end))
                print(f"DEP service {start} to {end} added (post-1989, IDT performed).")
            else:
                print(f"DEP service {start} to {end} not added (post-1989, no IDT).")
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use 'YYYY-MM-DD'.")

    def calculate_inclusive_days(self, start_date, end_date):
        d1 = datetime.strptime(start_date, '%Y-%m-%d')
        d2 = datetime.strptime(end_date, '%Y-%m-%d')
        if d2.day == 31:
            d2 = d2.replace(day=30)
        elif d2.month == 2 and d2.day == 29 and not (d2.year % 4 == 0 and (d2.year % 100 != 0 or d2.year % 400 == 0)):
            d2 = d2.replace(day=28)  # Non-leap year Feb 29 -> 28
        return (d2 - d1).days + 1

    def calculate_total_inclusive_days(self, periods):
        return sum(self.calculate_inclusive_days(start, end) for start, end in periods)

    def subtract_days_from_date(self, reference_date, days_to_subtract):
        ref_date = datetime.strptime(reference_date, '%Y-%m-%d')
        result_date = ref_date - timedelta(days=days_to_subtract)
        return result_date.strftime('%Y-%m-%d')

    def add_days_to_date(self, reference_date, days_to_add):
        ref_date = datetime.strptime(reference_date, '%Y-%m-%d')
        result_date = ref_date + timedelta(days=days_to_add)
        return result_date.strftime('%Y-%m-%d')

    def calculate_lost_time(self, lost_periods):
        total_lost_days = 0
        for start, end in lost_periods:
            days = self.calculate_inclusive_days(start, end)
            years = days // 360
            remaining_days = days % 360
            months = remaining_days // 30
            extra_days = remaining_days % 30
            total_lost_days += years * 360 + months * 30 + extra_days
        return total_lost_days

    def days_to_ymd(self, start_date, end_date):
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        if end.day == 31:
            end = end.replace(day=30)
        elif end.month == 2 and end.day == 29 and not (end.year % 4 == 0 and (end.year % 100 != 0 or end.year % 400 == 0)):
            end = end.replace(day=28)

        years = end.year - start.year
        months = end.month - start.month
        days = end.day - start.day + 1

        if days < 0:
            months -= 1
            prev_month = start.replace(month=start.month % 12 + 1, year=start.year + start.month // 12)
            days_in_prev_month = (prev_month - start).days + 1
            days += days_in_prev_month
        if months < 0:
            years -= 1
            months += 12

        if end < start:
            return "00 Years, Months 00, Days 00"
        return f"{years:02d} Years, Months {months:02d}, Days {days:02d}"

    def total_days_to_ymd(self, total_days):
        years = total_days // 365
        remaining_days = total_days % 365
        # Count actual leap days in the period (approximation)
        leap_days = years // 4 - years // 100 + years // 400
        adjusted_days = remaining_days - leap_days
        if adjusted_days < 0:
            years -= 1
            adjusted_days += 365
        months = adjusted_days // 30
        days = adjusted_days % 30
        if months >= 12:
            years += months // 12
            months %= 12
        return f"{years:02d} Years, Months {months:02d}, Days {days:02d}"

    def calculate_pebd(self):
        try:
            doeaf = self.entries["Date of Original Entry Armed Forces (DOEAF)"].get()
            first_active_duty = self.entries["1st Day of Active Duty (initial PEBD)"].get()
            eos = self.entries["End of Obligated Service Date (EOS)"].get()
            reentry_date = self.entries["Reentry Date"].get()
            member_type = self.member_type.get()

            # Validate non-empty dates
            for date in [doeaf, first_active_duty, eos, reentry_date]:
                if date:
                    datetime.strptime(date, '%Y-%m-%d')

            total_service_days = self.calculate_total_inclusive_days(self.date_periods) if self.date_periods else 0
            total_lost_days = self.calculate_lost_time(self.lost_periods) if self.lost_periods else 0
            net_service_days = total_service_days - total_lost_days

            eos_dt = datetime.strptime(eos, '%Y-%m-%d')
            reentry_dt = datetime.strptime(reentry_date, '%Y-%m-%d')

            if reentry_dt <= eos_dt + timedelta(days=1):
                pebd = self.add_days_to_date(first_active_duty, total_lost_days) if total_lost_days > 0 and member_type == "Enlisted" else first_active_duty
                print(f"\nNo break in service (Reentry {reentry_date} ≤ EOS {eos} + 24 hours). "
                      f"PEBD is 1st Day of Active Duty{' adjusted for Time Lost' if total_lost_days > 0 and member_type == 'Enlisted' else ''}.")
            else:
                pebd = self.subtract_days_from_date(reentry_date, net_service_days)
                print(f"\nBreak in service (Reentry {reentry_date} > EOS {eos} + 24 hours). "
                      f"PEBD = Reentry Date - Net Creditable Service Days.")

            result_text = (
                f"Total service days: {self.total_days_to_ymd(total_service_days)}\n"
                f"Time Lost days (30-day month basis): {self.total_days_to_ymd(total_lost_days)}\n"
                f"Net creditable service days: {self.total_days_to_ymd(net_service_days)}\n"
                f"Pay Entry Base Date (PEBD): {pebd}\n"
                f"DOEAF: {doeaf}\n"
                f"EOS: {eos}\n"
                f"1st Day of Active Duty: {first_active_duty}\n"
                f"Reentry Date: {reentry_date}\n"
                f"Member Type: {member_type}\n"
            )
            if self.date_periods:
                result_text += "Creditable Service Periods (including DEP if applicable):\n"
                for i, (start, end) in enumerate(self.date_periods, 1):
                    result_text += f"  Period {i}: {start} to {end} ({self.days_to_ymd(start, end)})\n"
            if self.lost_periods:
                result_text += "Time Lost Periods:\n"
                for i, (start, end) in enumerate(self.lost_periods, 1):
                    result_text += f"  Lost Period {i}: {start} to {end} ({self.days_to_ymd(start, end)})\n"

            # Show results in a popup window instead of just printing
            self.show_results(result_text)

        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid date format: {ve}. Use 'YYYY-MM-DD'.")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {e}")

    def show_results(self, results_text):
        result_window = tk.Toplevel(self.root)
        result_window.title("PEBD Calculation Results")
        text_area = tk.Text(result_window, height=15, width=80)
        text_area.pack(padx=5, pady=5)
        text_area.insert(tk.END, results_text)
        text_area.config(state='disabled')  # Make read-only

    def reset(self):
        """Reset all fields and stored data for a new calculation."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.member_type.set("Enlisted")
        self.date_periods.clear()
        self.lost_periods.clear()
        print("Calculator reset for new calculation.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PEBDCalculator(root)
    root.mainloop()