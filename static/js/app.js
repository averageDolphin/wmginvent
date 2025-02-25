document.addEventListener("DOMContentLoaded", function() {
    fetchProducts();

    // Attach event listener to form submission
    document.getElementById("add-product-form").addEventListener("submit", function(event) {
        event.preventDefault();
        addProduct();
    });
});

function fetchProducts() {
    fetch("/api/products")
        .then(response => response.json())
        .then(data => {
            let productTable = document.getElementById("product-list");
            productTable.innerHTML = "";
            
            Object.keys(data).forEach(productId => {
                let product = data[productId];
                let row = `<tr>
                    <td>${product.product_id}</td>
                    <td>${product.name}</td>
                    <td>${product.brand}</td>
                    <td>$${product.price.toFixed(2)}</td>
                    <td>${product.stock}</td>
                    <td>
                        <button class="btn btn-danger btn-sm" onclick="deleteProduct('${product.product_id}')">Delete</button>
                    </td>
                </tr>`;
                productTable.innerHTML += row;
            });
        })
        .catch(error => console.error("Error loading products:", error));
}

function addProduct() {
    let productData = {
        product_id: document.getElementById("product_id").value,
        name: document.getElementById("name").value,
        brand: document.getElementById("brand").value,
        price: parseFloat(document.getElementById("price").value),
        stock: parseInt(document.getElementById("stock").value),
        threshold: 5,
        discontinued: false,
        image_url: "images/default.jpg"
    };

    fetch("/api/products", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(productData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            fetchProducts();
            document.getElementById("add-product-form").reset();
            document.querySelector("#addProductModal .btn-close").click(); // Close modal after submission
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error("Error adding product:", error));
}

function deleteProduct(productId) {
    fetch(`/api/products/${productId}`, { method: "DELETE" })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                fetchProducts();
            } else {
                alert(data.error);
            }
        })
        .catch(error => console.error("Error deleting product:", error));
}

document.addEventListener("DOMContentLoaded", function() {
    fetchDashboardData();
    fetchRecentOrders();
});

function fetchDashboardData() {
    fetch("/api/reports/sales")
        .then(response => response.json())
        .then(data => {
            document.getElementById("total-products").textContent = Object.keys(data.product_sales).length;
            document.getElementById("total-orders").textContent = data.total_orders;
            document.getElementById("total-revenue").textContent = `$${data.total_revenue.toFixed(2)}`;

            fetch("/api/reports/stock")
                .then(response => response.json())
                .then(stockData => {
                    document.getElementById("low-stock").textContent = Object.keys(stockData.low_stock_products).length;
                });

            renderSalesChart(data.product_sales);
        })
        .catch(error => console.error("Error fetching dashboard data:", error));
}

function fetchRecentOrders() {
    fetch("/api/orders")
        .then(response => response.json())
        .then(data => {
            let ordersTable = document.getElementById("recent-orders");
            ordersTable.innerHTML = "";

            Object.keys(data).slice(0, 5).forEach(orderId => {
                let order = data[orderId];
                let row = `<tr>
                    <td>${order.order_id}</td>
                    <td>${order.customer_name}</td>
                    <td>${order.order_date}</td>
                    <td>$${order.items.reduce((sum, item) => sum + (item.price * item.quantity), 0).toFixed(2)}</td>
                    <td>${order.status}</td>
                </tr>`;
                ordersTable.innerHTML += row;
            });
        })
        .catch(error => console.error("Error fetching recent orders:", error));
}

function renderSalesChart(salesData) {
    const ctx = document.getElementById("salesChart").getContext("2d");
    const labels = Object.keys(salesData);
    const data = Object.values(salesData);

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Units Sold",
                data: data,
                backgroundColor: "rgba(102, 51, 153, 0.7)",
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, /* Allow better scaling */
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

