import os
import imagekit_client
import supabase_client

def upload_images(question_id, file_paths, progress_callback, replace_existing=False):
    """
    Coordinates the upload of multiple images.
    - Matches files to images/{question_uuid}/{order_index}.ext
    - Inserts records into Supabase.
    - If replace_existing is True, deletes existing images for this question first.
    - progress_callback signature: callback(current_index, total_count, status_message)
    """
    total = len(file_paths)
    if total == 0:
        return
        
    if replace_existing:
        progress_callback(0, total, "Deleting existing database records...")
        supabase_client.delete_existing_images(question_id)
        
    for index, filepath in enumerate(file_paths, start=1):
        filename = os.path.basename(filepath)
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        if not ext:
            ext = ".png" # default fallback
            
        custom_filename = f"{index}{ext}"
        folder_path = f"images/{question_id}"
        
        progress_callback(index - 1, total, f"Uploading {filename} to ImageKit ({index}/{total})...")
        
        # 1. Upload to ImageKit
        cdn_url = imagekit_client.upload_to_imagekit(filepath, folder_path, custom_filename)
        
        progress_callback(index - 1, total, f"Saving {filename} to database...")
        
        # 2. Insert into Supabase
        supabase_client.insert_image_record(question_id, cdn_url, index)
        
    progress_callback(total, total, "Upload complete!")
