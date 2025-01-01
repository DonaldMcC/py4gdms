from py4web.utils.form import Form, FormStyleBootstrap4, FormStyleDefault, FormStyleFactory

#change form.py line 506 to  if field.type == "notboolean":  # changed so this never applies to support this
FormStyleBootstrap4inline = FormStyleFactory()
FormStyleBootstrap4inline.classes.update(
    {
        "outer": "form-group row",
        "inner": "col-sm-9",
        "label": "col-form-label col-sm-3",
        "info": "form-text small text-center",
        "error": "form-text small text-center text-danger py4web-validation-error invalid-feedback",
        "submit": "btn btn-primary",
        "input": "form-control",
        "input[type=text]": "form-control",
        "input[type=date]": "form-control",
        "input[type=time]": "form-control",
        "input[type=datetime-local]": "form-control",
        "input[type=radio]": "form-check-input",
        "input[type=checkbox]": "form-check-input",
        "input[type=submit]": "btn btn-primary",
        "input[type=password]": "form-control",
        "input[type=file]": "form-control-file",
        "select": "form-control",
        "textarea": "form-control",
    }
)


#change form.py line 506 to  if field.type == "notboolean":  # changed so this never applies to support this
FormStyleBootstrap3column = FormStyleFactory()
FormStyleBootstrap3column.classes.update(
    {
        "outer": "form-group row",
        "inner": "col-sm-6",
        "label": "col-form-label col-sm-3",
        "info": "col-sm-3 form-text small text-center",
        "error": "form-text small text-center text-danger py4web-validation-error invalid-feedback",
        "submit": "btn btn-primary",
        "input": "form-control",
        "input[type=text]": "form-control",
        "input[type=date]": "form-control",
        "input[type=time]": "form-control",
        "input[type=datetime-local]": "form-control",
        "input[type=radio]": "form-check-input",
        "input[type=checkbox]": "form-check-input",
        "input[type=submit]": "btn btn-primary",
        "input[type=password]": "form-control",
        "input[type=file]": "form-control-file",
        "select": "form-control",
        "textarea": "form-control",
    }
)