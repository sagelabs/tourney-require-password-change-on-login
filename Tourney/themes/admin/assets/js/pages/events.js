import $ from "jquery";
import events from "../compat/events";
import Tourney from "../../compat/Tourney";

$(() => {
  events(Tourney.config.urlRoot);
});
