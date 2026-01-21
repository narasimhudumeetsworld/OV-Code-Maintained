/**
 * OV-Code Task Manager - Minimal Web App Example
 * 
 * This demonstrates best practices for JavaScript:
 * - Use const/let instead of var
 * - Use textContent instead of innerHTML (XSS prevention)
 * - Proper error handling
 * - Accessible UI interactions
 * - Clean, readable code
 */

// Task storage (in production, use proper state management)
const tasks = [];

/**
 * Initialize the application
 */
function init() {
    // Load saved tasks from localStorage
    const savedTasks = localStorage.getItem('ov-code-tasks');
    if (savedTasks) {
        try {
            const parsed = JSON.parse(savedTasks);
            tasks.push(...parsed);
            renderTasks();
        } catch (error) {
            console.error('Failed to load saved tasks:', error);
        }
    }
    
    // Add keyboard support for input
    const input = document.getElementById('taskInput');
    input.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            addTask();
        }
    });
    
    renderTasks();
}

/**
 * Add a new task
 */
function addTask() {
    const input = document.getElementById('taskInput');
    const text = input.value.trim();
    
    // Validate input
    if (!text) {
        input.focus();
        return;
    }
    
    // Create task object
    const task = {
        id: Date.now(),
        text: text,
        completed: false,
        createdAt: new Date().toISOString()
    };
    
    tasks.push(task);
    saveTasks();
    renderTasks();
    
    // Clear input
    input.value = '';
    input.focus();
}

/**
 * Toggle task completion status
 * @param {number} taskId - The ID of the task to toggle
 */
function toggleTask(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (task) {
        task.completed = !task.completed;
        saveTasks();
        renderTasks();
    }
}

/**
 * Delete a task
 * @param {number} taskId - The ID of the task to delete
 */
function deleteTask(taskId) {
    const index = tasks.findIndex(t => t.id === taskId);
    if (index !== -1) {
        tasks.splice(index, 1);
        saveTasks();
        renderTasks();
    }
}

/**
 * Save tasks to localStorage
 */
function saveTasks() {
    try {
        localStorage.setItem('ov-code-tasks', JSON.stringify(tasks));
    } catch (error) {
        console.error('Failed to save tasks:', error);
    }
}

/**
 * Render the task list to the DOM
 * Uses textContent instead of innerHTML for XSS prevention
 */
function renderTasks() {
    const taskList = document.getElementById('taskList');
    
    // Clear existing content
    taskList.innerHTML = '';
    
    if (tasks.length === 0) {
        const emptyState = document.createElement('li');
        emptyState.className = 'empty-state';
        emptyState.textContent = 'No tasks yet. Add one above!';
        taskList.appendChild(emptyState);
    } else {
        tasks.forEach(task => {
            const li = document.createElement('li');
            li.className = `task-item${task.completed ? ' completed' : ''}`;
            
            // Checkbox
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'task-checkbox';
            checkbox.checked = task.completed;
            checkbox.setAttribute('aria-label', `Mark "${task.text}" as ${task.completed ? 'incomplete' : 'complete'}`);
            checkbox.addEventListener('change', () => toggleTask(task.id));
            
            // Task text (using textContent for security)
            const span = document.createElement('span');
            span.className = 'task-text';
            span.textContent = task.text;
            
            // Delete button
            const deleteBtn = document.createElement('button');
            deleteBtn.className = 'task-delete';
            deleteBtn.textContent = 'Delete';
            deleteBtn.setAttribute('aria-label', `Delete "${task.text}"`);
            deleteBtn.addEventListener('click', () => deleteTask(task.id));
            
            li.appendChild(checkbox);
            li.appendChild(span);
            li.appendChild(deleteBtn);
            taskList.appendChild(li);
        });
    }
    
    // Update stats
    updateStats();
}

/**
 * Update task statistics
 */
function updateStats() {
    const total = tasks.length;
    const completed = tasks.filter(t => t.completed).length;
    
    document.getElementById('totalTasks').textContent = `${total} task${total !== 1 ? 's' : ''}`;
    document.getElementById('completedTasks').textContent = `${completed} completed`;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);
