/* ===== RUSTEAM Landing — Main JS ===== */

(function () {
  'use strict';

  /* ---------- SMOOTH SCROLL ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var targetId = this.getAttribute('href');
      if (targetId === '#') return;
      var target = document.querySelector(targetId);
      if (!target) return;
      e.preventDefault();
      var headerH = document.querySelector('.header').offsetHeight;
      var top = target.getBoundingClientRect().top + window.pageYOffset - headerH - 16;
      window.scrollTo({ top: top, behavior: 'smooth' });

      // close mobile nav if open
      closeMobileNav();
    });
  });

  /* ---------- MOBILE NAV ---------- */
  var burger = document.getElementById('burger');
  var mobileNav = document.getElementById('mobileNav');

  function closeMobileNav() {
    if (burger) burger.classList.remove('active');
    if (mobileNav) mobileNav.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (burger) {
    burger.addEventListener('click', function () {
      burger.classList.toggle('active');
      mobileNav.classList.toggle('active');
      document.body.style.overflow = mobileNav.classList.contains('active') ? 'hidden' : '';
    });
  }

  if (mobileNav) {
    mobileNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeMobileNav);
    });
  }

  /* ---------- HEADER SCROLL EFFECT ---------- */
  var header = document.getElementById('header');
  var lastScroll = 0;

  window.addEventListener('scroll', function () {
    var scrollY = window.pageYOffset;
    if (scrollY > 100) {
      header.style.background = 'rgba(10, 10, 15, 0.95)';
    } else {
      header.style.background = 'rgba(10, 10, 15, 0.85)';
    }
    lastScroll = scrollY;
  }, { passive: true });

  /* ---------- SCROLL ANIMATIONS (IntersectionObserver) ---------- */
  var animateEls = document.querySelectorAll('[data-animate]');

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var el = entry.target;
          var delay = parseInt(el.getAttribute('data-delay') || '0', 10);
          setTimeout(function () {
            el.classList.add('animated');
          }, delay);
          observer.unobserve(el);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -40px 0px'
    });

    animateEls.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    // Fallback: show all immediately
    animateEls.forEach(function (el) {
      el.classList.add('animated');
    });
  }

  /* ---------- FAQ ACCORDION ---------- */
  var faqItems = document.querySelectorAll('.faq__question');

  faqItems.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = this.closest('.faq__item');
      var isOpen = item.classList.contains('active');

      // Close all
      document.querySelectorAll('.faq__item.active').forEach(function (openItem) {
        openItem.classList.remove('active');
        openItem.querySelector('.faq__question').setAttribute('aria-expanded', 'false');
      });

      // Toggle current
      if (!isOpen) {
        item.classList.add('active');
        this.setAttribute('aria-expanded', 'true');
      }
    });
  });

  /* ---------- YEAR CHECKER (проходной год) ---------- */
  var yearInput = document.getElementById('year');
  var yearHint = document.getElementById('yearHint');

  // Проходные годы — авто, которые можно ввезти с выгодной пошлиной
  // Для физ. лиц выгодны авто 3–5 лет (пониженная ставка ЕТТ)
  function checkYear(year) {
    var currentYear = new Date().getFullYear();
    var age = currentYear - year;

    if (year > currentYear) {
      return { pass: false, msg: 'Год ещё не наступил' };
    }
    if (year === currentYear || year === currentYear - 1) {
      return { pass: true, msg: 'Новый авто — проходной год. Пошлина по стандартной ставке.' };
    }
    if (age >= 3 && age <= 5) {
      return { pass: true, msg: 'Проходной год! Льготная ставка пошлины (1.5–2.5 EUR/см³). Максимальная выгода.' };
    }
    if (age > 5 && age <= 7) {
      return { pass: false, msg: 'Авто старше 5 лет — повышенная пошлина (3–3.6 EUR/см³). Менее выгодно.' };
    }
    if (age > 7) {
      return { pass: false, msg: 'Авто старше 7 лет — высокая пошлина + утилизационный сбор. Не рекомендуем.' };
    }
    return { pass: true, msg: 'Проходной год.' };
  }

  if (yearInput && yearHint) {
    yearInput.addEventListener('input', function () {
      var val = parseInt(this.value, 10);
      if (this.value.length === 4 && !isNaN(val)) {
        var result = checkYear(val);
        yearHint.textContent = (result.pass ? '✓ ' : '⚠ ') + result.msg;
        yearHint.style.color = result.pass ? 'var(--success)' : 'var(--accent)';
        yearHint.classList.add('visible');
      } else {
        yearHint.classList.remove('visible');
      }
    });
  }

  /* ---------- BUDGET FORMATTER ---------- */
  var budgetInput = document.getElementById('budget');

  if (budgetInput) {
    budgetInput.addEventListener('input', function () {
      var raw = this.value.replace(/\D/g, '');
      if (raw) {
        this.value = Number(raw).toLocaleString('ru-RU');
      }
    });
  }

  /* ---------- PHONE MASK ---------- */
  var phoneInput = document.getElementById('phone');

  if (phoneInput) {
    phoneInput.addEventListener('input', function (e) {
      var val = this.value.replace(/\D/g, '');
      var formatted = '';

      if (val.length === 0) {
        formatted = '';
      } else if (val[0] === '7' || val[0] === '8') {
        formatted = '+7 ';
        if (val.length > 1) formatted += '(' + val.substring(1, 4);
        if (val.length >= 4) formatted += ') ';
        if (val.length > 4) formatted += val.substring(4, 7);
        if (val.length > 7) formatted += '-' + val.substring(7, 9);
        if (val.length > 9) formatted += '-' + val.substring(9, 11);
      } else {
        formatted = '+7 (' + val.substring(0, 3);
        if (val.length >= 3) formatted += ') ';
        if (val.length > 3) formatted += val.substring(3, 6);
        if (val.length > 6) formatted += '-' + val.substring(6, 8);
        if (val.length > 8) formatted += '-' + val.substring(8, 10);
      }

      this.value = formatted;
    });

    phoneInput.addEventListener('focus', function () {
      if (!this.value) this.value = '+7 (';
    });
  }

  /* ---------- FORM VALIDATION & SUBMIT ---------- */
  var calcForm = document.getElementById('calcForm');
  var calcSuccess = document.getElementById('calcSuccess');

  function showError(id, msg) {
    var el = document.getElementById(id);
    if (el) {
      el.textContent = msg;
      el.classList.add('visible');
    }
    var input = document.getElementById(id.replace('Error', ''));
    if (input) input.classList.add('error');
  }

  function clearError(id) {
    var el = document.getElementById(id);
    if (el) {
      el.textContent = '';
      el.classList.remove('visible');
    }
    var input = document.getElementById(id.replace('Error', ''));
    if (input) input.classList.remove('error');
  }

  function clearAllErrors() {
    ['brandError', 'budgetError', 'yearError', 'nameError', 'phoneError'].forEach(clearError);
  }

  // Clear errors on input
  ['brand', 'budget', 'year', 'name', 'phone'].forEach(function (id) {
    var input = document.getElementById(id);
    if (input) {
      input.addEventListener('input', function () {
        clearError(id + 'Error');
      });
    }
  });

  if (calcForm) {
    calcForm.addEventListener('submit', function (e) {
      e.preventDefault();
      clearAllErrors();

      var valid = true;

      var brand = document.getElementById('brand').value.trim();
      var budget = document.getElementById('budget').value.trim();
      var year = document.getElementById('year').value.trim();
      var name = document.getElementById('name').value.trim();
      var phone = document.getElementById('phone').value.trim();

      if (!brand) {
        showError('brandError', 'Укажите марку или модель авто');
        valid = false;
      }

      if (!budget) {
        showError('budgetError', 'Укажите ваш бюджет');
        valid = false;
      }

      if (!year) {
        showError('yearError', 'Укажите год выпуска');
        valid = false;
      } else {
        var y = parseInt(year, 10);
        if (isNaN(y) || y < 2000 || y > new Date().getFullYear()) {
          showError('yearError', 'Укажите корректный год (2000–' + new Date().getFullYear() + ')');
          valid = false;
        }
      }

      if (!name) {
        showError('nameError', 'Укажите ваше имя');
        valid = false;
      }

      var phoneDigits = phone.replace(/\D/g, '');
      if (!phone || phoneDigits.length < 11) {
        showError('phoneError', 'Укажите корректный номер телефона');
        valid = false;
      }

      if (!valid) return;

      // Success — hide form, show success message
      var submitBtn = document.getElementById('calcSubmit');
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span>Отправка...</span>';

      setTimeout(function () {
        calcForm.style.display = 'none';
        calcSuccess.style.display = 'block';
      }, 800);
    });
  }

  /* ---------- COUNTER ANIMATION ---------- */
  var counterEls = document.querySelectorAll('.trust-item__number');

  function animateCounter(el) {
    var target = parseInt(el.textContent.replace(/\D/g, ''), 10);
    var suffix = el.textContent.replace(/[\d]/g, '');
    var duration = 2000;
    var start = 0;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      el.textContent = Math.floor(eased * target) + suffix;
      if (progress < 1) {
        requestAnimationFrame(step);
      }
    }

    requestAnimationFrame(step);
  }

  if ('IntersectionObserver' in window) {
    var counterObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    counterEls.forEach(function (el) {
      counterObserver.observe(el);
    });
  }

})();
