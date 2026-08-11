import Alpine from "alpinejs";
import Tourney from "./index";

window.Tourney = Tourney;
window.Alpine = Alpine;

// Get unread notifications from server
let lastId = Tourney.events.counter.read.getLast();
Tourney.fetch(`/api/v1/notifications?since_id=${lastId}`)
  .then(response => {
    return response.json();
  })
  .then(response => {
    // Get notifications from server and mark them as read
    let notifications = response.data;
    let read = Tourney.events.counter.read.getAll();
    notifications.forEach(n => {
      read.push(n.id);
    });
    Tourney.events.counter.read.setAll(read);

    // Mark all unread as read
    Tourney.events.counter.unread.readAll();

    // Broadcast our new count (which should be 0)
    let count = Tourney.events.counter.unread.getAll().length;
    Tourney.events.controller.broadcast("counter", {
      count: count,
    });
    Alpine.store("unread_count", count);
  });

Alpine.start();
