function processOrder(itemStock, membership, orderAmount, shippingOption) {
    if (itemStock < 1) {
      alert("❌ 죄송합니다. 해당 상품은 품절입니다.");
      return;
    }
  
    let discountRate = 0;
    if (membership === "VIP") discountRate = 0.10;
    else if (membership === "Gold") discountRate = 0.05;
  
    let discountedAmount = orderAmount * (1 - discountRate);
  
    if (discountedAmount >= 200000) discountedAmount -= 15000;
    else if (discountedAmount >= 100000) discountedAmount -= 5000;
  
    let shippingFee = shippingOption === "fast" ? 3000 : 0;
  
    const finalAmount = discountedAmount + shippingFee;
  
    alert(`✅ 주문이 정상적으로 완료되었습니다.\n💳 최종 결제 금액: ${finalAmount.toLocaleString("ko-KR")}원`);
  }
  
  function handleOrder() {
    const stock = document.getElementById("stock").value;
    const amount = document.getElementById("amount").value;
    const membership = document.getElementById("membership").value;
    const shipping = document.getElementById("shipping").value;
  
    if (stock === "" || amount === "") {
      alert("📌 상품 재고와 주문 금액을 모두 입력해주세요.");
      return;
    }
  
    const stockNum = parseInt(stock);
    const amountNum = parseInt(amount);
  
    if (isNaN(stockNum) || isNaN(amountNum) || stockNum < 0 || amountNum < 0) {
      alert("⚠️ 재고와 주문 금액은 0 이상의 숫자로 입력되어야 합니다.");
      return;
    }
  
    processOrder(stockNum, membership, amountNum, shipping);
  }
  