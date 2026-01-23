let contents = ['','',''];
let indexik = 0;

async function fetchData() {
  try {
    const res = await fetch('/getall');
    const data = await res.json();
    contents[0] = data.top;
    contents[1] = data.left;
    contents[2] = data.right;
  } catch (e) {
    console.error(e);
  }
}

function show() {
  const titelem = document.getElementById('titulek');
  const contelem = document.getElementById('contents');
  while (contents[indexik] == '') {
    indexik = (indexik+1) % 3;
  }
  if (indexik == 0) {
    titelem.innerText = 'Pravidelné akce:';
  }
  else if (indexik == 1) {
    titelem.innerText = 'Další oznámení:';
  }
  else {
    titelem.innerText = 'Blížící se akce:';
  };
  contelem.innerText = contents[indexik];  
  indexik = (indexik+1) % 3;
}

function startPolling() {
  interval1 = setInterval(fetchData, 2999); 
}

function startShowing() {
  interval2 = setInterval(show, 7000);
}

startPolling();
startShowing();
