const inputBox = document.getElementById("input-box");
const linkContainer = document.getElementById("link-container");

linkContainer.addEventListener("click", function(e) {
    if (e.target.tagName === "SPAN") {
        const li = e.target.parentElement;
        const code = li.getAttribute("data-code");

        if (code) {
            fetch(`http://localhost:8000/delete/${code}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (response.ok) {
                    li.remove(); 
                } else {
                    alert("Failed to delete link from server.");
                }
            })
            .catch(error => {
                console.error("Error deleting link:", error);
            });
        }
    }
});

function shortLink() {
    const url = inputBox.value.trim();

    if (url === '') {
        alert("You must write a link!");
        return;
    }

    if (!url.startsWith("http://") && !url.startsWith("https://")) {
        alert("Link must start with http:// or https://");
        return;
    }

    fetch('http://localhost:8000/shorten', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url: url})
    })
    .then(response => response.json())
    .then(data => {
    console.log("Response data:", data);
    if(data.error) {
        alert(data.error);
        return;
    }

    let li = document.createElement("li");
    li.setAttribute("data-code", data.short_url.split("/").pop()); 
    li.innerHTML = `
        <strong>Original:</strong> <a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a> &nbsp;&nbsp;&nbsp; - <strong>Shortened:</strong> <a href="${data.short_url}" target="_blank" rel="noopener noreferrer">${data.short_url}</a>
    `;
    let span = document.createElement("span");
    span .innerHTML = "\u00d7";
    li.appendChild(span);
    
    linkContainer.appendChild(li);
    inputBox.value = '';
})
    .catch(() => {
        alert("Error shortening the URL.");
    });
}
async function loadLinks() {
    try {
        const response = await fetch('http://localhost:8000/links');
        if (!response.ok) {
            throw new Error('Falha ao carregar links');
        }
        const links = await response.json();

        const linkContainer = document.getElementById("link-container");
        linkContainer.innerHTML = ''; 

        links.forEach(link => {
            const shortUrl = `http://localhost:8000/${link.code}`;
            let li = document.createElement("li");
            li.setAttribute("data-code", link.code);
            li.innerHTML = `<strong>Original:</strong> <a href="${link.url}" target="_blank">${link.url}</a> — <strong>Shortened:</strong> <a href="${shortUrl}" target="_blank">${shortUrl}</a>`;
            let span = document.createElement("span");
            span .innerHTML = "\u00d7";
            li.appendChild(span);
            linkContainer.appendChild(li);
        });
    } catch (error) {
        console.error('Erro ao carregar links:', error);
    }
}

window.onload = loadLinks;