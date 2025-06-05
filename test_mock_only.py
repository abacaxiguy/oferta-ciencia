#!/usr/bin/env python3
"""
Test script to generate PDF with mock data only for comparison
"""

from generate_schedule_pdf import create_timetable_pdf

if __name__ == "__main__":
    print("Generating PDF with mock data...")
    create_timetable_pdf(use_genetic_algorithm=False)
    print("Mock data PDF generated successfully!") 