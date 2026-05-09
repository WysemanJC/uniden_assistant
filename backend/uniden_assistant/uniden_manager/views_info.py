"""
API endpoints for application information (version, health, status).
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from uniden_assistant.version import VERSION_INFO


class VersionView(APIView):
    """Return application version information."""

    def get(self, request):
        return Response(
            {
                "version": VERSION_INFO["full"],
                "semver": VERSION_INFO["semver"],
                "is_release": VERSION_INFO["is_release"],
                "pre_release": VERSION_INFO["pre_release"],
                "build_metadata": VERSION_INFO["build_metadata"],
            }
        )


class HealthView(APIView):
    """Health check endpoint."""

    def get(self, request):
        return Response(
            {
                "status": "healthy",
                "version": VERSION_INFO["full"],
            }
        )
