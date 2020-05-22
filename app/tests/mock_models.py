class mock_context:
    def __init__(self, headers):
        self.context = {}
        self.headers = mock_header(headers)
        self.context["request"] = self.headers


class mock_header:
    def __init__(self, headers):
        self.headers = headers

# Example usage:-

# headers = {
#   "authorization": "Bearer " + user.access_token
# }
# req = mock_context(headers)
# resolved_user = resolve_me(None, req)