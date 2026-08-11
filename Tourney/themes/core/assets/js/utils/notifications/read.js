import Alpine from "alpinejs";
import Tourney from "../../index";

export default () => {
  Tourney._functions.events.eventCount = count => {
    Alpine.store("unread_count", count);
  };

  Tourney._functions.events.eventRead = eventId => {
    Tourney.events.counter.read.add(eventId);
    let count = Tourney.events.counter.unread.getAll().length;
    Tourney.events.controller.broadcast("counter", { count: count });
    Alpine.store("unread_count", count);
  };

  document.addEventListener("alpine:init", () => {
    Tourney._functions.events.eventCount(Tourney.events.counter.unread.getAll().length);
  });
};
