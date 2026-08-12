from imagekitio import ImageKit
import os
import config

imagekit = ImageKit(
    private_key=config.IMAGEKIT_PRIVATE_KEY
)

def upload_to_imagekit(file_path: str, folder_path: str, custom_filename: str) -> str:
    """
    Uploads a file to ImageKit under folder_path and with custom_filename.
    Returns the CDN url of the uploaded image.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    with open(file_path, "rb") as f:
        result = imagekit.files.upload(
            file=f,
            file_name=custom_filename,
            folder=folder_path,
            use_unique_file_name=False,
            public_key=config.IMAGEKIT_PUBLIC_KEY
        )
    return result.url
