const validate = (function () {
  const regexEmail =
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  const regexPassword =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,55}$/;
  const form = document.querySelector("#form");
  const ipEmail = form?.elements["email"];
  const ipUserName = form?.elements["username"];
  const ipPassword = form?.elements["password1"];
  const ipPasswordConfirm = form.elements["password2"];
  const err = document.querySelector(".err");

  return {
    addErr(elm, mes) {
      elm.classList.add("border", "border-red-500");
      elm.nextElementSibling.innerHTML = mes;
      elm.nextElementSibling.classList.remove("hidden");
    },
    removeErr(elm) {
      elm.classList.remove("border", "border-red-500");
      elm.nextElementSibling.classList.add("hidden");
    },
    init() {
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        let isValid = true;
        if (ipEmail !== undefined && !regexEmail.test(ipEmail.value.trim())) {
          isValid = false;
          this.addErr(ipEmail, "Email không hợp lệ!");
        }
        if (ipPasswordConfirm) {
          if (!regexPassword.test(ipPassword.value.trim())) {
            isValid = false;
            this.addErr(
              ipPassword,
              "Mật khẩu phải chứa tối thiểu 8 ký tự, tối đa 55 ký tự và chứa ít nhất một ký tự hoa, ký tự thường, ký tự số, ký tự đặc biệt!"
            );
          } else {
            if (ipPassword.value !== ipPasswordConfirm.value) {
              isValid = false;
              this.addErr(ipPasswordConfirm, "Mật khẩu xác nhận không khớp!");
            }
          }
        }
        if (isValid) {
          form.submit();
        }
      });

      // remove err
      const that = this;

      ipUserName?.addEventListener("input", function () {
        if(!this.nextElementSibling.classList.contains("hidden"))
          this.nextElementSibling.classList.add("hidden")
        if (this.classList.contains("border-red-500")) {
          that.removeErr(this);
        }
      });
      ipEmail?.addEventListener("input", function () {
        if(!this.nextElementSibling.classList.contains("hidden"))
          this.nextElementSibling.classList.add("hidden")
        if (this.classList.contains("border-red-500")) {
          that.removeErr(this);
        }
      });
      ipPasswordConfirm &&
        ipUserName?.addEventListener("input", function () {
          if (this.classList.contains("border-red-500")) {
            that.removeErr(this);
          }
        });
      ipPassword.addEventListener("input", function () {
        if (this.classList.contains("border-red-500")) {
          that.removeErr(this);
        }
      });
      ipPasswordConfirm &&
        ipPasswordConfirm.addEventListener("input", function () {
          if (this.classList.contains("border-red-500")) {
            that.removeErr(this);
          }
        });
    },
  };
})();
validate.init();
