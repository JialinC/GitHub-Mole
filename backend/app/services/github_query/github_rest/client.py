# class RESTClient:
#     """
#     A client for interacting with the GitHub REST API.
#     Handles the construction and execution of RESTful requests with provided authentication.
#     """

#     def __init__(
#         self,
#         protocol: str = "https",
#         host: str = "api.github.com",
#         is_enterprise: bool = False,
#         authenticator: Authenticator = None,
#     ) -> None:
#         """
#         Initialization with protocol, host, and whether the GitHub instance is Enterprise
#         Requires an Authenticator to be provided for handling authentication
#         Args:
#             protocol: Protocol for the server
#             host: Host for the server
#             is_enterprise: Is the host running on Enterprise Version?
#             authenticator: Authenticator for the client
#         """
#         self._protocol = protocol
#         self._host = host
#         self._is_enterprise = is_enterprise

#         if authenticator is None:
#             raise InvalidAuthenticationError("Authentication needs to be specified")

#         self._authenticator = authenticator

#     def _base_path(self) -> str:
#         """
#         Constructs the base path for REST API requests, differing based on whether it's an enterprise instance
#         Returns:
#             Base path for requests
#         """
#         return (
#             f"{self._protocol}://{self._host}/api/v3/"
#             if self._is_enterprise
#             else f"{self._protocol}://{self._host}/"
#         )

#     def _generate_headers(self, **kwargs):
#         """
#         Generates headers for the request including authorization and any additional provided headers
#         Args:
#             **kwargs: Headers

#         Returns:
#             Headers required for requests
#         """
#         headers = {}

#         headers.update(self._authenticator.get_authorization_header())
#         headers.update(kwargs)

#         return headers

#     def get(self, path: str, **kwargs):
#         """
#         Makes a GET request to the specified path, handling rate limits and retrying as needed
#         Args:
#             path: API path to hit
#             **kwargs: Arguments for the GET request

#         Returns:
#             Response as a JSON
#         """
#         path = path[1:] if path.startswith("/") else path
#         kwargs.setdefault("headers", {})

#         kwargs["headers"] = self._generate_headers(**kwargs["headers"])

#         response = None
#         json_response = None

#         i = -1

#         while json_response is None and i < 10:
#             i += 1

#             try:
#                 response = requests.get(f"{self._base_path()}{path}", **kwargs)

#                 if int(response.headers["X-RateLimit-Remaining"]) < 2:
#                     reset_at = datetime.fromtimestamp(
#                         int(response.headers["X-RateLimit-Reset"])
#                     )
#                     current_time = datetime.utcnow()

#                     seconds = (reset_at - current_time).total_seconds()
#                     print(f"waiting for {seconds}s.")
#                     time.sleep(seconds + 5)

#                     json_response = None
#                     continue

#                 if response.status_code == 202:
#                     json_response = None
#                     time.sleep(randint(0, i))

#                     continue

#                 json_response = response.json()

#             except RequestException:
#                 raise QueryFailedException(response=response)

#         return json_response
