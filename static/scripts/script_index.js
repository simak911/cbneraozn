async function fetchData() {
  try {
    const res = await fetch('/getall');
    const data = await res.json();
    const top = data.top;
    const left = data.left;
    const right = data.right;
    const topcont = document.getElementById('topcont');
    const rightcont = document.getElementById('rightcont');
    const leftcont = document.getElementById('leftcont');
    topcont.innerText = top;
    leftcont.innerText = left;
    rightcont.innerText = right;
  } catch (e) {
    console.error(e);
  }
}

let intervalId;

function startPolling() {
  intervalId = setInterval(fetchData, 3000); 
}

startPolling();
