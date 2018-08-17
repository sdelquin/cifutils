from jinja2 import Environment, FileSystemLoader
import uuid
from django.http import HttpResponse
import os
import xlsxwriter
import re
from django.conf import settings

TEMPLATES_DIR = "reports/templates"
RENDERED_FILES_DIR = "/tmp/"
PDFFILES_EXTENSION = ".pdf"
XLSXFILES_EXTENSION = ".xlsx"
XLSXFILES_LINE_SEPARATOR = "\n"
XLSXFILES_ELEMENT_SEPARATOR = ";"

ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


class PdfReport():

    def __init__(self, template_filepath):
        """
        template_filepath is always relative to TEMPLATES_DIR
        """
        self.template = ENV.get_template(template_filepath)
        self.mappings = {
            'base_dir': os.path.join(settings.BASE_DIR, TEMPLATES_DIR)
        }

    def render(self, **kwargs):
        self.output_filename = RENDERED_FILES_DIR + str(uuid.uuid4()) +\
            PDFFILES_EXTENSION
        self.rendered_filename = RENDERED_FILES_DIR + str(uuid.uuid4()) +\
            '.html'
        for k, v in kwargs.items():
            self.mappings[k] = v
        self.rendered_template = self.template.render(self.mappings)
        with open(self.rendered_filename, 'w') as f:
            f.write(self.rendered_template)
        os.system(f'prince {self.rendered_filename} -o {self.output_filename}')
        os.remove(self.rendered_filename)

    def http_response(self):
        response = HttpResponse(open(self.output_filename, 'rb'))
        os.remove(self.output_filename)
        response["Content-Type"] = "application/pdf"
        response["Content-Disposition"] = \
            f'attachment; filename="report.pdf"'
        return response


class XlsxReport():

    def __init__(self, template_filepath):
        """
        template_filepath is always relative to TEMPLATES_DIR
        """
        self.template = ENV.get_template(template_filepath)

    def render(self, **kwargs):
        self.output_filename = RENDERED_FILES_DIR + str(uuid.uuid4()) +\
            XLSXFILES_EXTENSION
        self.rendered_template = self.template.render(kwargs)
        self.workbook = xlsxwriter.Workbook(self.output_filename)
        self.worksheet = self.workbook.add_worksheet()
        lines = self.rendered_template.split(XLSXFILES_LINE_SEPARATOR)
        row_number = 0
        for l in lines:
            if (re.match(r"^\s*$", l)):
                continue
            col_number = 0
            elements = l.split(XLSXFILES_ELEMENT_SEPARATOR)
            for e in elements:
                self.worksheet.write(row_number, col_number, e.strip())
                col_number += 1
            row_number += 1
        self.workbook.close()

    def http_response(self):
        response = HttpResponse(open(self.output_filename, 'rb'))
        os.remove(self.output_filename)
        response["Content-Type"] = "application/xlsx"
        response["Content-Disposition"] = \
            f'attachment; filename="report.xlsx"'
        return response
