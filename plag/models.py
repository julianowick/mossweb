import os
import logging

from django.db import models
from django.core.validators import FileExtensionValidator

class Course(models.Model):
    name = models.CharField(max_length=254)
    classe = models.CharField(max_length=5, default='U')
    professor = models.CharField(max_length=254)
    email = models.EmailField()
    year = models.PositiveSmallIntegerField()
    semester = models.PositiveSmallIntegerField()

    def __str__(self):
        return '%s - %s (%d/%d)' % (self.name, self.classe, self.year, self.semester)

# Define file upload path and filename
def upload_filename(instance, filename):
    name, extension = os.path.splitext(filename)
    output = 'uploads/%s/%s%s' % (str(instance.course).replace('/','-'), instance.name, extension) 
    return output.replace(' ', '_')

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    upload = models.FileField(upload_to=upload_filename, null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=('zip',))])

    def extract(self):
        pass

    def moss(self):
        pass

    def __str__(self):
        return self.name

    class AssignmentException(Exception):
        # Get an instance of a logger
        logger = logging.getLogger(__name__)

        def __init__(self, msg):
            self.msg = msg
            self.logger.warning(msg)

        def __str__(self):
            return repr(self.msg)

