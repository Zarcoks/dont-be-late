from django.http import HttpResponseRedirect, HttpResponse


def hx_or_http_redirect(request, url):
    if request.headers.get("HX-Request"):
        return HttpResponse(headers={"HX-Redirect": url})
    return HttpResponseRedirect(url)