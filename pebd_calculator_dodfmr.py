#!/usr/bin/env python3
"""
Generic script to calculate PEBD per DoDFMR Volume 7A, Chapter 1, Section 2.4 (May 2024).
Uses tkinter widgets for DOEAF, 1st Day of Active Duty, EOS, Reentry Date, creditable service periods,
and Time Lost. Outputs in 'XX Years, Months XX, Days XX' format.
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
        self.entries = {}  # Initialize the entries dictionary

        # Core date entries
        self.create_label_entry("Date of Original Entry Armed Forces (DOEAF):", 0)
        self.create_label_entry("1st Day of Active Duty (initial PEBD):", 1)
        self.create_label_entry("End of Obligated Service Date (EOS):", 2)
        self.create_label_entry("Reentry Date:", 3)

        # Buttons for adding periods
        tk.Button(root, text="Add Creditable Service Period", command=self.add_service_period).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Add Time Lost Period", command=self.add_lost_period).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Calculate PEBD", command=self.calculate_pebd).grid(row=6, column=0, columnspan=2, pady=10)

    def create_label_entry(self, label_text, row):
        tk.Label(self.root, text=label_text).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        entry = tk.Entry(self.root)
        entry.grid(row=row, column=1, padx=5, pady=5)
        self.entries[label_text.strip(":")] = entry

    def add_service_period(self):
        window = tk.Toplevel(self.root)
        window.title("Add Creditable Service Period")
        
        tk.Label(window, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        start_entry = tk.Entry(window)
        start_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(window, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        end_entry = tk.Entry(window)
        end_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(window, text="Save", command=lambda: self.save_period(window, start_entry, end_entry, self.date_periods)).grid(row=2, column=0, columnspan=2, pady=10)

    def add_lost_period(self):
        window = tk.Toplevel(self.root)
        window.title("Add Time Lost Period")
        
        tk.Label(window, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        start_entry = tk.Entry(window)
        start_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(window, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        end_entry = tk.Entry(window)
        end_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(window, text="Save", command=lambda: self.save_period(window, start_entry, end_entry, self.lost_periods)).grid(row=2, column=0, columnspan=2, pady=10)

    def save_period(self, window, start_entry, end_entry, period_list):
        start = start_entry.get()
        end = end_entry.get()
        try:
            datetime.strptime(start, '%Y-%m-%d')
            datetime.strptime(end, '%Y-%m-%d')
            period_list.append((start, end))
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use 'YYYY-MM-DD' (e.g., 2013-12-17).")

    def calculate_inclusive_days(self, start_date, end_date):
        """Calculate inclusive days with DoDFMR 2.4.1.2.2 adjustments."""
        d1 = datetime.strptime(start_date, '%Y-%m-%d')
        d2 = datetime.strptime(end_date, '%Y-%m-%d')
        if d2.day == 31:
            d2 = d2.replace(day=30)
        elif d2.month == 2 and d2.day == 29:
            d2 = d2.replace(day=30)
        elif d2.month == 2 and d2.day == 28 and not (d2.year % 4 == 0 and (d2.year % 100 != 0 or d2.year % 400 == 0)):
            d2 = d2.replace(day=30)
        return (d2 - d1).days + 1

    def calculate_total_inclusive_days(self, periods):
        """Calculate total inclusive days across periods."""
        return sum(self.calculate_inclusive_days(start, end) for start, end in periods)

    def subtract_days_from_date(self, reference_date, days_to_subtract):
        """Subtract days from a reference date."""
        ref_date = datetime.strptime(reference_date, '%Y-%m-%d')
        result_date = ref_date - timedelta(days=days_to_subtract)
        return result_date.strftime('%Y-%m-%d')

    def add_days_to_date(self, reference_date, days_to_add):
        """Add days to a reference date."""
        ref_date = datetime.strptime(reference_date, '%Y-%m-%d')
        result_date = ref_date + timedelta(days=days_to_add)
        return result_date.strftime('%Y-%m-%d')

    def calculate_lost_time(self, lost_periods):
        """Calculate lost time on a 30-day month basis per 2.4.1.3.1."""
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
        """Convert period to 'XX Years, Months XX, Days XX' using calendar dates."""
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        if end.day == 31:
            end = end.replace(day=30)
        elif end.month == 2 and end.day == 29:
            end = end.replace(day=30)
        elif end.month == 2 and end.day == 28 and not (end.year % 4 == 0 and (end.year % 100 != 0 or end.year % 400 == 0)):
            end = end.replace(day=30)

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
        """Convert total days to 'XX Years, Months XX, Days XX' with calendar approximation."""
        years = total_days // 365
        remaining_days = total_days % 365
        months = remaining_days // 30
        days = remaining_days % 30
        leap_adjust = years // 4
        if remaining_days >= leap_adjust:
            days += leap_adjust
            if days >= 30:
                months += days // 30
                days = days % 30
            if months >= 12:
                years += months // 12
                months = months % 12
        return f"{years:02d} Years, Months {months:02d}, Days {days:02d}"

    def calculate_pebd(self):
        try:
            # Get core dates from entries
            doeaf = self.entries["Date of Original Entry Armed Forces (DOEAF)"].get()
            first_active_duty = self.entries["1st Day of Active Duty (initial PEBD)"].get()
            eos = self.entries["End of Obligated Service Date (EOS)"].get()
            reentry_date = self.entries["Reentry Date"].get()

            # Validate dates
            for date in [doeaf, first_active_duty, eos, reentry_date]:
                datetime.strptime(date, '%Y-%m-%d')

            # Calculate totals
            total_service_days = self.calculate_total_inclusive_days(self.date_periods) if self.date_periods else 0
            total_lost_days = self.calculate_lost_time(self.lost_periods) if self.lost_periods else 0
            net_service_days = total_service_days - total_lost_days

            # Convert dates for comparison
            eos_dt = datetime.strptime(eos, '%Y-%m-%d')
            reentry_dt = datetime.strptime(reentry_date, '%Y-%m-%d')

            # Determine PEBD
            if reentry_dt <= eos_dt + timedelta(days=1):  # 24-hour gap
                pebd = self.add_days_to_date(first_active_duty, total_lost_days) if total_lost_days > 0 else first_active_duty
                print(f"\nNo break in service (Reentry {reentry_date} ≤ EOS {eos} + 24 hours). "
                      f"PEBD is 1st Day of Active Duty{' adjusted for Time Lost' if total_lost_days > 0 else ''}.")
            else:
                pebd = self.subtract_days_from_date(reentry_date, net_service_days)
                print(f"\nBreak in service (Reentry {reentry_date} > EOS {eos} + 24 hours). "
                      f"PEBD = Reentry Date - Net Creditable Service Days.")

            # Display results
            print(f"Total service days: {self.total_days_to_ymd(total_service_days)}")
            print(f"Time Lost days (30-day month basis): {self.total_days_to_ymd(total_lost_days)}")
            print(f"Net creditable service days: {self.total_days_to_ymd(net_service_days)}")
            print(f"Pay Entry Base Date (PEBD): {pebd}")
            print(f"DOEAF: {doeaf}")
            print(f"EOS: {eos}")
            print(f"1st Day of Active Duty: {first_active_duty}")
            print(f"Reentry Date: {reentry_date}")
            if self.date_periods:
                print("Creditable Service Periods:")
                for i, (start, end) in enumerate(self.date_periods, 1):
                    print(f"  Period {i}: {start} to {end} ({self.days_to_ymd(start, end)})")
            if self.lost_periods:
                print("Time Lost Periods:")
                for i, (start, end) in enumerate(self.lost_periods, 1):
                    print(f"  Lost Period {i}: {start} to {end} ({self.days_to_ymd(start, end)})")

        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use 'YYYY-MM-DD' (e.g., 2013-12-17).")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PEBDCalculator(root)
    root.mainloop()