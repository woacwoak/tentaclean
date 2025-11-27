function directToLogin() {
    window.location.href = "login.html";
}

function directToSignup() {
    window.location.href = "signup.html";
<<<<<<< HEAD
=======
}

// Task page functionality
document.addEventListener('DOMContentLoaded', function() {
    // Task completion functionality
    const taskButtons = document.querySelectorAll('.task-btn:not(.create-btn)');
    taskButtons.forEach(button => {
        const circle = button.querySelector('.circle');
        let isCompleted = false;
        
        if (circle) {
            circle.addEventListener('click', function(e) {
                e.stopPropagation();
                isCompleted = !isCompleted;
                
                if (isCompleted) {
                    circle.style.backgroundColor = '#5BA4D8';
                    circle.style.borderColor = '#5BA4D8';
                    button.style.textDecoration = 'line-through';
                    button.style.opacity = '0.6';
                    button.classList.add('completed');
                } else {
                    circle.style.backgroundColor = 'transparent';
                    circle.style.borderColor = '#999';
                    button.style.textDecoration = 'none';
                    button.style.opacity = '1';
                    button.classList.remove('completed');
                }
            });
        }
    });

    // Delete task functionality
    const deleteIcons = document.querySelectorAll('.task-icon');
    deleteIcons.forEach(icon => {
        icon.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const taskBtn = this.closest('.task-btn');
            if (taskBtn && confirm('Are you sure you want to delete this task?')) {
                taskBtn.style.animation = 'slideOut 0.3s ease-out forwards';
                setTimeout(() => {
                    taskBtn.remove();
                }, 300);
            }
        });
    });

    // Create new task functionality
    const createBtn = document.querySelector('.create-btn');
    if (createBtn) {
        createBtn.addEventListener('click', function() {
            const taskName = prompt('Enter task name:');
            if (taskName && taskName.trim()) {
                createNewTask(taskName.trim());
            }
        });
    }

    // Dashboard button functionality
    const createHouseBtn = document.getElementById('createbtn');
    if (createHouseBtn) {
        createHouseBtn.addEventListener('click', function() {
            window.location.href = '/createhouse';
        });
    }

    const joinBtns = document.querySelectorAll('#joinbtn');
    joinBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            alert('Join house functionality coming soon!');
        });
    });

    // Create house form submission
    const createHouseFormBtn = document.getElementById('createHousebtn');
    if (createHouseFormBtn) {
        createHouseFormBtn.addEventListener('click', function() {
            const houseName = document.getElementById('houseName').value;
            const address = document.getElementById('address').value;
            const capacity = document.getElementById('capacity').value;
            const description = document.getElementById('descriptionInput').value;
            
            if (houseName && address && capacity && description) {
                alert('House "' + houseName + '" created successfully!');
                window.location.href = '/houselist';
            } else {
                alert('Please fill in all fields');
            }
        });
    }
});

// Helper function to create new task
function createNewTask(taskName) {
    const taskList = document.querySelector('.task-list');
    const createBtn = document.querySelector('.create-btn');
    
    const newTask = document.createElement('button');
    newTask.className = 'task-btn';
    newTask.style.animation = 'slideIn 0.3s ease-out';
    
    newTask.innerHTML = `
        <span class="circle"></span>
        ${taskName}
        <a href="#" class="task-icon">
          <img src="/static/img/icons/trash_can.jpg" alt="Trash Icon" class="task-icon">
        </a>
    `;
    
    taskList.insertBefore(newTask, createBtn);
    
    // Add event listeners to the new task
    const circle = newTask.querySelector('.circle');
    let isCompleted = false;
    
    circle.addEventListener('click', function(e) {
        e.stopPropagation();
        isCompleted = !isCompleted;
        
        if (isCompleted) {
            circle.style.backgroundColor = '#5BA4D8';
            circle.style.borderColor = '#5BA4D8';
            newTask.style.textDecoration = 'line-through';
            newTask.style.opacity = '0.6';
        } else {
            circle.style.backgroundColor = 'transparent';
            circle.style.borderColor = '#999';
            newTask.style.textDecoration = 'none';
            newTask.style.opacity = '1';
        }
    });
    
    const deleteIcon = newTask.querySelector('.task-icon');
    deleteIcon.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        if (confirm('Are you sure you want to delete this task?')) {
            newTask.style.animation = 'slideOut 0.3s ease-out forwards';
            setTimeout(() => {
                newTask.remove();
            }, 300);
        }
    });
}

// Password validation for signup
const signupForm = document.getElementById('signupForm');
if (signupForm && signupForm.action.includes('signup')) {
    signupForm.addEventListener('submit', function(e) {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword');
        
        if (confirmPassword && password !== confirmPassword.value) {
            e.preventDefault();
            alert('Passwords do not match!');
            return false;
        }
    });
>>>>>>> 084327c4f7462c7a368dd1382a356ba648823319
}