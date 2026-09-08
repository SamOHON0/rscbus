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

  // Enquiry form. There is no booking system and no backend on this build,
  // so the form composes an email to the office instead. To move to a real
  // endpoint later, set data-endpoint on the form and POST instead.
  var form = document.querySelector('form.enq');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var get = function (n) {
        var el = form.querySelector('[name="' + n + '"]');
        return el ? el.value.trim() : '';
      };
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
      var subject = 'Website enquiry - ' + (get('service') || 'Bus hire') +
        (get('date') ? ' - ' + get('date') : '');
      window.location.href = 'mailto:office@rscbuses.ie?subject=' +
        encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
      var note = form.querySelector('.formnote');
      if (note) {
        note.textContent = 'Opening your email app with the details filled in. ' +
          'If nothing happens, email office@rscbuses.ie directly.';
        note.style.color = '#14314f';
        note.style.fontWeight = '700';
      }
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
