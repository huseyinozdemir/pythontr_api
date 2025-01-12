import ssl
from django.core.mail.backends.smtp import EmailBackend


class CustomEmailBackend(EmailBackend):
    def open(self):
        """
        Override to customize the SSL context and open the connection.
        """
        if self.connection:
            return self.connection

        # Custom SSL context
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

        try:
            self.connection = self.connection_class(
                self.host, self.port, timeout=self.timeout
            )
            if self.use_tls:
                self.connection.starttls(context=self.ssl_context)
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception as e:
            if self.fail_silently:
                return False
            raise e
