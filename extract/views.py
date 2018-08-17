from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import HttpResponse
import json
import re
import time
from reports.reports import PdfReport, XlsxReport


ELEMENTS_TO_EXTRACT = [
    {"parameter_in_file": "_chemical_formula_sum",
     "title": "Empirical formula",
     "value": None},
    {"parameter_in_file": "_chemical_formula_weight",
     "title": "M / g mol\u207B\u00B9",
     "value": None},
    {"parameter_in_file": "_cell_measurement_temperature",
     "title": "Temperature / K",
     "value": None},
    {"parameter_in_file": "_diffrn_radiation_wavelength",
     "title": "\u03BB / \u00C5",
     "value": None},
    {"parameter_in_file": "_space_group_crystal_system",
     "title": "Crystal system",
     "value": None},
    {"parameter_in_file": "_space_group_name_H-M_alt",
     "title": "Space group",
     "value": None},
    {"parameter_in_file": "_cell_length_a",
     "title": "a / \u00C5",
     "value": None},
    {"parameter_in_file": "_cell_length_b",
     "title": "b / \u00C5",
     "value": None},
    {"parameter_in_file": "_cell_length_c",
     "title": "c / \u00C5",
     "value": None},
    {"parameter_in_file": "_cell_angle_alpha",
     "title": "\u03B1 / \u00B0",
     "value": None},
    {"parameter_in_file": "_cell_angle_beta",
     "title": "\u03B2 / \u00B0",
     "value": None},
    {"parameter_in_file": "_cell_angle_gamma",
     "title": "\u0263 / \u00B0",
     "value": None},
    {"parameter_in_file": "_cell_volume",
     "title": "V / \u00C5\u00B3",
     "value": None},
    {"parameter_in_file": "_cell_formula_units_Z",
     "title": "Z",
     "value": None},
    {"parameter_in_file": "_exptl_crystal_density_diffrn",
     "title": "Dcalc / g/cm\u00B3",
     "value": None},
    {"parameter_in_file": "_exptl_absorpt_coefficient_mu",
     "title": "\u03BC / mm\u207B\u00B9",
     "value": None},
    {"parameter_in_file": "_diffrn_reflns_number",
     "title": "Unique reflections",
     "value": None},
    {"parameter_in_file": "_diffrn_reflns_av_R_equivalents",
     "title": "R(int)",
     "value": None},
    {"parameter_in_file": "_refine_ls_goodness_of_fit_ref",
     "title": "GOF on F\u00B2",
     "value": None},
    {"parameter_in_file": "_refine_ls_R_factor_gt",
     "title": "R\u2081[I>2\u03C3(I)]b",
     "value": None},
    {"parameter_in_file": "_refine_ls_wR_factor_gt",
     "title": "wR\u2082[I>2\u03C3(I)]",
     "value": None}
]


@ensure_csrf_cookie
def index(request):
    start_time = time.time()
    response_data = {}
    response_data["objects"] = ELEMENTS_TO_EXTRACT
    file_content = request.FILES.get("file").readlines()
    response_data["processed_lines"] = len(file_content)
    for i in response_data["objects"]:
        for line in file_content:
            line = line.strip().decode('utf-8')
            r = re.match(r"^%s\s+(.*)" % (i["parameter_in_file"]), line)
            if (r):
                i["value"] = r.group(1).strip("'")
                break
    response_data["elapsed_time"] = time.time() - start_time
    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")


@csrf_exempt
def get_pdf(request):
    params = json.loads(request.POST.get("extracted_parameters"))
    report = PdfReport("extract/extract.pdf.tmpl")
    report.render(params=params)
    return report.http_response()


@csrf_exempt
def get_xlsx(request):
    params = json.loads(request.POST.get("extracted_parameters"))
    report = XlsxReport("extract/extract.xlsx.tmpl")
    report.render(params=params)
    return report.http_response()
