async function fetchData() {
  try {
    const res = await fetch('/api/data');
    const data = await res.json();
    updateUI(data);
  } catch (e) {
    console.error(e);
  }
}

let intervalId;

function startPolling() {
  intervalId = setInterval(fetchData, 3000); // N = 3s
}



startPolling();
