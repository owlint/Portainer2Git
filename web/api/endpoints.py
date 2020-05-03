# Third Party
from flask_restful import Resource, reqparse
from infrastructure.application_services.application_services import (
    ApplicationServices,
)
from infrastructure.services.services import Services


class CreateUser(Resource):
    def __init__(self):
        super().__init__()

        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "first_name", type=str, location="json", required=True
        )
        self.parser.add_argument(
            "last_name", type=str, location="json", required=True
        )
        self.parser.add_argument(
            "email", type=str, location="json", required=True
        )
        self.parser.add_argument(
            "password", type=str, location="json", required=True
        )
        self.parser.add_argument(
            "is_admin", type=bool, location="json", required=True
        )

    def post(self):
        args = self.parser.parse_args()

        try:
            user_id = self.create_user(args)
            Services.logger().info(
                f"New user with email {args['email']} created"
            )
            return {"user_id": user_id}
        except ValueError:
            Services.logger().warning(
                f"Try to create already existing user with "
                f"email {args['email']}"
            )
            return {"message": "This user already exists"}, 501
        except Exception as ex:
            return {"message": ex.message}, 500

    def create_user(self, args):
        user_application_service = ApplicationServices.user()
        return user_application_service.create_user(
            args["first_name"],
            args["last_name"],
            args["email"],
            args["password"],
            args["is_admin"],
        )
