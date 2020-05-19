from validators.user_validation import validate_user_model


def resolve_register_user(_, info, data):
    """Resolver for registering a new user"""
    user = validate_user_model(data)

    saved_user = user.save()

    print("Saved user: {}".format(saved_user))

    # TODO: Encode and return token if successful
