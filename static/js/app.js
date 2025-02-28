// Helper functions
async function calculateTotalPrice(orderItems) {
    let total = 0;

    try {
        let response = await fetch("/api/products"); // Fetch product prices directly
        let products = await response.json();
        orderItems.forEach(item => {
            let product = products[item.product_id]; // Look up product
            if (product) {
                total += product.price * (item.quantity || 1); // Multiply price by quantity
            }
        });

    } catch (error) {
        console.error("Error fetching product prices:", error);
    }
    return total;
}

// Product 
document.addEventListener("DOMContentLoaded", function() {
    fetchProducts();

    document.getElementById("add-product-form").addEventListener("submit", function(event) {
        event.preventDefault();
        addProduct();
    });
});

document.addEventListener("DOMContentLoaded", function() {
    fetchProducts();

    document.getElementById("edit-product-form").addEventListener("submit", function(event) {
        event.preventDefault();
        updateProduct();
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
                        <button class="btn btn-warning btn-sm" onclick="openEditProductModal('${product.product_id}', '${product.name}', '${product.brand}', ${product.price}, ${product.stock})">Edit</button>
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

function openEditProductModal(productId, name, brand, price, stock) {
    document.getElementById("edit-product-id").value = productId;
    document.getElementById("edit-product-name").value = name;
    document.getElementById("edit-product-brand").value = brand;
    document.getElementById("edit-product-price").value = price;
    document.getElementById("edit-product-stock").value = stock;
    
    new bootstrap.Modal(document.getElementById("editProductModal")).show();
}

function updateProduct() {
    let productId = document.getElementById("edit-product-id").value;
    let updatedProduct = {
        name: document.getElementById("edit-product-name").value,
        brand: document.getElementById("edit-product-brand").value,
        price: parseFloat(document.getElementById("edit-product-price").value),
        stock: parseInt(document.getElementById("edit-product-stock").value)
    };

    fetch(`/api/products/${productId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedProduct)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            fetchProducts();
            document.getElementById("edit-product-form").reset();
            document.querySelector("#editProductModal .btn-close").click();
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error("Error updating product:", error));
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


// Dashboard
document.addEventListener("DOMContentLoaded", function() {
    fetchDashboardData();
    fetchRecentOrders();
});

function fetchDashboardData() {
    fetch("/api/reports/sales")
        .then(response => response.json())
        .then(async data => {
            document.getElementById("total-products").textContent = Object.keys(data.product_sales).length;
            document.getElementById("total-orders").textContent = data.total_orders;

            let formatted_sales = Object.entries(data.product_sales).map(([product_id, quantity]) => ({
                product_id,
                quantity
            }));

            let total_revenue = await calculateTotalPrice(formatted_sales);

            document.getElementById("total-revenue").textContent = `$${total_revenue.toFixed(2)}`;
            console.log(data);
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

            Object.keys(data).slice(0, 5).forEach(async orderId => {
                let order = data[orderId];

                let orderDate = new Date(orderId.slice(3) * 1000);
                orderDate = orderDate.toLocaleString();
                
                let totalPrice = (await calculateTotalPrice(order.items)).toFixed(2);
                console.log(totalPrice);
                let row = `<tr>
                    <td>${order.order_id}</td>
                    <td>${order.customer_name}</td>
                    <td>${orderDate}</td>
                    <td>$${totalPrice}</td>
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

// Orders
document.addEventListener("DOMContentLoaded", function() {
    if (window.location.pathname === "/orders") {
        fetchOrders();
        document.getElementById("edit-order-form").addEventListener("submit", function(event) {
            event.preventDefault();
            updateOrderStatus();
        });
    }
});




function fetchOrders() {
    
    fetch("/api/orders")
        .then(response => response.json())
        .then(data => {
            let orderTable = document.getElementById("order-list");
            orderTable.innerHTML = "";

            console.log("Orders API Response:", data); // Debugging

            if (!data || Object.keys(data).length === 0) {
                orderTable.innerHTML = `<tr><td colspan="6" class="text-center">No orders found</td></tr>`;
                return;
            }

            Object.keys(data).forEach(async orderId => {
                let order = data[orderId];
                
                let orderDate = new Date(orderId.slice(3) * 1000);
                orderDate = orderDate.toLocaleString();

                // let total = 0;
                // if (order.items && Array.isArray(order.items) && order.items.length > 0) {
                //     total = order.items.reduce((sum, item) => {
                //         return sum + ((item.price || 0) * (item.quantity || 1));
                //     }, 0);
                // }
                let totalPrice = (await calculateTotalPrice(order.items)).toFixed(2);
                console.log(totalPrice);


                let row = `<tr>
                    <td>${orderId}</td>
                    <td>${order.customer_name || "N/A"}</td>
                    <td>${orderDate || "N/A"}</td>
                    <td>$${totalPrice}</td>
                    <td>${order.status}</td>
                    <td>
                        <button class="btn btn-warning btn-sm" onclick="openEditOrderModal('${orderId}', '${order.status}')">Edit</button>
                        <button class="btn btn-danger btn-sm" onclick="deleteOrder('${orderId}')">Delete</button>
                    </td>
                </tr>`;
                orderTable.innerHTML += row;
            });
        })
        .catch(error => {
            console.error("Error loading orders:", error);
            document.getElementById("order-list").innerHTML = `<tr><td colspan="6" class="text-center text-danger">Error loading orders</td></tr>`;
        });
}

function openEditOrderModal(orderId, currentStatus) {
    document.getElementById("edit-order-id").value = orderId;
    document.getElementById("edit-order-status").value = currentStatus;
    new bootstrap.Modal(document.getElementById("editOrderModal")).show();
}

function updateOrderStatus() {
    let orderId = document.getElementById("edit-order-id").value;
    let newStatus = document.getElementById("edit-order-status").value;

    fetch(`/api/orders/${orderId}/update`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            fetchOrders();
            document.getElementById("edit-order-form").reset();
            document.querySelector("#editOrderModal .btn-close").click();
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error("Error updating order:", error));
}

function deleteOrder(orderId) {
    if (!confirm("Are you sure you want to delete this order?")) return;

    fetch(`/api/orders/${orderId}/delete`, { method: "DELETE" })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                fetchOrders();
            } else {
                alert(data.error);
            }
        })
        .catch(error => console.error("Error deleting order:", error));
}

// Report
document.addEventListener("DOMContentLoaded", function() {
    if (window.location.pathname === "/reports") {
        fetchSalesReport();
        fetchStockReport();
    }
});

function fetchSalesReport() {
    fetch("/api/reports/sales")
        .then(response => response.json())
        .then(data => {
            let table = document.getElementById("sales-report");
            table.innerHTML = "";

            if (!data.product_sales || Object.keys(data.product_sales).length === 0) {
                table.innerHTML = `<tr><td colspan="3" class="text-center">No sales data</td></tr>`;
                return;
            }
            console.log(data.product_sales)
            Object.keys(data.product_sales).forEach(async productId => {
                console.log(productId);
                
                let units_sold = data.product_sales[productId];
                
                let response = await fetch("api/products");
                let products = await response.json();
                let revenue = units_sold * products[productId].price;

                let row = `<tr>
                    <td>${productId}</td>
                    <td>${units_sold}</td>
                    <td>$${revenue}</td>
                </tr>`;
                table.innerHTML += row;
            });
        })
        .catch(error => console.error("Error loading sales report:", error));
}

function fetchStockReport() {
    fetch("/api/reports/stock")
        .then(response => response.json())
        .then(data => {
            let table = document.getElementById("stock-report");
            table.innerHTML = "";

            if (!data.low_stock_products || Object.keys(data.low_stock_products).length === 0) {
                table.innerHTML = `<tr><td colspan="2" class="text-center">No low stock products</td></tr>`;
                return;
            }

            Object.keys(data.low_stock_products).forEach(productId => {
                let product = data.low_stock_products[productId];
                let row = `<tr>
                    <td>${product.name}</td>
                    <td>${product.stock}</td>
                </tr>`;
                table.innerHTML += row;
            });
        })
        .catch(error => console.error("Error loading stock report:", error));
}

function downloadSalesReport() {
    fetch("/api/reports/sales")
        .then(response => response.json())
        .then(data => {
            let csvContent = "data:text/csv;charset=utf-8,Product ID,Units Sold,Total Revenue\n";
            Object.keys(data.product_sales).forEach(async productId => {
                let units_sold = data.product_sales[productId];
                
                let response = await fetch("api/products");
                let products = await response.json();
                let revenue = units_sold * products[productId].price;
                let report = data.product_sales[productId];
                csvContent += `${productId},${units_sold},${revenue}\n`;
                console.log(csvContent)
            });

            let encodedUri = encodeURI(csvContent);
            let link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "sales_report.csv");
            document.body.appendChild(link);
            link.click();
        })
        .catch(error => console.error("Error downloading report:", error));
}
