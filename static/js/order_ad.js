const order = (function () {
  const modalOrder = document.getElementById("modal-order-detail");
  const loadingUI = modalOrder.querySelector(".order-loading");
  const content = modalOrder.querySelector(".order-detail-content");
  let isOpenModal = false;
  let arrOrder = [];
  return {
    formatPrice(n) {
      let parts = n.toString().split(".");
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      return `₫ ${parts.join(",")}`;
    },
    formatData(data) {
      let arr = [];
      let arrRemoveDuplicates = data.filter(function (item, pos, self) {
        let index = self.map((e) => e.idd).indexOf(item.idd);
        return index === pos;
      });
      arrRemoveDuplicates.forEach((item) => {
        arr.push({
          id: item.idd,
          diachi: item.diachii,
          sdt: item.sdtt,
          ngaytao: item.ngaytaoo,
          ngaysua: item.ngaysuaa,
          tongtien: item.tongtienn,
          trangthai: item.TrangThaiDonHang_id == 1 ? "Chờ xác nhận" : item.TrangThaiDonHang_id == 2 ? "Đang vận chuyển" : item.TrangThaiDonHang_id == 3 ? "Hoàn thành" : "Đã hủy",
          chitietdonhang: [
            ...data
              .filter((e) => e.id === item.id)
              .map((e) => {
                return {
                  id: e.SanPham_id,
                  kichcosanpham_id: e.KichCoSanPham_id,
                  ten: e.ten,
                  soluong: e.soluongg,
                  mausac: e.mausac,
                  kichco: e.kichco,
                  hinhanh: e.hinhanh,
                  gia: e.gia,
                };
              }),
          ],
        });
      });
      return arr;
    },
    async getOrders(id) {
      const res = await fetch(
        `${location.origin}/laydonhangid/${id}/`
      );
      return await res.json();
    },
    showOrders(data) {
      data.forEach((item) => {
        const elmContent = document.createElement("div");
        elmContent.innerHTML = `
          <div class="flex flex-col space-y-6 md:space-y-0 md:flex-row justify-between items-center">
          <div class="mr-6">
              <h1 class="text-4xl font-semibold mb-2">Đơn hàng #${item.id}</h1>
              <span class="sm:text-lg text-base text-gray-600">${
                item.trangthai
              }</span> |
              <span class="sm:text-lg text-base text-gray-600"> ${
                item.ngaysua !== null ? item.ngaysua : item.ngaytao
              }</span>
          </div>
          <h3 class="text-rose-500 sm:text-2xl text-xl font-semibold">
              Tổng thành tiền: ${this.formatPrice(
                item["chitietdonhang"].reduce((prev, cur) => {
                  return prev + parseFloat(cur.gia) * parseFloat(cur.soluong);
                }, 0)
              )}
          </h3>
      </div>
      <h6 class="text-gray-700 md:text-base text-sm mt-2">Số điện thoại: ${
        item["sdt"]
      }</h6>
      <p class="text-gray-700 md:text-base text-sm mt-2">Địa chỉ: ${item[
        "diachi"
      ]
        }</p>
      <div class="flex flex-col gap-5">
          <div class="h-[444px] overflow-y-auto relative">
              ${item["chitietdonhang"]
                .map((e) => {
                  return `
                  <div class="bg-white p-4 shadow-lg false">
                  <div class="flex items-center justify-between ">
                      <h4 class="text-blue-500 md:text-lg sm:text-base text-sm">
                          ID: ${e.id} | <span class="text-gray-900"> ${
                    item.ngaysua !== null ? item.ngaysua : item.ngaytao
                  }</span>
                      </h4>
                      
                  </div>
                  <div class="clear-both gap-1 flex justify-between py-2 items-center border-y border-gray-200 border-solid">
                      <div class="flex items-center gap-1">
                          <img class="h-20 w-20" src="/media/${e.hinhanh}" >
                          <div>
                              <h4 class="sm:line-clamp-none line-clamp-1 sm:text-base text-sm">
                              ${e.ten}
                              </h4><span class="text-gray-500 sm:text-base text-sm">
                                  Phân loại
                                  hàng: ${e.mausac} | ${e.kichco}
                              </span><span class="block sm:text-base text-sm">Số lượng: ${
                                e.soluong
                              }</span>
                          </div>
                      </div><strong class="whitespace-nowrap"> ${this.formatPrice(
                        parseFloat(e.gia)
                      )}</strong>
                  </div>
                  <div class="flex justify-end flex-col items-end">
                      <div class="pt-4 pb-4">
                          Thành tiền: <strong class="sm:text-2xl text-lg text-rose-500"> ${this.formatPrice(
                            parseFloat(e.gia) * parseFloat(e.soluong)
                          )}</strong>
                      </div>
                  </div>
                  <div class="clear-both"></div>
              </div>
                  `;
                })
                .join(" ")}
             

      </div>              
        `;
        content.appendChild(elmContent);
      });
    },
    async handleOrder(orderId, type) {
      const res = await fetch(
        `api/${type === 4 ? `huydonhang` : `xulydonhang`}.php`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json; charset=utf-8",
          },
          body: JSON.stringify({
            dhId: orderId,
            loaiId: type,
          }),
        }
      );
      const data = await res.json();
      return data;
    },
    init() {
      
      document.querySelectorAll("[data-order-detail]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
          if (!isOpenModal) {
            content.innerHTML = "";
            loadingUI.classList.remove("hidden");
            modalOrder.classList.remove("hidden");
            isOpenModal = !isOpenModal;
            this.getOrders(e.target.dataset.orderDetail)
              .then((res) => {
                console.log(res);
                arrOrder = this.formatData(res['dsdonhang']);

                this.showOrders(arrOrder);
              })
              .catch((err) => console.log(err))
              .finally(() => {
                loadingUI.classList.add("hidden");
              });
          }
        });
      });
      modalOrder.addEventListener("click", (e) => {
        if (
          e.target.tagName === "BUTTON" &&
          e.target.classList.contains("btn-close-order-detail") &&
          isOpenModal
        ) {
          modalOrder.classList.add("hidden");
          isOpenModal = !isOpenModal;
        }
      });
      document
        .querySelector(".btn-close-order-detail")
        .addEventListener("click", () => {
          if (isOpenModal) {
            modalOrder.classList.add("hidden");
            isOpenModal = !isOpenModal;
          }
        });
    },
  };
})();
order.init();
