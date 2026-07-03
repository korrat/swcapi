from easyverein import BearerToken
from swcapi.config import settings


def handle_token_refresh(new_token: BearerToken) -> None:
    """
    Callback function to handle token refresh from the EasyvereinAPI.
    Saves the new bearer token into the configuration secrets.

    :param new_token: The new bearer token returned by the API.
    """
    print(f"Token refreshed: {new_token.Bearer}")
    settings.apikey = new_token.Bearer
