"""
Invoice Generator — StrongMinds & Audere
Usage:
  python invoice_generator.py strongminds
  python invoice_generator.py audere
Edit the CONFIG section below to set your details and invoice data.
"""
import sys
from datetime import date, timedelta
from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, numbers
)
from openpyxl.utils import get_column_letter
# ─────────────────────────────────────────────
# CONFIG — edit these before running
# ─────────────────────────────────────────────
MY_NAME    = "Dr Janagan Alagarajah"
MY_ADDRESS = "5 Highbury Close, New Malden, Surrey, KT3 5BY, UK"
MY_EMAIL   = "jana@auderenow.org"
# Payment / bank details
BANK_DETAILS = (
    "Account holder: Janagan Alagarajah\n"
    "Account number: GB89MONZO04000491867829\n"
    "Account type: Personal\n"
    "Bank name: Monzo Bank\n"
    "Branch code: Broadwalk House\n"
    "SWIFT Code: MONZGB2L"
)
# ── StrongMinds invoice ──
SM = {
    "invoice_number": "INV-2026-003",
    "date": date.today().strftime("%d %B %Y"),
    "due": "Due on receipt",
    "po_number": "",
    "bill_to": "StrongMinds\nKampala, Uganda",
    "contact": "StrongMinds Finance Team",
    "notes": "If you have any questions please contact me by email.",
    # Line items: (description, quantity, unit_price_usd)
    "items": [
        ("Innovation Lab Lead – ULCM Phase 3, Team Meetings, External Meetings", 16, 550.00),
        ("SMZ Trip (8–13 Feb) Expenses (food, taxis)", 1, 266.04),
    ],
    "currency": "USD",
}
# ── Audere time report ──
AU = {
    "date_period_start": "19/01/2026",
    "date_period_end":   "22/02/2026",
    "period_note":       "OOO from 28 January to 6 February 2026 (6 days of work)",
    # Rows: (program, hours, hourly_rate)
    # Set hours=0 or rate=0 to leave blank (like the original)
    "rows": [
        ("AI-HIVE Suppl",               24, 50),
        ("PSI HIV",                      0, 50),
        ("CeSHHAR",                      0, 50),
        ("General – Project",           24,  0),
        ("General Malaria",              0,  0),
        ("General – Support & Maintenance", 0, 0),
    ],
}
# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def thin_border(**sides):
    thin = Side(style="thin")
    return Border(**{s: thin for s in sides})
def all_border():
    thin = Side(style="thin")
    return Border(left=thin, right=thin, top=thin, bottom=thin)
def set_cell(ws, row, col, value="", bold=False, size=11, color="000000",
             bg=None, align="left", valign="center", wrap=False,
             number_format=None, border=None, italic=False):
    cell = ws.cell(row=row, column=col, value=value)
    cell.font = Font(name="Calibri", bold=bold, size=size, color=color, italic=italic)
    cell.alignment = Alignment(horizontal=align, vertical=valign, wrap_text=wrap)
    if bg:
        cell.fill = PatternFill("solid", fgColor=bg)
    if number_format:
        cell.number_format = number_format
    if border:
        cell.border = border
    return cell
def col_width(ws, col, w):
    ws.column_dimensions[get_column_letter(col)].width = w
def row_height(ws, row, h):
    ws.row_dimensions[row].height = h
# ─────────────────────────────────────────────
# StrongMinds Invoice
# ─────────────────────────────────────────────
def build_strongminds():
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoice"
    # Column widths  A   B     C    D     E     F
    for col, w in [(1,4),(2,28),(3,18),(4,14),(5,14),(6,14)]:
        col_width(ws, col, w)
    DARK  = "1F3864"   # navy
    MID   = "2F5496"   # mid blue
    LIGHT = "D6E4F7"   # pale blue
    WHITE = "FFFFFF"
    GOLD  = "F2C94C"
    GRAY  = "F2F2F2"
    # ── Row 1-2: header bar ──
    ws.merge_cells("A1:F2")
    set_cell(ws, 1, 1, "INVOICE", bold=True, size=22, color=WHITE,
             bg=DARK, align="center", valign="center")
    row_height(ws, 1, 36)
    row_height(ws, 2, 5)
    # ── Row 3-7: two-column info block ──
    row_height(ws, 3, 18)
    ws.merge_cells("B3:C3")
    set_cell(ws, 3, 2, MY_NAME, bold=True, size=12)
    ws.merge_cells("E3:F3")
    set_cell(ws, 3, 5, "Invoice Number:", bold=True, align="right")
    ws.merge_cells("E4:F4")
    set_cell(ws, 4, 5, SM["invoice_number"], bold=True, size=12, color=MID, align="right")
    ws.merge_cells("B4:C4")
    set_cell(ws, 4, 2, MY_ADDRESS)
    ws.merge_cells("B5:C5")
    set_cell(ws, 5, 2, MY_EMAIL)
    row_height(ws, 6, 5)
    ws.merge_cells("B7:C7")
    set_cell(ws, 7, 2, "Bill To:", bold=True, size=10, color="888888")
    ws.merge_cells("E7:F7")
    set_cell(ws, 7, 5, "Date:", bold=True, align="right")
    ws.merge_cells("B8:C9")
    set_cell(ws, 8, 2, SM["bill_to"], wrap=True, valign="top")
    row_height(ws, 8, 30)
    ws.merge_cells("E8:F8")
    set_cell(ws, 8, 5, SM["date"], align="right")
    ws.merge_cells("E9:F9")
    set_cell(ws, 9, 5, SM["due"], align="right", color="888888", size=9)
    # Contact
    ws.merge_cells("B10:C10")
    set_cell(ws, 10, 2, f"Contact: {SM['contact']}", size=9, color="666666")
    # PO
    if SM["po_number"]:
        ws.merge_cells("E10:F10")
        set_cell(ws, 10, 5, f"PO #: {SM['po_number']}", align="right", size=9)
    row_height(ws, 11, 8)
    # ── Table header ──
    headers = ["", "DESCRIPTION", "QTY", "UNIT PRICE", "AMOUNT", ""]
    aligns  = ["left","left","center","right","right","left"]
    for i, (h, a) in enumerate(zip(headers, aligns), 1):
        set_cell(ws, 12, i, h, bold=True, size=10, color=WHITE,
                 bg=DARK, align=a, border=all_border())
    row_height(ws, 12, 20)
    # ── Line items ──
    r = 13
    currency = SM["currency"]
    fmt = '"$"#,##0.00'
    for desc, qty, price in SM["items"]:
        row_height(ws, r, 22)
        bg = WHITE if (r % 2 == 1) else GRAY
        set_cell(ws, r, 1, "", bg=bg)
        set_cell(ws, r, 2, desc, bg=bg, wrap=True, valign="center")
        set_cell(ws, r, 3, qty, bg=bg, align="center")
        set_cell(ws, r, 4, price, bg=bg, align="right", number_format=fmt)
        set_cell(ws, r, 5, f"={get_column_letter(3)}{r}*{get_column_letter(4)}{r}",
                 bg=bg, align="right", number_format=fmt)
        set_cell(ws, r, 6, "", bg=bg)
        r += 1
    # Filler rows to pad table
    for _ in range(max(0, 6 - len(SM["items"]))):
        for c in range(1, 7):
            set_cell(ws, r, c, "", bg=GRAY if r%2==0 else WHITE)
        row_height(ws, r, 18)
        r += 1
    # ── Subtotal / Total ──
    first_item_row = 13
    last_item_row  = r - 1
    row_height(ws, r, 5); r += 1
    ws.merge_cells(f"B{r}:D{r}")
    set_cell(ws, r, 2, "Subtotal", bold=True, align="right")
    subtotal_formula = f"=SUM(E{first_item_row}:E{last_item_row})"
    set_cell(ws, r, 5, subtotal_formula, bold=True, align="right", number_format=fmt)
    r += 1
    ws.merge_cells(f"B{r}:D{r}")
    set_cell(ws, r, 2, "Tax (0%)", align="right", color="888888")
    set_cell(ws, r, 5, 0, align="right", number_format=fmt, color="888888")
    r += 1
    row_height(ws, r, 5); r += 1
    set_cell(ws, r, 1, "", bg=DARK)
    ws.merge_cells(f"B{r}:D{r}")
    set_cell(ws, r, 2, f"{currency} GRAND TOTAL", bold=True, size=13,
             align="right", color=WHITE, bg=DARK)
    set_cell(ws, r, 5, f"=E{r-3}+E{r-2}", bold=True, size=13,
             align="right", color=WHITE, bg=DARK, number_format=fmt)
    set_cell(ws, r, 6, "", bg=DARK)
    row_height(ws, r, 26); r += 2
    # ── Notes ──
    if SM["notes"]:
        ws.merge_cells(f"B{r}:F{r}")
        set_cell(ws, r, 2, "Notes", bold=True, size=9, color="888888")
        r += 1
        ws.merge_cells(f"B{r}:F{r+1}")
        set_cell(ws, r, 2, SM["notes"], size=9, color="444444",
                 wrap=True, valign="top")
        r += 3
    # ── Bank / payment details ──
    ws.merge_cells(f"B{r}:F{r}")
    set_cell(ws, r, 2, "Payment Details", bold=True, size=9, color="888888",
             bg=LIGHT)
    set_cell(ws, r, 1, "", bg=LIGHT)
    r += 1
    lines = BANK_DETAILS.split("\n")
    for line in lines:
        ws.merge_cells(f"B{r}:F{r}")
        set_cell(ws, r, 2, line, size=9, bg=LIGHT)
        set_cell(ws, r, 1, "", bg=LIGHT)
        r += 1
    # Print area
    ws.print_area = f"A1:F{r}"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.orientation = "portrait"
    filename = f"Invoice_StrongMinds_{SM['invoice_number']}.xlsx"
    wb.save(filename)
    print(f"✅  Saved: {filename}")
    return filename
# ─────────────────────────────────────────────
# Audere Time Report
# ─────────────────────────────────────────────
def build_audere():
    wb = Workbook()
    ws = wb.active
    ws.title = "Time Reporting"
    for col, w in [(1,6),(2,18),(3,30),(4,18),(5,10),(6,12),(7,14)]:
        col_width(ws, col, w)
    AUDERE_GRAY = "E8E8E8"
    YELLOW      = "FFFF00"
    BLUE_HDR    = "BDD7EE"
    BLUE_TOTAL  = "9DC3E6"
    WHITE       = "FFFFFF"
    def yrow(ws, r, label, value, h=18):
        row_height(ws, r, h)
        ws.merge_cells(f"B{r}:C{r}")
        set_cell(ws, r, 2, label, bold=True, size=10)
        ws.merge_cells(f"D{r}:G{r}")
        set_cell(ws, r, 4, value, bg=YELLOW, size=10)
    # ── Row 1: Audere logo ──
    ws.merge_cells("A1:G1")
    set_cell(ws, 1, 1, "audere", bold=False, size=24, bg=AUDERE_GRAY,
             align="left", valign="center", italic=True)
    row_height(ws, 1, 40)
    # ── Row 2: Title ──
    ws.merge_cells("A2:G2")
    set_cell(ws, 2, 1, "HOURLY WORKER TIME REPORTING", bold=True, size=13,
             bg=AUDERE_GRAY, align="left", valign="center")
    row_height(ws, 2, 24)
    row_height(ws, 3, 6)
    # ── Info rows ──
    yrow(ws, 4, "Name",            MY_NAME)
    yrow(ws, 5, "Mailing Address", MY_ADDRESS, h=22)
    yrow(ws, 6, "Email Address",   MY_EMAIL)
    # Date period row — multi-column
    row_height(ws, 7, 20)
    ws.merge_cells("B7:C7")
    set_cell(ws, 7, 2, "Date Period", bold=True, size=10)
    set_cell(ws, 7, 4, AU["date_period_start"], bg=YELLOW, size=10)
    set_cell(ws, 7, 5, AU["date_period_end"],   bg=YELLOW, size=10)
    ws.merge_cells(f"F7:G7")
    set_cell(ws, 7, 6, AU["period_note"], bg=YELLOW, size=9, wrap=True)
    row_height(ws, 8, 8)
    # ── Table header ──
    # Manual header row
    r = 9
    row_height(ws, r, 20)
    for col, (label, al) in enumerate([
        ("Date","center"), ("Activity Description","left"),
        ("Program","left"), ("Hours","center"),
        ("Hourly Rate","center"), ("Amount","right"), ("","right")
    ], 1):
        set_cell(ws, r, col, label, bold=True, size=10,
                 bg=BLUE_HDR, align=al, border=all_border())
    r += 1
    fmt_usd = '"$"#,##0.00'
    fmt_hrs = '0'
    for program, hours, rate in AU["rows"]:
        row_height(ws, r, 18)
        set_cell(ws, r, 1, "", border=all_border())  # Date
        set_cell(ws, r, 2, "", border=all_border())  # Activity
        set_cell(ws, r, 3, program, border=all_border())
        # Hours — only write if non-zero
        h_val = hours if hours else ""
        set_cell(ws, r, 4, h_val, align="center", border=all_border())
        # Rate
        r_val = rate if rate else ""
        set_cell(ws, r, 5, r_val, align="center", border=all_border())
        # Amount = hours * rate (only if both present)
        if hours and rate:
            set_cell(ws, r, 6, f"=D{r}*E{r}", align="right",
                     number_format=fmt_usd, border=all_border())
        else:
            set_cell(ws, r, 6, "$0.00", align="right", border=all_border())
        set_cell(ws, r, 7, "", border=all_border())
        r += 1
    row_height(ws, r, 6); r += 1
    # ── Total row ──
    row_height(ws, r, 26)
    ws.merge_cells(f"A{r}:C{r}")
    set_cell(ws, r, 1, "TOTAL", bold=True, size=14,
             bg=BLUE_TOTAL, align="center", valign="center")
    first_data = 10
    last_data  = r - 2
    set_cell(ws, r, 4, f"=SUM(D{first_data}:D{last_data})",
             bold=True, size=13, bg=BLUE_TOTAL, align="center",
             number_format=fmt_hrs)
    set_cell(ws, r, 5, "", bg=BLUE_TOTAL)
    set_cell(ws, r, 6, f"=SUM(F{first_data}:F{last_data})",
             bold=True, size=13, bg=BLUE_TOTAL, align="right",
             number_format=fmt_usd)
    set_cell(ws, r, 7, "", bg=BLUE_TOTAL)
    r += 2
    # ── Payment details ──
    ws.merge_cells(f"B{r}:G{r}")
    set_cell(ws, r, 2,
             "Payment Details (if not paid through Justworks)",
             bold=True, size=10, bg=YELLOW)
    set_cell(ws, r, 1, "", bg=YELLOW)
    r += 1
    for line in BANK_DETAILS.split("\n"):
        ws.merge_cells(f"B{r}:G{r}")
        set_cell(ws, r, 2, line, size=9, bg=YELLOW)
        set_cell(ws, r, 1, "", bg=YELLOW)
        row_height(ws, r, 16)
        r += 1
    ws.print_area = f"A1:G{r}"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.orientation = "portrait"
    period = AU["date_period_end"].replace("/", "-")
    filename = f"Audere_TimeReport_{period}.xlsx"
    wb.save(filename)
    print(f"✅  Saved: {filename}")
    return filename
# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("strongminds", "audere", "both"):
        print("Usage: python invoice_generator.py [strongminds|audere|both]")
        sys.exit(1)
    target = sys.argv[1]
    if target in ("strongminds", "both"):
        build_strongminds()
    if target in ("audere", "both"):
        build_audere()
