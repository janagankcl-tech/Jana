"""
Invoice Generator Web App
Run: python app.py
Then open http://localhost:5000 in your browser.
"""
import os
import tempfile
import threading
import webbrowser
from flask import Flask, render_template, request, send_file
from invoice_generator import (
    build_strongminds, build_audere,
    MY_NAME, MY_ADDRESS, MY_EMAIL, BANK_DETAILS, SM, AU
)
from ulcm_model import default_params as ULCM_DEFAULTS

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html",
        my_name=MY_NAME,
        my_address=MY_ADDRESS,
        my_email=MY_EMAIL,
        bank_details=BANK_DETAILS,
        sm=SM,
        au=AU,
    )


@app.route("/generate/strongminds", methods=["POST"])
def generate_strongminds():
    f = request.form

    # Parse line items from the dynamic table rows
    items = []
    i = 0
    while f.get(f"item_desc_{i}") is not None:
        desc  = f.get(f"item_desc_{i}", "").strip()
        qty   = f.get(f"item_qty_{i}", "0").strip()
        price = f.get(f"item_price_{i}", "0").strip()
        if desc:
            try:
                items.append((desc, int(qty), float(price)))
            except ValueError:
                pass
        i += 1

    sm_data = {
        "invoice_number": f.get("invoice_number", "").strip(),
        "date":           f.get("inv_date", "").strip(),
        "due":            f.get("due", "").strip(),
        "po_number":      f.get("po_number", "").strip(),
        "bill_to":        f.get("bill_to", "").strip(),
        "contact":        f.get("contact", "").strip(),
        "notes":          f.get("notes", "").strip(),
        "items":          items,
        "currency":       f.get("currency", "USD").strip(),
    }

    tmp = tempfile.mkdtemp()
    path = build_strongminds(
        my_name=f.get("my_name", MY_NAME).strip(),
        my_address=f.get("my_address", MY_ADDRESS).strip(),
        my_email=f.get("my_email", MY_EMAIL).strip(),
        bank_details=f.get("bank_details", BANK_DETAILS).strip(),
        sm_data=sm_data,
        output_dir=tmp,
    )
    filename = os.path.basename(path)
    return send_file(path, as_attachment=True, download_name=filename)


@app.route("/generate/audere", methods=["POST"])
def generate_audere():
    f = request.form

    # Parse program rows
    rows = []
    i = 0
    while f.get(f"program_{i}") is not None:
        program = f.get(f"program_{i}", "").strip()
        hours   = f.get(f"hours_{i}", "0").strip()
        rate    = f.get(f"rate_{i}", "0").strip()
        if program:
            try:
                rows.append((program, int(hours) if hours else 0, int(rate) if rate else 0))
            except ValueError:
                pass
        i += 1

    au_data = {
        "date_period_start": f.get("date_period_start", "").strip(),
        "date_period_end":   f.get("date_period_end", "").strip(),
        "period_note":       f.get("period_note", "").strip(),
        "rows":              rows,
    }

    tmp = tempfile.mkdtemp()
    path = build_audere(
        my_name=f.get("my_name", MY_NAME).strip(),
        my_address=f.get("my_address", MY_ADDRESS).strip(),
        my_email=f.get("my_email", MY_EMAIL).strip(),
        bank_details=f.get("bank_details", BANK_DETAILS).strip(),
        au_data=au_data,
        output_dir=tmp,
    )
    filename = os.path.basename(path)
    return send_file(path, as_attachment=True, download_name=filename)


@app.route("/ulcm")
def ulcm():
    return render_template("ulcm.html")


def open_browser():
    path = os.environ.get("OPEN_PATH", "/")
    webbrowser.open(f"http://localhost:5000{path}")


if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=False, port=5000)
