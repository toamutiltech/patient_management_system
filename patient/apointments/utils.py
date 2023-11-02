
import os
import uuid
from PIL import Image
from flask import url_for, current_app



def save_picture(form_image):
	
	 # Generate a unique filename (e.g., using a UUID or timestamp)
    unique_filename = str(uuid.uuid4()) + os.path.splitext(form_image.filename)[-1]

    # Save the file to the specified directory
    file_path = os.path.join(current_app.root_path, 'static/space_image', unique_filename)
    form_image.save(file_path)

    # Return the filename (without the path)
    return unique_filename