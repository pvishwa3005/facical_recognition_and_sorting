const dropZone =
    document.getElementById(
        "dropZone"
    );

const fileInput =
    document.getElementById(
        "fileInput"
    );

const previewContainer =
    document.getElementById(
        "previewContainer"
    );

const uploadForm =
    document.getElementById(
        "uploadForm"
    );

const browseBtn =
    document.getElementById(
        "browseBtn"
    );

const directoryPicker =
    document.getElementById(
        "directoryPicker"
    );

const outputDir =
    document.getElementById(
        "outputDir"
    );


dropZone.addEventListener(
    "dragover",
    (e) => {

        e.preventDefault();

        dropZone.classList.add(
            "dragover"
        );
    }
);

dropZone.addEventListener(
    "dragleave",
    () => {

        dropZone.classList.remove(
            "dragover"
        );
    }
);

dropZone.addEventListener(
    "drop",
    (e) => {

        e.preventDefault();

        dropZone.classList.remove(
            "dragover"
        );

        fileInput.files =
            e.dataTransfer.files;

        showPreview(
            e.dataTransfer.files
        );
    }
);

fileInput.addEventListener(
    "change",
    () => {

        showPreview(
            fileInput.files
        );
    }
);

function showPreview(files) {

    previewContainer.innerHTML = "";

    [...files].forEach(file => {

        const reader =
            new FileReader();

        reader.onload = (e) => {

            const div =
                document.createElement(
                    "div"
                );

            div.className =
                "preview-image";

            div.innerHTML = `
                <img src="${e.target.result}">
            `;

            previewContainer
                .appendChild(div);
        };

        reader.readAsDataURL(file);
    });
}


browseBtn.addEventListener(
    "click",
    () => {

        directoryPicker.click();
    }
);

directoryPicker.addEventListener(
    "change",
    (e) => {

        if (
            e.target.files.length > 0
        ) {

            const path =
                e.target.files[0]
                .webkitRelativePath;

            const folderName =
                path.split("/")[0];

            outputDir.value =
                folderName;
        }
    }
);


uploadForm.addEventListener(
    "submit",
    () => {

        showLoadingOverlay();
    }
);

function showLoadingOverlay() {

    const overlay =
        document.createElement(
            "div"
        );

    overlay.className =
        "loading-overlay";

    overlay.innerHTML = `

        <div class="loader-container">

            <div class="spinner"></div>

            <h2>
                Analyzing Faces...
            </h2>

            <p>
                Sorting your photos
            </p>

        </div>
    `;

    document.body.appendChild(
        overlay
    );
}
