from flask import Flask, render_template, request, send_file
from .services.optimizer.img_optimizer import ImageOptimizer, ImageFormat
from PIL import UnidentifiedImageError


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form_images = request.files.getlist("images_to_compress")
        expected_extension = request.form.get("images_format").lower()
        try:
            print(form_images)
            if len(form_images) == 1:
                result = ImageOptimizer.compress_image(
                    form_images[0], expected_extension
                )
                download_name = f"compressed_image.{expected_extension}"
            else:
                result = ImageOptimizer.compress_images(form_images, expected_extension)
                download_name = "compressed_image.zip"
            return send_file(
                result,
                as_attachment=True,
                download_name=download_name,
                mimetype="application/zip",
            )
        except UnidentifiedImageError:
            print("No file")

    return render_template(
        "index.html", page_name="Home", image_formats=list(ImageFormat)
    )


if __name__ == "__main__":
    app.run(debug=True)
