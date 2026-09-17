/* RSC Buses - shared site behaviour */
(function () {
  // Mobile nav. The menu markup sits inside the sticky <header>, so it
  // opens directly under the bar no matter how far the page is scrolled.
  var burger = document.querySelector('.burger');
  var menu = document.querySelector('.mobile-menu');
  if (burger && menu) {
    var setOpen = function (open) {
      menu.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    burger.addEventListener('click', function (e) {
      e.stopPropagation();
      setOpen(!menu.classList.contains('open'));
    });
    // Close after tapping a link, on Escape, on a tap outside, and if the
    // window is widened back to the desktop nav.
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) { setOpen(false); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { setOpen(false); }
    });
    document.addEventListener('click', function (e) {
      if (menu.classList.contains('open') && !menu.contains(e.target) &&
          !burger.contains(e.target)) { setOpen(false); }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1000) { setOpen(false); }
    });
  }

  // Enquiry form. Posts to Formspree over AJAX so the customer stays on the
  // page instead of being bounced to formspree.io. The form also carries
  // action/method, so if this script never runs the browser still submits it
  // natively. If the post fails we hand back a mailto so the enquiry is not
  // silently lost.
  var form = document.querySelector('form.enq');
  if (form) {
    var get = function (n) {
      var el = form.querySelector('[name="' + n + '"]');
      return el ? el.value.trim() : '';
    };

    var subjectLine = function () {
      return 'Website enquiry - ' + (get('service') || 'Bus hire') +
        (get('date') ? ' - ' + get('date') : '');
    };

    var mailtoFallback = function () {
      var lines = [
        'Name: ' + get('name'),
        'Phone: ' + get('phone'),
        'Email: ' + get('email'),
        'Service: ' + get('service'),
        'Date: ' + get('date'),
        'Passengers: ' + get('passengers'),
        'Pick-up: ' + get('pickup'),
        'Destination: ' + get('destination'),
        '',
        'Details:',
        get('message')
      ];
      return 'mailto:office@rscbuses.ie?subject=' + encodeURIComponent(subjectLine()) +
        '&body=' + encodeURIComponent(lines.join('\n'));
    };

    var say = function (html) {
      var note = form.querySelector('.formnote');
      if (!note) { return; }
      note.innerHTML = html;
      note.style.color = '#14314f';
      note.style.fontWeight = '700';
    };

    form.addEventListener('submit', function (e) {
      // No fetch means an old browser. Let it post the form the normal way.
      if (!window.fetch || !window.FormData) { return; }
      e.preventDefault();

      var btn = form.querySelector('[type="submit"]');
      var label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending...'; }

      // Give the office a useful subject line rather than a generic one.
      var subj = form.querySelector('[name="_subject"]');
      if (subj) { subj.value = subjectLine(); }

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      }).then(function (res) {
        if (!res.ok) { throw new Error('rejected'); }
        form.reset();
        say('Thanks, that is with us. We will come back to you, usually the same day.');
        if (btn) { btn.textContent = 'Enquiry sent'; }
      }).catch(function () {
        say('Sorry, that did not send. <a href="' + mailtoFallback() + '">Send it by email instead</a>, ' +
          'or ring us on <a href="tel:+353871817897">087 181 7897</a>.');
        if (btn) { btn.disabled = false; btn.textContent = label; }
      });
    });
  }


  // Pre-select the service when arriving from /contact/?service=slug
  if (form) {
    var slug = new URLSearchParams(window.location.search).get('service');
    var sel = form.querySelector('[name="service"]');
    if (slug && sel) {
      var want = slug.replace(/-/g, ' ');
      for (var s = 0; s < sel.options.length; s++) {
        if (sel.options[s].value.toLowerCase().replace(/[^a-z]+/g, '') ===
            want.toLowerCase().replace(/[^a-z]+/g, '')) { sel.selectedIndex = s; break; }
      }
    }
  }

  // year in footer
  var y = document.querySelectorAll('[data-year]');
  for (var i = 0; i < y.length; i++) { y[i].textContent = new Date().getFullYear(); }
})();
