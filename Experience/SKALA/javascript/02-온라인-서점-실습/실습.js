const bookList = [
  {
    title: "자바스크립트 완벽 가이드",
    author: "David Flanagan",
    price: 35000,
    stock: 5,
    category: "프로그래밍"
  },
  {
    title: "모던 자바스크립트 Deep Dive",
    author: "이웅모",
    price: 40000,
    stock: 0,
    category: "프로그래밍"
  },
  {
    title: "돈의 심리학",
    author: "모건 하우절",
    price: 18000,
    stock: 3,
    category: "경제"
  },
  {
    title: "불편한 편의점",
    author: "김호연",
    price: 14500,
    stock: 2,
    category: "소설"
  }
];

function addBook() {
  const title = document.getElementById("title").value;
  const author = document.getElementById("author").value;
  const price = parseInt(document.getElementById("price").value);
  const stock = parseInt(document.getElementById("stock").value);
  const category = document.getElementById("category").value;

  if (!title || !author || isNaN(price) || isNaN(stock)) {
    alert("모든 항목을 정확히 입력해주세요.");
    return;
  }

  const newBook = { title, author, price, stock, category };
  bookList.push(newBook);
  renderTable();
  clearForm();
}

function renderTable() {
  const tbody = document.querySelector("#bookTable tbody");
  tbody.innerHTML = "";

  bookList.forEach(book => {
    const row = `<tr>
      <td>${book.title}</td>
      <td>${book.author}</td>
      <td>${book.price}</td>
      <td>${book.stock}</td>
      <td>${book.category}</td>
    </tr>`;
    tbody.innerHTML += row;
  });
}

function clearForm() {
  document.getElementById("title").value = "";
  document.getElementById("author").value = "";
  document.getElementById("price").value = "";
  document.getElementById("stock").value = "";
  document.getElementById("category").value = "프로그래밍";
}

window.onload = () => {
  renderTable();
};

// -------------------------- 실습 버튼 함수 ---------------------------

function updateResult(title, items) {
  const resultList = document.getElementById("resultList");
  resultList.innerHTML = "";
  document.querySelector("#resultArea h2").textContent = "🧪 " + title;
  items.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    resultList.appendChild(li);
  });
}

function exercise1() {
  const titles = [];
  for (let i = 0; i < bookList.length; i++) {
    titles.push(bookList[i].title);
  }
  updateResult("실습 1: 모든 도서 제목 출력", titles);
}

function exercise2() {
  const stocked = [];
  for (let book of bookList) {
    if (book.stock >= 1) {
      stocked.push(book.title);
    }
  }
  updateResult("실습 2: 재고 1권 이상 도서", stocked);
}

function exercise3() {
  const programming = [];
  bookList.forEach(book => {
    if (book.category === "프로그래밍") {
      programming.push(book.title);
    }
  });
  updateResult("실습 3: 프로그래밍 카테고리 도서", programming);
}

function exercise4() {
  let sum = 0;
  for (let book of bookList) {
    sum += book.price;
  }
  const avg = (sum / bookList.length).toFixed(2);
  updateResult("실습 4: 전체 평균 가격", [`${avg}원`]);
}

function exercise5() {
  const updated = [];
  for (let book of bookList) {
    if (book.stock === 0) {
      book.stock = 10;
      updated.push(`${book.title} → 재고 10권으로 갱신됨`);
    }
  }
  renderTable();
  if (updated.length === 0) {
    updated.push("재고가 0인 도서가 없습니다.");
  }
  updateResult("실습 5: 재고 0 → 10권 추가", updated);
}
