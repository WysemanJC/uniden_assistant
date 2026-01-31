import json
import urllib.request
from urllib.error import HTTPError, URLError
from rest_framework.views import APIView
from rest_framework.response import Response


class ProxyAPIView(APIView):
    """Proxy API that forwards requests to internal tiered APIs without direct DB access."""

    upstream_prefix = ''

    def _build_upstream_url(self, request, path_suffix=''):
        base = request.build_absolute_uri('/')[:-1]
        query = request.META.get('QUERY_STRING', '')
        path = f"/api/{self.upstream_prefix}{path_suffix}"
        url = f"{base}{path}"
        if query:
            url = f"{url}?{query}"
        return url

    def _proxy(self, request, path_suffix=''):
        url = self._build_upstream_url(request, path_suffix)
        data = request.body if request.method in ['POST', 'PUT', 'PATCH'] else None
        headers = {
            'Content-Type': request.META.get('CONTENT_TYPE', 'application/json'),
        }
        req = urllib.request.Request(url, data=data, headers=headers, method=request.method)
        try:
            with urllib.request.urlopen(req) as resp:
                content = resp.read()
                try:
                    payload = json.loads(content.decode('utf-8'))
                    return Response(payload, status=resp.status)
                except json.JSONDecodeError:
                    return Response(content.decode('utf-8'), status=resp.status)
        except HTTPError as exc:
            content = exc.read().decode('utf-8')
            try:
                payload = json.loads(content)
                return Response(payload, status=exc.code)
            except json.JSONDecodeError:
                return Response({'error': content}, status=exc.code)
        except URLError as exc:
            return Response({'error': str(exc)}, status=502)


class HPDBProxyView(ProxyAPIView):
    upstream_prefix = 'hpdb/'

    def get(self, request, path=''):
        return self._proxy(request, path)

    def post(self, request, path=''):
        return self._proxy(request, path)


class UserSettingsProxyView(ProxyAPIView):
    upstream_prefix = 'usersettings/'

    def get(self, request, path=''):
        return self._proxy(request, path)

    def post(self, request, path=''):
        return self._proxy(request, path)

    def put(self, request, path=''):
        return self._proxy(request, path)

    def patch(self, request, path=''):
        return self._proxy(request, path)

    def delete(self, request, path=''):
        return self._proxy(request, path)


class AppConfigProxyView(ProxyAPIView):
    upstream_prefix = 'appconfig/'

    def get(self, request, path=''):
        return self._proxy(request, path)
