import os
from django.conf import settings
from django.utils.text import slugify

def get_upload_path(instance, filename):
    """
    Generate upload path based on user type and instance.
    Example: media/students/john-doe/filename.pdf
    """
    if hasattr(instance, 'user_type'):
        base_path = settings.UPLOAD_DIRS.get(instance.user_type, 'others')
    else:
        base_path = 'others'
    
    # Get user's name or username for the subfolder
    if hasattr(instance, 'user'):
        user_folder = slugify(instance.user.get_full_name() or instance.user.username)
    else:
        user_folder = 'unknown'
    
    return os.path.join('uploads', base_path, user_folder, filename) 