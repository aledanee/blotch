const apiBaseUrl = 'http://127.0.0.1:8001/v1';

let accessToken = localStorage.getItem('access_token');

if (!accessToken) {
    window.location.href = 'login.html'; // Redirect to login if no token
}

// Set Authorization headers
axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;

// Load Categories and Articles when the page is loaded
document.addEventListener('DOMContentLoaded', () => {
    loadCategories();
    loadArticles();
});

// Load Categories from API
function loadCategories() {
    axios.get(`${apiBaseUrl}/categories`)
        .then(response => {
            const categories = response.data;
            const categoriesList = document.getElementById('categoriesList');
            categoriesList.innerHTML = '';
            categories.forEach(category => {
                categoriesList.innerHTML += `<li class="list-group-item"><a href="#" onclick="loadArticlesByCategory(${category.id})">${category.name}</a></li>`;
            });
        })
        .catch(error => console.error('Failed to load categories', error));
}

// Load Articles from API
function loadArticles() {
    axios.get(`${apiBaseUrl}/search/articles`)
        .then(response => {
            const articles = response.data;
            const articlesContainer = document.getElementById('articlesContainer');
            articlesContainer.innerHTML = '';
            articles.forEach(article => {
                articlesContainer.innerHTML += generateArticleHTML(article);
            });
        })
        .catch(error => console.error('Failed to load articles', error));
}

// Load Articles by Category
function loadArticlesByCategory(categoryId) {
    axios.get(`${apiBaseUrl}/articles/all?category_id=${categoryId}`)
        .then(response => {
            const articles = response.data;
            const articlesContainer = document.getElementById('articlesContainer');
            articlesContainer.innerHTML = '';
            articles.forEach(article => {
                articlesContainer.innerHTML += generateArticleHTML(article);
            });
        })
        .catch(error => console.error('Failed to load articles by category', error));
}

// Search Articles by Title
function searchArticles() {
    const searchQuery = document.getElementById('searchInput').value;
    axios.get(`${apiBaseUrl}/search/articles?search=${searchQuery}`)
        .then(response => {
            const articles = response.data;
            const articlesContainer = document.getElementById('articlesContainer');
            articlesContainer.innerHTML = '';
            articles.forEach(article => {
                articlesContainer.innerHTML += generateArticleHTML(article);
            });
        })
        .catch(error => console.error('Failed to search articles', error));
}

// Generate HTML for Article
function generateArticleHTML(article) {
    return `
        <div class="col-md-12 mb-4">
            <div class="card">
                <img src="${article.image_url}" class="card-img-top" alt="${article.title}">
                <div class="card-body">
                    <h5 class="card-title">${article.title}</h5>
                    <p class="card-text">${article.text}</p>
                    <button class="btn btn-primary" onclick="likeArticle(${article.id})">Like</button>
                    <button class="btn btn-secondary" onclick="loadComments(${article.id})">Comments</button>
                </div>
            </div>
        </div>
    `;
}

// Like Article
function likeArticle(articleId) {
    axios.post(`${apiBaseUrl}/like/articles/${articleId}/likes`)
        .then(response => {
            alert('Article liked successfully!');
        })
        .catch(error => alert('Failed to like article.'));
}

// Load Comments for Article
function loadComments(articleId) {
    axios.get(`${apiBaseUrl}/comment/articles/${articleId}/comments`)
        .then(response => {
            const comments = response.data;
            const commentsContainer = document.getElementById('commentsContainer');
            commentsContainer.innerHTML = '';
            comments.forEach(comment => {
                commentsContainer.innerHTML += `<p>${comment.content}</p>`;
            });
        })
        .catch(error => alert('Failed to load comments.'));
}

// Add Comment to Article
function addComment(articleId) {
    const commentContent = document.getElementById('commentInput').value;
    axios.post(`${apiBaseUrl}/comment/articles/${articleId}/comments`, { content: commentContent })
        .then(response => {
            loadComments(articleId); // Refresh comments
        })
        .catch(error => alert('Failed to add comment.'));
}

// Logout and clear local storage
function logout() {
    localStorage.removeItem('access_token');
    window.location.href = 'login.html';
}
