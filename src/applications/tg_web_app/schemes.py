from applications.auth.schemas import JWTPairToken


class JWTPairTokenTgAuth(JWTPairToken):
    created: bool = False
