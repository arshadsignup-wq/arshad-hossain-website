/* Formspree AJAX submit — keeps people on the page instead of bouncing
   them to Formspree's own thank-you screen. Falls back to a normal POST
   if JavaScript is off, because the <form> keeps its action and method. */
function handleForm(e) {
  e.preventDefault();

  var form = e.target;
  var status = form.querySelector('.form-status');
  var btn = form.querySelector('button[type="submit"]');
  var label = btn.textContent;

  btn.disabled = true;
  btn.textContent = 'Sending…';
  status.className = 'form-status';

  // Which page produced this lead. Without it there is no way to tell
  // whether a service page, a case study or the blog is doing the work.
  var data = new FormData(form);
  data.append('page', window.location.pathname);
  if (document.referrer) data.append('referrer', document.referrer);

  fetch(form.action, {
    method: 'POST',
    body: data,
    headers: { 'Accept': 'application/json' }
  })
    .then(function (res) {
      if (res.ok) {
        form.reset();
        status.className = 'form-status show ok';
        status.textContent = 'Got it — thanks. I read these myself and will reply within one business day.';
        return;
      }
      return res.json().then(function (data) {
        throw new Error(
          data && data.errors
            ? data.errors.map(function (x) { return x.message; }).join(', ')
            : 'That did not go through.'
        );
      });
    })
    .catch(function (err) {
      status.className = 'form-status show err';
      status.textContent = err.message + ' Please try again, or reach me on LinkedIn.';
    })
    .then(function () {
      btn.disabled = false;
      btn.textContent = label;
    });
}
