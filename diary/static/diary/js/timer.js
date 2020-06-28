 let init = 0
 let startDate
 let clockTimer


 function startTIME() {
  let thisDate = new Date();
  let t = thisDate.getTime() - startDate.getTime();
  t = Math.floor (t/1000);
  let s = t%60; t-=s;
  t = Math.floor (t/60);
  let m = t%60; t-=m;
  t = Math.floor (t/60);
  if (m<10) m='0'+m;
  if (s<10) s='0'+s;
  if (init === 1) document.clockform.clock.value = m + ':' + s
  clockTimer = setTimeout("startTIME()",10);
 }

 function findTIME() {
  if (init === 0) {
   startDate = new Date();
   startTIME();
   init = 1;
  }
  else {
    let getTime = $('#clock').val();
    clearTimeout(clockTimer)
    $('input#update-rest-time').val(getTime)
  }
 }
