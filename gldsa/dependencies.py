from typing import *
import os
import logging
from datetime import datetime

from gldsa import __name__, __version__, __url__

logger = logging.getLogger(__name__)


class Dependency:
    def __init__(self, **kwargs):
        self.namespace = kwargs.get("namespace")
        self.name = kwargs.get("name")
        self.version = kwargs.get("version")
        self.manager = kwargs.get("manager")
        self.path = kwargs.get("path")

    def getName(self):
        if self.manager == "maven":
            return f"{self.namespace}.{self.name}"
        return self.name

    def getPurl(self):
        result = f"pkg:"
        if self.manager:
            result += f"{self.manager}/"
        if self.namespace:
            result += f"{self.namespace}/"
        result += f"{self.name}"
        if self.version:
            result += f"@{self.version}"
            
        return result

    def __str__(self) -> str:
        """Return a string representation of the dependency"""
        return self.getPurl()


def exportDependencies(source: str, dependencies: list[Dependency], **kwargs) -> dict:
    """ Create a dependency graph submission JSON payload for GitHub
    """
    resolved = {}
    for dep in dependencies:
        name = dep.getName()
        purl = dep.getPurl()
        resolved[name] = {"package_url": purl}

    data = {
        "version": 0,
        "sha": kwargs.get("sha"),
        "ref": kwargs.get("ref"),
        "job": {"correlator": __name__, "id": __name__},
        "detector": {"name": __name__, "version": __version__, "url": __url__},
        "scanned": datetime.now().isoformat(),
        "manifests": {
            __name__: {
                "name": __name__,
                "file": {
                    "source_location": source,
                },
                "resolved": resolved,
            }
        },
    }
    return data
