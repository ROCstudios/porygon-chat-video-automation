def main():
    return 'stringer'

if __name__ == "__main__":
    main()


# user will call in from the client, we need to have a flask endpoint that will recquest the initial login information

# we will then send the oauth information to the client, from there the user will be directed to the redirect url

# we will take that url and extract the code in the client

# we will then send that code to our backend and we will use that code to get the access token and refresh token

# this will be stored locally for subsequent requests until an error is thrown.
