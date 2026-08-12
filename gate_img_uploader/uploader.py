import os
import imagekit_client
import supabase_client

def upload_question_images(question_id, file_paths, progress_callback, replace_existing=False):
    """
    Coordinates the upload of multiple images for a GATE question.
    """
    total = len(file_paths)
    if total == 0:
        return
        
    if replace_existing:
        progress_callback(0, total, "Deleting existing question image records...")
        supabase_client.delete_question_images(question_id)
        
    for index, filepath in enumerate(file_paths, start=1):
        filename = os.path.basename(filepath)
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        if not ext:
            ext = ".png"
            
        custom_filename = f"q_{index}{ext}"
        folder_path = f"gate/questions/{question_id}"
        
        progress_callback(index - 1, total, f"Uploading {filename} to ImageKit ({index}/{total})...")
        cdn_url = imagekit_client.upload_to_imagekit(filepath, folder_path, custom_filename)
        
        progress_callback(index - 1, total, f"Saving {filename} to database...")
        supabase_client.insert_question_image(question_id, cdn_url, index)
        
    progress_callback(total, total, "Question images upload complete!")

def upload_option_images(option_id, file_paths, progress_callback, replace_existing=False):
    """
    Coordinates the upload of multiple images for a GATE option.
    """
    total = len(file_paths)
    if total == 0:
        return
        
    if replace_existing:
        progress_callback(0, total, "Deleting existing option image records...")
        supabase_client.delete_option_images(option_id)
        
    for index, filepath in enumerate(file_paths, start=1):
        filename = os.path.basename(filepath)
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        if not ext:
            ext = ".png"
            
        custom_filename = f"opt_{index}{ext}"
        folder_path = f"gate/options/{option_id}"
        
        progress_callback(index - 1, total, f"Uploading {filename} to ImageKit ({index}/{total})...")
        cdn_url = imagekit_client.upload_to_imagekit(filepath, folder_path, custom_filename)
        
        progress_callback(index - 1, total, f"Saving {filename} to database...")
        supabase_client.insert_option_image(option_id, cdn_url, index)
        
    progress_callback(total, total, "Option images upload complete!")
