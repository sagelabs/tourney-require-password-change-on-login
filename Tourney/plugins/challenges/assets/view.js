Tourney._internal.challenge.data = undefined;

// TODO: Remove in Tourney v4.0
Tourney._internal.challenge.renderer = null;

Tourney._internal.challenge.preRender = function() {};

// TODO: Remove in Tourney v4.0
Tourney._internal.challenge.render = null;

Tourney._internal.challenge.postRender = function() {};

Tourney._internal.challenge.submit = function(preview) {
  var challenge_id = parseInt(Tourney.lib.$("#challenge-id").val());
  var submission = Tourney.lib.$("#challenge-input").val();

  var body = {
    challenge_id: challenge_id,
    submission: submission
  };
  var params = {};
  if (preview) {
    params["preview"] = true;
  }

  return Tourney.api.post_challenge_attempt(params, body).then(function(response) {
    if (response.status === 429) {
      // User was ratelimited but process response
      return response;
    }
    if (response.status === 403) {
      // User is not logged in or CTF is paused.
      return response;
    }
    return response;
  });
};
