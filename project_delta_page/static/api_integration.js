/**
 * API Integration Logic for GammaStore
 * Handles all communication between the Frontend and the FastAPI Backend.
 */

const API_BASE = "http://127.0.0.1:8000";

// Utility for handling API responses
async function apiRequest(endpoint, method = 'GET', body = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    };
    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'API Error');
        }
        return await response.json();
    } catch (error) {
        console.error(`API Request Failed (${method} ${endpoint}):`, error.message);
        alert(`Error: ${error.message}`);
        throw error;
    }
}

/**
 * PAGE SPECIFIC LOGIC
 */

// 1. ADMIN DASHBOARD LOGIC
async function loadAdminData() {
    try {
        const categories = await apiRequest('/categories/');
        const products = await apiRequest('/products/');
        
        renderCategories(categories);
        renderProducts(products);
    } catch (e) {
        console.error("Failed to load admin data", e);
    }
}

function renderCategories(categories) {
    const list = document.getElementById('category-list');
    if (!list) return;
    
    list.innerHTML = categories.map(cat => `
        <div class="flex justify-between items-center p-3 border-b hover:bg-gray-50">
            <div>
                <p class="font-bold text-gray-800">${cat.name}</p>
                <p class="text-xs text-gray-500">${cat.description || 'No description'}</p>
            </div>
            <button class="text-red-500 hover:text-red-700"><i class="fas fa-trash"></i></button>
        </div>
    `).join('');
}

function renderProducts(products) {
    const list = document.getElementById('product-list');
    if (!list) return;

    list.innerHTML = products.map(prod => `
        <div class="flex justify-between items-center p-3 border-b hover:bg-gray-50">
            <div>
                <p class="font-bold text-gray-800">${prod.name}</p>
                <p class="text-xs text-indigo-600">$${prod.price.toFixed(2)}</p>
            </div>
            <button class="text-red-500 hover:text-red-700"><i class="fas fa-trash"></i></button>
        </div>
    `).join('');
}

// 2. PRODUCT LISTING (HOME) LOGIC
async function loadProducts() {
    try {
        const products = await apiRequest('/products/');
        const container = document.getElementById('product-grid');
        if (!container) return;

        container.innerHTML = products.map(prod => `
            <div class="bg-white rounded-xl shadow-md overflow-hidden transition hover:shadow-lg">
                <div class="h-48 bg-gray-200 flex items-center justify-center">
                    <i class="fas fa-image text-gray-400 text-4xl"></i>
                </div>
                <div class="p-6">
                    <p class="text-gray-500 text-sm mb-1">Category ID: ${prod.category_id}</p>
                    <h3 class="text-xl font-bold text-gray-800 mb-2">${prod.name}</h3>
                    <div class="flex justify-between items-center">
                        <span class="text-indigo-600 font-bold text-lg">$${prod.price.toFixed(2)}</span>
                        <a href="detail.html?id=${prod.id}" class="text-gray-400 hover:text-indigo-600 transition"><i class="fas fa-arrow-right"></i></a>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (e) {
        console.error("Failed to load products", e);
    }
}

// 3. PRODUCT DETAIL LOGIC
async function loadProductDetail() {
    const params = new URLSearchParams(window.location.search);
    const productId = params.get('id');
    if (!productId) {
        window.location.href = 'index.html';
        return;
    }

    try {
        // In a real app, you'd have an endpoint like /products/{id}
        // For now, we fetch all and find the specific one to simulate the detail view
        const products = await apiRequest('/products/');
        const product = products.find(p => p.id === parseInt(productId));

        if (!product) {
            throw new Error("Product not found");
        }

        document.getElementById('detail-name').innerText = product.name;
        document.getElementById('detail-price').innerText = `$${product.price.toFixed(2)}`;
        document.getElementById('detail-desc').innerText = product.description || 'No description available.';
        document.getElementById('detail-category').innerText = `Category ID: ${product.category_id}`;
    } catch (e) {
        console.error("Failed to load product detail", e);
        document.body.innerHTML = `<div class="flex h-screen items-center justify-center"><div class="text-center"><h1 class="text-2xl font-bold">Product Not Found</h1><a href="index.html" class="text-indigo-600 underline">Return to Store</a></div></div>`;
    }
}

/**
 * INITIALIZATION
 */
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    
    if (path.includes('admin.html')) {
        loadAdminData();
    } else if (path.includes('detail.html')) {
        loadProductDetail();
    } else {
        loadProducts();
    }
});
