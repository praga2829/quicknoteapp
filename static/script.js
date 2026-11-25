// Save a new note
async function saveNote() {

    const input = document.getElementById("noteInput");

    const content = input.value.trim();

    if (content === "") {
        alert("Please write a note!");
        return;
    }

    try {
        const response = await fetch("/save", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                content: content
            })
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.message);
            return;
        }

        alert(result.message);

        input.value = "";

        loadNotes();

    } catch (error) {
        alert("Unable to save note!");
        console.error(error);
    }
}


// Display saved notes
async function loadNotes() {

    try {
        const response = await fetch("/notes");

        const notes = await response.json();

        const notesList = document.getElementById("notesList");

        notesList.innerHTML = "";

        notes.forEach(note => {

            const div = document.createElement("div");

            div.className = "note";

            div.textContent = note.content;

            notesList.appendChild(div);

        });

    } catch (error) {
        console.error("Error loading notes:", error);
    }
}


// Load notes when page opens
loadNotes();