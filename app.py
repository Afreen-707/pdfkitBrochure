import os
import io
import pdfkit
from flask import Flask, request, render_template, send_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        services = request.form["services"].splitlines()
        contact = request.form["contact"].splitlines()
        logo_file = request.files["logo"]

        logo_url = None
        if logo_file and logo_file.filename:
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_file.filename)
            logo_file.save(logo_path)
            logo_url = f"file:///{os.path.abspath(logo_path).replace(os.sep, '/')}"

        rendered = render_template("brochure_template.html",
                                   name=name,
                                   services=services,
                                   contact=contact,
                                   logo_url=logo_url)

        html_path = "temp.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        # ✅ Add this option to fix local file access
        options = {
            'enable-local-file-access': None
        }

        # 👇 Now wkhtmltopdf can access local files like images
        pdf = pdfkit.from_file(html_path, False, options=options)

        return send_file(io.BytesIO(pdf),
                         download_name="business_brochure.pdf",
                         as_attachment=True)

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
