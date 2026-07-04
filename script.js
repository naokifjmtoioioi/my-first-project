(() => {
  // --- Mobile nav toggle ---
  const navToggle = document.getElementById('navToggle');
  const nav = document.getElementById('nav');

  navToggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('is-open');
    navToggle.classList.toggle('is-active', isOpen);
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });

  nav.querySelectorAll('.nav-link').forEach((link) => {
    link.addEventListener('click', () => {
      nav.classList.remove('is-open');
      navToggle.classList.remove('is-active');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });

  // --- Header background on scroll ---
  const header = document.getElementById('header');
  const toTop = document.getElementById('toTop');

  const onScroll = () => {
    const scrolled = window.scrollY > 40;
    header.style.boxShadow = scrolled ? '0 4px 16px rgba(90, 62, 40, 0.08)' : 'none';
    toTop.classList.toggle('is-visible', window.scrollY > 480);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // --- Reveal on scroll ---
  const revealTargets = document.querySelectorAll(
    '.profile, .cards .card, .works .work, .voices .voice, .form'
  );
  revealTargets.forEach((el) => el.classList.add('reveal'));

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );
  revealTargets.forEach((el) => observer.observe(el));

  // --- Contact form validation ---
  const form = document.getElementById('contactForm');
  const status = document.getElementById('formStatus');

  const rules = {
    name: (value) => (value.trim().length > 0 ? '' : 'お名前を入力してください。'),
    email: (value) => {
      if (!value.trim()) return 'メールアドレスを入力してください。';
      const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return pattern.test(value) ? '' : '正しいメールアドレスの形式で入力してください。';
    },
    message: (value) => (value.trim().length > 0 ? '' : 'お問い合わせ内容を入力してください。'),
  };

  const showError = (fieldName, message) => {
    const field = form.elements[fieldName];
    const errorEl = form.querySelector(`[data-error-for="${fieldName}"]`);
    if (errorEl) errorEl.textContent = message;
    if (field) field.classList.toggle('is-invalid', Boolean(message));
  };

  const validateField = (fieldName) => {
    const field = form.elements[fieldName];
    const message = rules[fieldName](field.value);
    showError(fieldName, message);
    return !message;
  };

  Object.keys(rules).forEach((fieldName) => {
    form.elements[fieldName].addEventListener('blur', () => validateField(fieldName));
    form.elements[fieldName].addEventListener('input', () => {
      if (form.elements[fieldName].classList.contains('is-invalid')) {
        validateField(fieldName);
      }
    });
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();

    const isValid = Object.keys(rules)
      .map((fieldName) => validateField(fieldName))
      .every(Boolean);

    if (!isValid) {
      status.textContent = '入力内容をご確認ください。';
      status.style.color = '#c0473a';
      return;
    }

    // NOTE: この先は送信APIやメールサービス（例: Formspree, EmailJS など）と
    // 接続する想定のプレースホルダーです。
    status.style.color = '';
    status.textContent = '送信しました。ご連絡ありがとうございます。折り返しご連絡いたします。';
    form.reset();
    Object.keys(rules).forEach((fieldName) => showError(fieldName, ''));
  });
})();
