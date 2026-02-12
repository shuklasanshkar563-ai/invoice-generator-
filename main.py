from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("invoice_form.html")

@app.route("/ownership")
def ownership():
    return render_template("ownership.html")

@app.route("/generate", methods=["POST"])
def generate_invoice():

    # -------- Customer Details --------
    name = request.form.get("name", "")
    email = request.form.get("email", "")
    mobile = request.form.get("mobile", "")
    address = request.form.get("address", "")

    # -------- Item Details --------
    service = request.form.get("service_name", "")
    qty = int(request.form.get("quantity", 1))
    rate = float(request.form.get("rate", 0))
    total = qty * rate

    note = request.form.get("note", "")

    # -------- Checkbox Flags --------
    show_email = request.form.get("show_email") is not None
    show_mobile = request.form.get("show_mobile") is not None
    show_address = request.form.get("show_address") is not None
    show_note = request.form.get("show_note") is not None

    # -------- Invoice Meta --------
    invoice_no = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # -------- Create PDF in Memory --------
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setFont("Helvetica", 12)

    y = 800

    pdf.drawString(50, y, "SS Web Studio")
    y -= 20
    pdf.drawString(50, y, "INVOICE")
    y -= 30

    pdf.drawString(50, y, f"Invoice No: {invoice_no}")
    y -= 20
    pdf.drawString(50, y, f"Date: {datetime.now().strftime('%d-%m-%Y')}")
    y -= 30

    pdf.drawString(50, y, f"Customer Name: {name}")
    y -= 20

    if show_email and email:
        pdf.drawString(50, y, f"Email: {email}")
        y -= 20

    if show_mobile and mobile:
        pdf.drawString(50, y, f"Mobile: {mobile}")
        y -= 20

    if show_address and address:
        pdf.drawString(50, y, f"Address: {address}")
        y -= 20

    y -= 20
    pdf.drawString(50, y, "Item Details")
    y -= 20

    pdf.drawString(50, y, f"Description: {service}")
    y -= 20
    pdf.drawString(50, y, f"Quantity: {qty}")
    y -= 20
    pdf.drawString(50, y, f"Rate: ₹{rate:.2f}")
    y -= 20
    pdf.drawString(50, y, f"Amount: ₹{total:.2f}")
    y -= 30

    pdf.drawString(50, y, f"Total Payable: ₹{total:.2f}")
    y -= 30

    if show_note and note:
        pdf.drawString(50, y, f"Note: {note}")
        y -= 20

    pdf.drawString(50, 80, "Thank you for your business!")
    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{invoice_no}.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
