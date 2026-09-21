from datetime import datetime
from io import BytesIO
import os

import qrcode
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class QRCodeModel(db.Model):
    __tablename__ = "qr_codes"

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.String(255), nullable=False)
    qr_image = db.Column(db.String(255), nullable=True)

    # QR Code Customization Settings
    box_size = db.Column(db.Integer, default=10, nullable=False)
    border = db.Column(db.Integer, default=4, nullable=False)
    fill_color = db.Column(db.String(20), default="#000000", nullable=False)
    back_color = db.Column(db.String(20), default="#FFFFFF", nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __str__(self):
        return self.content

    def save(self):
        """
        Generate and save QR code image using the stored customization settings.
        """

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=self.box_size,
            border=self.border,
        )

        qr.add_data(self.content)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color=self.fill_color,
            back_color=self.back_color
        )

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        filename = f"qr_{timestamp}.png"

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        upload_folder = "static/qr_codes"
        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(upload_folder, filename)

        with open(filepath, "wb") as f:
            f.write(buffer.getvalue())

        self.qr_image = f"/static/qr_codes/{filename}"

        db.session.commit()

    @property
    def get_qr_code_image(self):
        if self.qr_image:
            return self.qr_image

        return None