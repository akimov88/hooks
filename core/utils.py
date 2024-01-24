from keycloak import KeycloakOpenID


def get_client():
    client = KeycloakOpenID(
        server_url='http://localhost:8080/auth/',
        realm_name='django_realm',
        client_id='django_client',
        client_secret_key='SLa5AAxZyh7Yqn0jv9UsJcIUh1TbyeXg',
    )
    return client
