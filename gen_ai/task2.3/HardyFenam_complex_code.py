"""
open_session() function from the Flask library. After simplification with ChatGPT.
"""

class SecureCookieSessionInterface(SessionInterface):
    """The default session interface that stores sessions in signed cookies
    through the :mod:`itsdangerous` module.
    """

    def open_session(self, app: Flask, request: Request) -> SecureCookieSession | None:
    s = self.get_signing_serializer(app)
    if not s:
        return None  # Return early if signing serializer is unavailable

    session_cookie = request.cookies.get(self.get_cookie_name(app))
    if not session_cookie:
        return self.session_class()  # No session cookie, return a new session

    # Compute max age once
    max_age = app.permanent_session_lifetime.total_seconds()

    try:
        data = s.loads(session_cookie, max_age=max_age)
    except BadSignature:
        return self.session_class()  # If tampered or expired, return a new session

    return self.session_class(data)  # Valid session, return it with stored data
