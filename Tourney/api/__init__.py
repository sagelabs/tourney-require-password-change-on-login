from flask import Blueprint, current_app
from flask_restx import Api

from Tourney.api.v1.awards import awards_namespace
from Tourney.api.v1.brackets import brackets_namespace
from Tourney.api.v1.challenges import challenges_namespace
from Tourney.api.v1.comments import comments_namespace
from Tourney.api.v1.config import configs_namespace
from Tourney.api.v1.exports import exports_namespace
from Tourney.api.v1.files import files_namespace
from Tourney.api.v1.flags import flags_namespace
from Tourney.api.v1.hints import hints_namespace
from Tourney.api.v1.notifications import notifications_namespace
from Tourney.api.v1.pages import pages_namespace
from Tourney.api.v1.schemas import (
    APIDetailedSuccessResponse,
    APISimpleErrorResponse,
    APISimpleSuccessResponse,
)
from Tourney.api.v1.scoreboard import scoreboard_namespace
from Tourney.api.v1.shares import shares_namespace
from Tourney.api.v1.solutions import solutions_namespace
from Tourney.api.v1.statistics import statistics_namespace
from Tourney.api.v1.submissions import submissions_namespace
from Tourney.api.v1.tags import tags_namespace
from Tourney.api.v1.teams import teams_namespace
from Tourney.api.v1.tokens import tokens_namespace
from Tourney.api.v1.topics import topics_namespace
from Tourney.api.v1.unlocks import unlocks_namespace
from Tourney.api.v1.users import users_namespace

api = Blueprint("api", __name__, url_prefix="/api/v1")
Tourney_API_v1 = Api(
    api,
    version="v1",
    doc=current_app.config.get("SWAGGER_UI_ENDPOINT"),
    authorizations={
        "AccessToken": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Generate access token in the settings page of your user account.",
        },
    },
    security=["AccessToken"],
)

Tourney_API_v1.schema_model("APISimpleErrorResponse", APISimpleErrorResponse.schema())
Tourney_API_v1.schema_model(
    "APIDetailedSuccessResponse", APIDetailedSuccessResponse.schema()
)
Tourney_API_v1.schema_model("APISimpleSuccessResponse", APISimpleSuccessResponse.schema())

Tourney_API_v1.add_namespace(challenges_namespace, "/challenges")
Tourney_API_v1.add_namespace(tags_namespace, "/tags")
Tourney_API_v1.add_namespace(topics_namespace, "/topics")
Tourney_API_v1.add_namespace(awards_namespace, "/awards")
Tourney_API_v1.add_namespace(hints_namespace, "/hints")
Tourney_API_v1.add_namespace(flags_namespace, "/flags")
Tourney_API_v1.add_namespace(submissions_namespace, "/submissions")
Tourney_API_v1.add_namespace(scoreboard_namespace, "/scoreboard")
Tourney_API_v1.add_namespace(teams_namespace, "/teams")
Tourney_API_v1.add_namespace(users_namespace, "/users")
Tourney_API_v1.add_namespace(statistics_namespace, "/statistics")
Tourney_API_v1.add_namespace(files_namespace, "/files")
Tourney_API_v1.add_namespace(notifications_namespace, "/notifications")
Tourney_API_v1.add_namespace(configs_namespace, "/configs")
Tourney_API_v1.add_namespace(pages_namespace, "/pages")
Tourney_API_v1.add_namespace(unlocks_namespace, "/unlocks")
Tourney_API_v1.add_namespace(tokens_namespace, "/tokens")
Tourney_API_v1.add_namespace(comments_namespace, "/comments")
Tourney_API_v1.add_namespace(shares_namespace, "/shares")
Tourney_API_v1.add_namespace(brackets_namespace, "/brackets")
Tourney_API_v1.add_namespace(exports_namespace, "/exports")
Tourney_API_v1.add_namespace(solutions_namespace, "/solutions")
