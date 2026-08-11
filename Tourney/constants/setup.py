from Tourney.constants.options import (
    AccountVisibilityTypes,
    ChallengeVisibilityTypes,
    RegistrationVisibilityTypes,
    ScoreVisibilityTypes,
    UserModeTypes,
)
from Tourney.constants.themes import DEFAULT_THEME

DEFAULTS = {
    # General Settings
    "ctf_name": "Tourney",
    "user_mode": UserModeTypes.USERS,
    # Visual/Style Settings
    "ctf_theme": DEFAULT_THEME,
    # Visibility Settings
    "challenge_visibility": ChallengeVisibilityTypes.PRIVATE,
    "registration_visibility": RegistrationVisibilityTypes.PUBLIC,
    "score_visibility": ScoreVisibilityTypes.PUBLIC,
    "account_visibility": AccountVisibilityTypes.PUBLIC,
}
