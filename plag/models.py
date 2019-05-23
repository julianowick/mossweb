import os
import logging
import shutil
import zipfile
import mosspy

from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
    dirname = instance.upload_dirname()
    output = '%s/%s%s' % (dirname, instance.name, extension) 
    return output.replace(' ', '_')

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    upload = models.FileField(upload_to=upload_filename, null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=('zip',))])

    def upload_dirname(self):
        dirname = 'uploads/%s' % str(self.course).replace('/','-') 
        return dirname.replace(' ', '_')

    def extract_dirname(self):
        dirname = 'extract/%s/%s' % (str(self.course).replace('/','-'), self.name)
        return dirname.replace(' ', '_')

    def report_dirname(self):
        dirname = 'reports/%s/%s' % (str(self.course).replace('/','-'), self.name)
        return dirname.replace(' ', '_')

    def report_filename(self):
        dirname = self.report_dirname()
        return '%s/report.html' % dirname

    def is_processed(self):
        return os.path.exists(self.report_filename())

    def load_report(self):
        if not self.is_processed():
            raise self.AssignmentException(
                'No report has been created for assignment %s' %
                self.name
            )
        output = ''
        with open(self.report_filename(), 'r') as file:
            data = file.read()
            output += data

        return output

    # Extract assignments from zip file (Moodle assignment style)
    def extract(self):
        if(not(self.upload)): # No file has been uploaded
            raise self.AssignmentException(
                'No file has been uploaded to assignment %s' %
                self.name
            )
        with zipfile.ZipFile(self.upload) as zip_file:
            for member in zip_file.namelist():
                filename = os.path.basename(member)
                # skip directories
                if not filename:
                    continue

                # skip non-C source files
                if not filename.endswith(('.c', '.cpp')):
                    continue

                # copy file (taken from zipfile's extract)
                source = zip_file.open(member)
                # create new name based on the directory name i.e. student's name
                newname = member[0:member.index('_')].replace(' ', '_') + '.c'
                target_dir = self.extract_dirname()
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                target = open(os.path.join(target_dir, newname), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)
        return True

    # Run the moss similarity check web service
    def moss(self):
        m = mosspy.Moss(settings.MOSS_USERID, "c")
        extract_dir = self.extract_dirname()
        if not os.path.exists(extract_dir):
            raise self.AssignmentException(
                'It seems like the zip file for assignment %s has not been extracted' %
                self.name
            )
        m.addFilesByWildcard('%s/*.c' % extract_dir)
        url = m.send()

        logger.info('Report URL: %s ' % url)

        # Save report file
        report_dir = self.report_dirname()
        if not os.path.exists(report_dir):
            os.makedirs('%s/%s' % (report_dir, 'report/'))
        m.saveWebPage(url, "%s/report.html" % report_dir)

        # mosspy.download_report(url, '%s/report/' % report_dir, connections=8, log_level=10) # logging.DEBUG (20 to disable)

    def __str__(self):
        return self.name

    class AssignmentException(Exception):

        def __init__(self, msg):
            self.msg = msg
            logger.warning(msg)

        def __str__(self):
            return repr(self.msg)

