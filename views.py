from flask import redirect, render_template, request, url_for
from flask.views import MethodView

from models import QRCodeModel, db


class QRCodeView(MethodView):

    def get(self):
        qr_code_id = request.args.get("qr_code")

        qr_object = None

        if qr_code_id:
            qr_object = QRCodeModel.query.get(qr_code_id)

        return render_template(
            "generator.html",
            qr_code=qr_object
        )

    def post(self):
        content = request.form.get("content")

        if not content:
            return redirect(url_for("generator"))

        # Get customization settings from form
        box_size = request.form.get("box_size", type=int)
        border = request.form.get("border", type=int)

        fill_color = request.form.get("fill_color", "#000000")
        back_color = request.form.get("back_color", "#FFFFFF")

        # Default values if invalid or missing
        box_size = box_size if box_size and box_size > 0 else 10
        border = border if border is not None and border >= 0 else 4

        new_qr = QRCodeModel(
            content=content,
            box_size=box_size,
            border=border,
            fill_color=fill_color,
            back_color=back_color
        )

        db.session.add(new_qr)
        db.session.commit()

        # Generate QR image and save path
        new_qr.save()

        return redirect(
            url_for(
                "generator",
                qr_code=new_qr.id
            )
        )