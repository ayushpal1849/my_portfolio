document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.admin-alert .btn-close').forEach((button) => {
        button.addEventListener('click', function() {
            const alert = this.closest('.admin-alert');
            if (alert) {
                alert.remove();
            }
        });
    });

    // --- Form Toggle Logic ---
    const buttons = { // Maps button IDs to their corresponding form IDs
        'btn-add-experience': 'form-experience',
        'btn-add-project': 'form-project',
        'btn-add-certification': 'form-certification',
        'btn-upload-resume': 'form-resume'
    };

    // Get all form elements
    const forms = Object.values(buttons).map(id => document.getElementById(id));

    // Function to hide all forms
    const hideAllForms = () => {
        forms.forEach(form => {
            if (form) form.style.display = 'none';
        });
    };

    // Add click listeners to buttons
    for (const [btnId, formId] of Object.entries(buttons)) {
        const button = document.getElementById(btnId);
        const form = document.getElementById(formId);
        if (button && form) {
            button.addEventListener('click', () => {
                // If the form is already visible, hide it. Otherwise, show it and hide others.
                const isVisible = form.style.display === 'block';
                hideAllForms();
                if (!isVisible) {
                    form.style.display = 'block';
                }
            });
        }
    }

    // --- AJAX Form Submission for Experience and Project ---
    const csrfToken = document.getElementById('csrf_token').value;
    const handleApiResponse = async (response) => {
        let result = { success: false, message: 'Unexpected response from server.' };

        try {
            result = await response.json();
        } catch (error) {
            result = { success: false, message: 'Unable to parse server response.' };
        }

        if (response.status === 401) {
            alert(result.message || 'Your admin session expired. Please log in again.');
            window.location.href = '/admin/login';
            return null;
        }

        if (!response.ok && !result.message) {
            result.message = 'Request failed. Please try again.';
        }

        return result;
    };

    // Handle Experience Form
    const expForm = document.getElementById('form-experience');
    if (expForm) {
        expForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = {
                company: formData.get('company'),
                role: formData.get('role'),
                duration: formData.get('duration'),
                responsibilities: formData.get('responsibilities').split('\n').filter(line => line.trim() !== '')
            };
            
            fetch('/admin/add_experience', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                body: JSON.stringify(data)
            })
            .then(handleApiResponse)
            .then(result => {
                if (!result) return;
                alert(result.message);
                if (result.success) this.reset();
            })
            .catch(() => alert('Unable to add experience right now.'));
        });
    }

    // Handle Project Form
    const projForm = document.getElementById('form-project');
    if (projForm) {
        projForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());

            fetch('/admin/add_project', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                body: JSON.stringify(data)
            })
            .then(handleApiResponse)
            .then(result => {
                if (!result) return;
                alert(result.message);
                if (result.success) this.reset();
            })
            .catch(() => alert('Unable to add project right now.'));
        });
    }

    // Handle Certification Form
    const certForm = document.getElementById('form-certification');
    if (certForm) {
        certForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);

            fetch('/admin/add_certification', {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken }, // No Content-Type, browser sets it for multipart/form-data
                body: formData
            })
            .then(handleApiResponse)
            .then(result => {
                if (!result) return;
                alert(result.message);
                if (result.success) this.reset();
            })
            .catch(() => alert('Unable to add certification right now.'));
        });
    }

    // Handle Resume Upload Form
    const resumeForm = document.getElementById('form-resume');
    if (resumeForm) {
        resumeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);

            fetch('/admin/upload_resume', {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken }, // No Content-Type, browser sets it for multipart/form-data
                body: formData
            })
            .then(handleApiResponse)
            .then(result => {
                if (!result) return;
                alert(result.message); // Use alert to show feedback
                if (result.success) this.reset();
            })
            .catch(() => alert('Unable to upload resume right now.'));
        });
    }
});
