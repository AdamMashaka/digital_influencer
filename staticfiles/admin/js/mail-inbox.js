(function () {
  "use strict";

  let checkAll = document.querySelector('.check-all');
  checkAll.addEventListener('click', checkAllFn)

  function checkAllFn() {
    if (checkAll.checked) {
      document.querySelectorAll('.mail-checkbox input').forEach(function (e) {
        e.closest('.mail-list').classList.add('selected');
        e.checked = true;
      });
    }
    else {
      document.querySelectorAll('.mail-checkbox input').forEach(function (e) {
        e.closest('.mail-list').classList.remove('selected');
        e.checked = false;
      });
    }
  }
  //modal //
  let maxScreen = document.querySelector('.ti-modal-max-screen');
  let minScreen = document.querySelector('.ti-modal-min-screen');
  let closeBtn = document.querySelector('.ti-modal-close-btn');

  maxScreen.addEventListener("click", () => {
    document.querySelector(".ti-modal").classList.toggle("mail-fullscreen");
    document.querySelector(".ti-modal").classList.remove("mail-minscreen");
  })

  minScreen.addEventListener("click", () => {
    document.querySelector(".ti-modal").classList.toggle("mail-minscreen");
    document.querySelector(".ti-modal").classList.remove("mail-fullscreen");
  })
  closeBtn.addEventListener("click", () => {
    document.querySelector(".ti-modal").classList.remove("mail-minscreen");
    document.querySelector(".ti-modal").classList.remove("mail-fullscreen");
  })
  //modal//

  // mail//
  let ccBtn = document.querySelector('.btn-cc');
  let ccBtn2 = document.querySelector('.btn-bcc-cc');
  let bccBtn = document.querySelector('.btn-bcc');
  let bccBtn2 = document.querySelector('.btn-cc-bcc');
  let mailCc = document.querySelector('.mail-cc');
  let mailBcc = document.querySelector('.mail-bcc');
  let MailMain = document.querySelector('#mail-compose');

  ccBtn.addEventListener("click", () => {
    MailMain.classList.add("mail-add-cc");
    mailCc.classList.remove("hidden");
  })
  ccBtn2.addEventListener("click", () => {
    MailMain.classList.add("mail-add-cc2");
    mailCc.classList.remove("hidden");
  })

  bccBtn2.addEventListener("click", () => {
    MailMain.classList.add("mail-add-bcc");
    mailBcc.classList.remove("hidden");
  })

  bccBtn.addEventListener("click", () => {
    MailMain.classList.add("mail-add-bcc2");
    mailBcc.classList.remove("hidden");
  })



})();

