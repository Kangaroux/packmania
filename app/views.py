from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from lib.api import APIView


def main(request):
  return render(request, "main.html")

def csrf_handler(request, reason=""):
  return APIView.error("CSRF token is missing or invalid.", status=403)


# Dummy 500 error view
class Dummy500View(APIView):
  def get(self, request):
    raise Exception("Fake exception from the dummy 500 error view")


# Dummy CSRF protected view
class DummyCSRFView(APIView):
  def post(self, request):
    return self.ok()