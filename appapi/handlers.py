from rest_framework.views import exception_handler
def custom_exception_handler(exc, context):
    exc_handlers = {
        "Http404":_handle_not_found,
        "PermissionDenied":_handle_permission_denied,
    }
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status'] = response.status_code
    exception = exc.__class__.__name__ 
    if exception in exc_handlers:
        del response.data["detail"]
        return exc_handlers[exception](exc,context,response)
    return response
def _handle_not_found(exc,context,response):
    response.data["info"] = "Not Found"
    return response
def _handle_permission_denied(exec,context,response):
    response.data["info"] = "Access Denied"
    return response