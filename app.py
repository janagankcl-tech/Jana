"""
Invoice Generator Web App
Run: python app.py
Then open http://localhost:5000 in your browser.
"""
import os
import tempfile
import threading
import webbrowser
from flask import Flask, jsonify, render_template, request, send_file
from invoice_generator import (
    build_strongminds, build_audere,
    MY_NAME, MY_ADDRESS, MY_EMAIL, BANK_DETAILS, SM, AU
)
from ulcm_model import ULCMModel, run_scenarios, params_from_dict

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


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/ulcm/run", methods=["POST"])
def ulcm_run():
    try:
        data = request.get_json(force=True, silent=True) or {}
        params = params_from_dict(data)
        results = ULCMModel(params).run()
        return jsonify({"ok": True, "results": results})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@app.route("/api/ulcm/scenarios", methods=["POST"])
def ulcm_scenarios():
    try:
        data = request.get_json(force=True, silent=True) or {}
        base = params_from_dict(data.get("base_params", {}))
        out = {}
        for param_name, values in data.get("sweeps", {}).items():
            df = run_scenarios(base, param_name, values)
            out[param_name] = df.to_dict(orient="list")
        return jsonify({"ok": True, "scenarios": out})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


def open_browser():
    webbrowser.open("http://localhost:5000")


if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=False, port=5000)
