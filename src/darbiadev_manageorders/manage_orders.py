"""A wrapper for ManageOrders' API."""

from typing import Self

import requests


class ManageOrdersServices:
    """A class wrapping ManageOrders' API.

    This class wraps ManageOrders' API.
    """

    def __init__(self: Self, base_url: str, username: str, password: str) -> None:
        self._base_url: str = base_url
        self.__username: str = username
        self.__password: str = password

        self.__id_token: str | None = None
        self.__refresh_token: str | None = None
        self.__access_token: str | None = None

    def _make_request(  # noqa: PLR0913 -- will go away with the below fixme
        self: Self,
        method: str,
        path: str,
        headers: dict[str, str] | None = None,
        data: dict[str, str] | None = None,
        authenticated: bool = True,  # noqa: FBT001,FBT002 -- fixme: reauthenticate if needed
    ) -> dict[str, str]:
        args = {
            "method": method,
            "url": self._base_url + path,
            "headers": headers or {},
        }

        if authenticated:
            args["headers"]["Authorization"] = self.__id_token

        if data is not None:
            args["json"] = data

        response = requests.request(**args)
        response.raise_for_status()
        return response.json()

    def _update_token(
        self: Self,
    ) -> None:
        response = self._make_request(
            method="post",
            path="signin",
            data={"username": self.__username, "password": self.__password},
            authenticated=False,
        )
        self.__id_token = response["id_token"]
        self.__refresh_token = response["refresh_token"]
        self.__access_token = response["access_token"]
