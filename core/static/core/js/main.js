// RugbyLink Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        if (!alert.querySelector('.btn-close')) {
            setTimeout(function() {
                alert.style.transition = 'opacity 0.5s';
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.remove();
                }, 500);
            }, 5000);
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form validation feedback
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Image lazy loading
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Search functionality
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                // Implement live search here if needed
            }, 300);
        });
    }

    // Like/Unlike functionality
    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const isLiked = this.classList.contains('liked');
            
            // Toggle visual state immediately
            this.classList.toggle('liked');
            this.classList.toggle('text-danger');
            
            // Update like count
            const likeCount = this.querySelector('.like-count');
            if (likeCount) {
                const currentCount = parseInt(likeCount.textContent);
                likeCount.textContent = isLiked ? currentCount - 1 : currentCount + 1;
            }
            
            // Send AJAX request
            fetch(`/feed/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: isLiked ? 'unlike' : 'like'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update like count with server response
                    if (likeCount) {
                        likeCount.textContent = data.likes_count;
                    }
                } else {
                    // Revert visual state on error
                    this.classList.toggle('liked');
                    this.classList.toggle('text-danger');
                    if (likeCount) {
                        const currentCount = parseInt(likeCount.textContent);
                        likeCount.textContent = isLiked ? currentCount + 1 : currentCount - 1;
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Revert visual state on error
                this.classList.toggle('liked');
                this.classList.toggle('text-danger');
                if (likeCount) {
                    const currentCount = parseInt(likeCount.textContent);
                    likeCount.textContent = isLiked ? currentCount + 1 : currentCount - 1;
                }
            });
        });
    });

    // Comment form submission
    document.querySelectorAll('.comment-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const content = this.querySelector('textarea[name="content"]').value.trim();
            
            if (!content) return;
            
            // Add loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Posting...';
            submitBtn.disabled = true;
            
            fetch(`/feed/comment/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: content
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Clear form
                    this.querySelector('textarea[name="content"]').value = '';
                    
                    // Add comment to the list
                    const commentsContainer = document.querySelector(`.comments-container[data-post-id="${postId}"]`);
                    if (commentsContainer && data.comment_html) {
                        commentsContainer.insertAdjacentHTML('beforeend', data.comment_html);
                    }
                    
                    // Update comment count
                    const commentCount = document.querySelector(`.comment-count[data-post-id="${postId}"]`);
                    if (commentCount) {
                        commentCount.textContent = data.comments_count;
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            })
            .finally(() => {
                // Restore button state
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            });
        });
    });

    // Connection request functionality
    document.querySelectorAll('.connect-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const userId = this.dataset.userId;
            const isConnected = this.classList.contains('connected');
            
            // Toggle visual state immediately
            this.classList.toggle('connected');
            this.textContent = isConnected ? 'Connect' : 'Connected';
            
            fetch(`/connections/connect/${userId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: isConnected ? 'disconnect' : 'connect'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.textContent = data.connected ? 'Connected' : 'Connect';
                    this.classList.toggle('connected', data.connected);
                } else {
                    // Revert on error
                    this.classList.toggle('connected');
                    this.textContent = isConnected ? 'Connected' : 'Connect';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Revert on error
                this.classList.toggle('connected');
                this.textContent = isConnected ? 'Connected' : 'Connect';
            });
        });
    });

    // Message functionality
    document.querySelectorAll('.message-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const conversationId = this.dataset.conversationId;
            const content = this.querySelector('input[name="content"]').value.trim();
            
            if (!content) return;
            
            // Add loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;
            
            fetch(`/messaging/send/${conversationId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: content
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Clear form
                    this.querySelector('input[name="content"]').value = '';
                    
                    // Add message to the conversation
                    const messagesContainer = document.querySelector('.messages-container');
                    if (messagesContainer && data.message_html) {
                        messagesContainer.insertAdjacentHTML('beforeend', data.message_html);
                        messagesContainer.scrollTop = messagesContainer.scrollHeight;
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            })
            .finally(() => {
                // Restore button state
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            });
        });
    });
});

// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Utility function to show toast notifications
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

// Create toast container if it doesn't exist
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

// Utility function to format numbers
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Utility function to format dates
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) {
        return 'Just now';
    } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
    } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
    } else if (diffInSeconds < 604800) {
        const days = Math.floor(diffInSeconds / 86400);
        return `${days} day${days !== 1 ? 's' : ''} ago`;
    } else {
        return date.toLocaleDateString();
    }
}

