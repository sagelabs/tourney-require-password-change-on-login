import Tourney from "../index";
import lolight from "lolight";

export default () => {
  if (
    // default to true if config is not defined yet
    !Tourney.config.themeSettings.hasOwnProperty("use_builtin_code_highlighter") ||
    Tourney.config.themeSettings.use_builtin_code_highlighter === true
  ) {
    lolight("pre code");
  }
};
