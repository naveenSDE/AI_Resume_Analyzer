document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('resume');
    const fileLabel = document.getElementById('file-label');
    const uploadForm = document.querySelector('.upload-form');
    const loadingOverlay = document.getElementById('loading-overlay');

    // Drag & Drop Functionality
    if (dropZone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });

        function highlight(e) {
            dropZone.classList.add('highlight');
        }

        function unhighlight(e) {
            dropZone.classList.remove('highlight');
        }

        dropZone.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;

            if (files.length > 0) {
                fileInput.files = files;
                updateFileLabel(files[0].name);
            }
        }

        fileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                updateFileLabel(this.files[0].name);
            }
        });

        function updateFileLabel(filename) {
            fileLabel.textContent = filename;
            dropZone.classList.add('file-selected');
        }
    }

    // Form Submission & Loading State
    if (uploadForm) {
        uploadForm.addEventListener('submit', function (e) {
            // Basic validation
            if (!fileInput.value && !dropZone.classList.contains('file-selected')) {
                e.preventDefault();
                alert('Please upload a resume.');
                return;
            }

            loadingOverlay.classList.remove('hidden');
        });
    }
});
