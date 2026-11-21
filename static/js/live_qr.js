
const root = document.getElementById("live");
const sessionId = root.dataset.sessionId;
const countdownEl = document.getElementById("countdown");

let qr = null;
let currentToken = null;
let secondsLeft = 0;
let ended = false;

function drawQR(token) {
  if (token === currentToken) return;  // same code, nothing to redraw
  currentToken = token;
  if (qr === null) {
    qr = new QRCode(document.getElementById("qrcode"), { text: token, width: 320, height: 320 });
  } else {
    qr.makeCode(token);
  }
}

function showEnded() {
  ended = true;
  document.getElementById("ended-msg").classList.remove("d-none");
  document.getElementById("qrcode").classList.add("d-none");
  countdownEl.textContent = "-";
}

async function refreshToken() {
  if (ended) return;
  const res = await fetch(`/faculty/session/${sessionId}/qr`);
  const data = await res.json();
  if (data.token === null) {           // the server says the session is over
    showEnded();
    return;
  }
  drawQR(data.token);
  secondsLeft = data.expires_in;
  countdownEl.textContent = secondsLeft;
}

async function refreshList() {
    if (ended) return;
    const res = await fetch(`/faculty/session/${sessionId}/live`);
    const data = await res.json();
    const list = document.getElementById("marked-list");
    list.innerHTML = "";
    let present = 0, flagged = 0;
    data.marked.forEach((m) => {
      if (m.status === "present") present++;
      if (m.status === "flagged") flagged++;
      const li = document.createElement("li");
      li.className = "list-group-item d-flex justify-content-between align-items-center";
      const name = document.createElement("span");
      name.textContent = m.name + " (" + m.marked_at + ")"; // textContent keeps names safe
      const badge = document.createElement("span");
      badge.className = "badge " + (m.status === "present" ? "bg-success" : "bg-warning text-dark");
      badge.textContent = m.status;
      li.append(name, badge);
      list.appendChild(li);
    });
    document.getElementById("count-present").textContent = present;
    document.getElementById("count-flagged").textContent = flagged;
    if (data.summary) {
      document.getElementById("count-total").textContent = data.summary.total_students;
    }
}

// every second: tick the countdown; when it reaches 0, ask for the new code
setInterval(() => {
  if (ended) return;
  secondsLeft = Math.max(0, secondsLeft - 1);
  countdownEl.textContent = secondsLeft;
  if (secondsLeft === 0) refreshToken();
}, 1000);

// every 3 seconds: refresh the list of students
setInterval(refreshList, 3000);

document.getElementById("btn-end").addEventListener("click", async () => {
 if (!confirm("End this attendance session?")) return;
 await fetch(`/faculty/session/${sessionId}/end`, { method: "POST" });
 window.location.href = `/faculty/session/${sessionId}/report`;
});

refreshToken();
refreshList();
