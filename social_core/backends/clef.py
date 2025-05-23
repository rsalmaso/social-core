"""
Clef OAuth support.

This contribution adds support for Clef OAuth service. The settings
SOCIAL_AUTH_CLEF_KEY and SOCIAL_AUTH_CLEF_SECRET must be defined with the
values given by Clef application registration process.
"""

from .oauth import BaseOAuth2


class ClefOAuth2(BaseOAuth2):
    """Clef OAuth authentication backend"""

    name = "clef"
    AUTHORIZATION_URL = "https://clef.io/iframes/qr"
    ACCESS_TOKEN_URL = "https://clef.io/api/v1/authorize"
    SCOPE_SEPARATOR = ","

    def auth_params(self, *args, **kwargs):
        params = super().auth_params(*args, **kwargs)
        params["app_id"] = params.pop("client_id")
        params["redirect_url"] = params.pop("redirect_uri")
        return params

    def get_user_id(self, response, details):  # type: ignore[reportIncompatibleMethodOverride]
        return details.get("info").get("id")

    def get_user_details(self, response):
        """Return user details from Github account"""
        info = response.get("info")
        fullname, first_name, last_name = self.get_user_names(
            first_name=info.get("first_name"), last_name=info.get("last_name")
        )

        email = info.get("email", "")
        username = email.split("@", 1)[0] if email else info.get("id")

        return {
            "username": username,
            "email": email,
            "fullname": fullname,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": info.get("phone_number", ""),
        }

    def user_data(self, access_token, *args, **kwargs):
        return self.get_json(
            "https://clef.io/api/v1/info", params={"access_token": access_token}
        )
