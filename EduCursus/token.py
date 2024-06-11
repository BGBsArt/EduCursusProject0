from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class TokenGenerator(PasswordResetTokenGenerator) :
    def _make_hash_value(self, user, timestamp) :
        return(
            text_type(user.pk) + text_type(timestamp)
        )   # Token unique de type texte à chaque utilisateur

    # Création d'une instance de la classe pour pouvoir  l'importer dans views
generatorToken = TokenGenerator()