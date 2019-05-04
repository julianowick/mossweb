import os

from django.db import models

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
    upload = models.FileField(upload_to=upload_filename, null=True, blank=True)

    def __str__(self):
        return self.name
