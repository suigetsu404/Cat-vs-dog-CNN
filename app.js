document.addEventListener('DOMContentLoaded', () => {
    const imageForm = document.getElementById('image-form');

    async function apiFetch(path, opts = {}) {
        // const url = 'http://localhost:5000' + path;
        const url = path;
        return fetch(url, { ...opts });
    }

    function setStatus(msg){
        const el = document.getElementById('status');
        if (el) el.textContent = msg;
        document.body.setAttribute('status', msg);
    }
    
    imageForm.action = '/upload';
    imageForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fd = new FormData(imageForm)
        const file = document.getElementById('image-input').files[0];
            if (file){
                const imageURL = URL.createObjectURL(file)
                document.getElementById('image-preview').src = imageURL
            }
            else{
                document.getElementById('image-preview').src = ''
            }
        setStatus('Uploading image...')
        try {
            const res = await apiFetch('/upload', {method: 'POST', body: fd });
            let data;
            try{
                data = await res.json();
            } catch (jsonError){
                setStatus(`Server error (${res.status})`)
                return;
            }
            if (res.ok){
                prediction(data)
                document.body.setAttribute('image', fd)
            } else {
                setStatus(`Error: ${data.error || 'unknown error'}`)
                alert(`Error: ${data.error || 'unknown error'}`);
            }
        } catch (err){
            console.error('Image upload error', err);
            setStatus('Network error during upload.')
            alert('Network error during image upload');
        }
    });

    function prediction(data) {
        const entries = Object.entries(data);
        entries.sort((a, b) => b[1] - a[1]);
        const bestMatch = entries[0]
        const bestClass = bestMatch[0]
        const bestScore = (bestMatch[1] * 100).toFixed(0);
        setStatus(`Image shows ${bestClass} (confidence: ${bestScore}%)`)
    }
})