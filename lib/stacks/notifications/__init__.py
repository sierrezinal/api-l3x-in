from os import environ as env
from typing import Iterable

from aws_cdk import (
    aws_iam,
    aws_lambda,
    core,
)

from utils.cdk import (
    get_lambda,
    code_from_path,
)


class NotificationsStack(core.Stack):

    # pylint: disable=redefined-builtin
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.pushover = get_lambda(
            self,
            "%s-lambda-pushover" % id,
            code='lib/stacks/%s/lambdas' % id,
            handler="send_to_pushover.handler",
            environment={
                "PUSHOVER_TOKEN": env["PUSHOVER_TOKEN"],
                "PUSHOVER_USERKEY": env["PUSHOVER_USERKEY"],
                "LAMBDA_FUNCTIONS_LOG_LEVEL": "INFO",
            })

        self.mailjet = get_lambda(
            self,
            "%s-lambda-mailjet" % id,
            code='lib/stacks/%s/lambdas' % id,
            handler="send_to_mailjet.handler",
            environment={
                "MAILJET_API_KEY": env["MAILJET_API_KEY"],
                "MAILJET_API_SECRET": env["MAILJET_API_SECRET"],
                "MAILJET_DEFAULT_TO_ADDRESS": env["MAILJET_DEFAULT_TO_ADDRESS"],
                "MAILJET_FROM_ADDRESS": env["MAILJET_FROM_ADDRESS"],
            })

        self.mailjet.grant_invoke(aws_iam.User(self, f"{id}-mail-sender"))
