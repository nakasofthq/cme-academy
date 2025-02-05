import os
import magic
from django.core.exceptions import ValidationError


# To validation pdf files
def pdf_validation(file):
    valid_mime_types = ['application/pdf']
    file_mime_type = magic.from_buffer(file.read(2048), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type.')
    valid_file_extensions = ['.pdf']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')



# To validation images files
def img_validation(file):
    valid_mime_types = ["image/jpeg", "image/png"]
    filesize = file.size
    megabyte_limit = 0.25
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Image too large, Maximum size allowed is %sKB" %(250))
    try:
        file_mime_type = magic.from_buffer(file.read(2048), mime=True)
        if file_mime_type not in valid_mime_types:
            raise ValidationError('Unsupported file type.')
    except:
        pass
    valid_file_extensions = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')



# To validation images and pdf files
def img_pdf_validation(file):
    valid_mime_types = ["image/jpeg", "image/png", 'application/pdf']
    try:
        file_mime_type = magic.from_buffer(file.read(2048), mime=True)
        if file_mime_type not in valid_mime_types:
            raise ValidationError('Unsupported file type.')
    except:
        pass
    valid_file_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')


# To validation microsoft excel files
def xls_validation(file):
    valid_mime_types = ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]
    file_mime_type = magic.from_buffer(file.read(2048), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError("Unsupported file type.")
    valid_file_extensions = [".xls", ".xlsx"]
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')