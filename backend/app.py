from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)


def compress_image(file_stream, compressed_image_format="webp"):
    image_to_compress = Image.open(file_stream)
    compressed_image = image_to_compress.convert(
        "P", palette=Image.ADAPTIVE, colors=256
    )
    img_bytes_arr = io.BytesIO()
    compressed_image.save(img_bytes_arr, format=compressed_image_format)
    img_bytes_arr.seek(0)
    return img_bytes_arr


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        img = request.files.get("image_to_compress")
        img_extension = "webp"
        compressed_image_stream = compress_image(img, img_extension)
        return send_file(
            compressed_image_stream,
            as_attachment=True,
            download_name=f"compressed_image.{img_extension}",
            mimetype="image/png",
        )
    return render_template("index.html", page_name="Strona główna")


if __name__ == "__main__":
    app.run(debug=True)
