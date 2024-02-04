from io import BytesIO
from PIL import Image, UnidentifiedImageError
from werkzeug.datastructures import FileStorage
from enum import Enum
from zipfile import ZipFile
from typing import List, TypedDict


class FilesToZip(TypedDict):
    name: str
    data: BytesIO


class ImageFormat(Enum):
    """Available formats for ImageOptimizer

    Args:
        Enum (WEBP): Best format for website images - due best quality for the lowest size.
        Enum (PNG): Standard format for images.
    """

    WEBP = "webp"
    PNG = "png"


class ZipMixin:
    @staticmethod
    def save_to_zip(files: List[FilesToZip]) -> BytesIO:
        result_zip = BytesIO()
        with ZipFile(result_zip, "w") as zf:
            for file in files:
                zf.writestr(
                    file.get("name"),
                    file.get("data").getvalue(),
                )
        result_zip.seek(0)
        return result_zip


class ImageOptimizer(ZipMixin):

    @staticmethod
    def compress_image(
        file_stream: FileStorage,
        compressed_image_format: ImageFormat = ImageFormat.WEBP,
    ) -> BytesIO:
        """Compress image by changing colors to 8-bit (256).

        Args:
            file_stream (FileStorage): Data given from form input
            compressed_image_format (ImageFormat, optional): Format of output image. Defaults to "ImageFormat.WEBP".

        Returns:
            BytesIO: compressed image

        Returns:
            BytesIO: _description_
        """
        try:
            image_to_compress = Image.open(file_stream)
            compressed_image = image_to_compress.convert(
                "P", palette=Image.ADAPTIVE, colors=256
            )
            img_bytes_arr = BytesIO()
            compressed_image.save(img_bytes_arr, format=compressed_image_format)
            img_bytes_arr.seek(0)
            return img_bytes_arr
        except (FileNotFoundError, UnidentifiedImageError, ValueError, TypeError) as e:
            raise e

    @staticmethod
    def compress_images(
        images: List[FileStorage],
        compressed_image_format: ImageFormat = ImageFormat.WEBP,
    ) -> BytesIO:
        compressed_images = []
        for img in images:
            compressed_images.append(
                {
                    "name": f"{img.filename.split('.')[0]}.{compressed_image_format}",
                    "data": ImageOptimizer.compress_image(img, compressed_image_format),
                }
            )
        return ImageOptimizer.save_to_zip(compressed_images)
