const tabSimpleBtn = document.getElementById("tab-simple-btn");
const tabBatchBtn = document.getElementById("tab-batch-btn");
const tabSimple = document.getElementById("tab-simple");
const tabBatch = document.getElementById("tab-batch");

tabSimpleBtn.addEventListener("click", (e) => {
    e.preventDefault();
    tabSimple.classList.add("active");
    tabBatch.classList.remove("active");
});

tabBatchBtn.addEventListener("click", (e) => {
    e.preventDefault();
    tabBatch.classList.add("active");
    tabSimple.classList.remove("active");
});

const form = document.getElementById("analyze-form");
const resultBox = document.getElementById("result-box");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const cvFile = document.getElementById("cv_file").files[0];
    const aoFile = document.getElementById("ao_file").files[0];
    const question = document.getElementById("question").value;

    if (!cvFile || !aoFile) {
        resultBox.innerText = "Veuillez uploader un CV et un AO.";
        return;
    }

    const formData = new FormData();
    formData.append("cv_file", cvFile);
    formData.append("ao_file", aoFile);
    formData.append("question", question);

    resultBox.innerText = "Analyse en cours...";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            resultBox.innerText = "Erreur : " + JSON.stringify(data, null, 2);
            return;
        }

        const score = data?.matching?.score ?? "N/A";
        const missing = data?.matching?.competences_manquantes ?? [];
        const resume = data?.matching?.resume ?? "";
        const positionnement = data?.matching?.positionnement_candidat ?? "";
        const reponse = data?.reponse_commerciale ?? "";

        resultBox.innerText =
            `Score de matching : ${score}\n\n` +
            `Positionnement : ${positionnement}\n\n` +
            `Résumé : ${resume}\n\n` +
            `Compétences manquantes : ${missing.join(", ")}\n\n` +
            `Réponse commerciale : ${reponse}`;
    } catch (error) {
        resultBox.innerText = "Erreur réseau : " + error.message;
    }
});

const batchForm = document.getElementById("batch-form");
const batchResultBox = document.getElementById("batch-result-box");
const rankingTableBody = document.querySelector("#ranking-table tbody");
const exportCsvBtn = document.getElementById("export-csv-btn");

batchForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const aoFile = document.getElementById("batch_ao_file").files[0];
    const cvFiles = document.getElementById("batch_cv_files").files;

    if (!aoFile || cvFiles.length === 0) {
        batchResultBox.innerText = "Veuillez uploader un AO et plusieurs CV.";
        return;
    }

    const formData = new FormData();
    formData.append("ao_file", aoFile);

    for (const file of cvFiles) {
        formData.append("cv_files", file);
    }

    batchResultBox.innerText = "Scoring et ranking en cours...";
    rankingTableBody.innerHTML = "";

    try {
        const response = await fetch("/rank_candidates", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            batchResultBox.innerText = "Erreur : " + JSON.stringify(data, null, 2);
            return;
        }

        batchResultBox.innerText = `Classement terminé. ${data.nombre_candidats} candidats analysés.`;

        const rows = data?.tableau?.rows ?? [];

        rows.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${row.nom || ""}</td>
                <td>${row.prenom || ""}</td>
                <td>${row.profil || ""}</td>
                <td>${row.competences || ""}</td>
                <td>${row.taches || ""}</td>
                <td>${row.ecarts || ""}</td>
                <td>${row.score_similarite || ""}</td>
                <td>${row.rang || ""}</td>
                <td>${row.decision_ia || ""}</td>
            `;
            rankingTableBody.appendChild(tr);
        });
    } catch (error) {
        batchResultBox.innerText = "Erreur réseau : " + error.message;
    }
});

exportCsvBtn.addEventListener("click", async () => {
    const aoFile = document.getElementById("batch_ao_file").files[0];
    const cvFiles = document.getElementById("batch_cv_files").files;

    if (!aoFile || cvFiles.length === 0) {
        batchResultBox.innerText = "Veuillez uploader un AO et plusieurs CV avant export.";
        return;
    }

    const formData = new FormData();
    formData.append("ao_file", aoFile);

    for (const file of cvFiles) {
        formData.append("cv_files", file);
    }

    try {
        const response = await fetch("/rank_candidates_csv", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            batchResultBox.innerText = "Erreur export CSV : " + JSON.stringify(error, null, 2);
            return;
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "ranking_candidats.csv";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        batchResultBox.innerText = "Erreur réseau export : " + error.message;
    }
});
