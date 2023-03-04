import sys
from io import StringIO

from django.urls import reverse


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout


def make_url(request, url_name, *args):
    rurl = reverse(url_name, args=args)
    url = request.build_absolute_uri(rurl)
    return url


def make_task_url(task, request, path):
    # task_url = f"{request.build_absolute_uri()}{task.id}"
    task_url = make_url(request, path, task.id)
    return task_url
