document.addEventListener("DOMContentLoaded", () => {

    const searchInput =
        document.getElementById("symptom-search");

    const selectedContainer =
        document.getElementById("selected-symptoms");

    const countElement =
        document.getElementById("symptom-count");

    const predictButton =
        document.getElementById("predict-button");

    const errorElement =
        document.getElementById("prediction-error");


    let selectedSymptoms = [];


    /* =====================================================
       ADD SYMPTOM
       ===================================================== */

    function addSymptom(symptom) {

        symptom = symptom.trim();

        if (!symptom) {
            return;
        }


        const normalized =
            symptom.toLowerCase();


        const alreadySelected =
            selectedSymptoms.some(
                item =>
                    item.toLowerCase() === normalized
            );


        if (alreadySelected) {
            return;
        }


        selectedSymptoms.push(symptom);

        renderSelectedSymptoms();

    }


    /* =====================================================
       REMOVE SYMPTOM
       ===================================================== */

    function removeSymptom(symptom) {

        selectedSymptoms =
            selectedSymptoms.filter(
                item =>
                    item.toLowerCase() !==
                    symptom.toLowerCase()
            );


        renderSelectedSymptoms();

    }


    /* =====================================================
       RENDER SELECTED SYMPTOMS
       ===================================================== */

    function renderSelectedSymptoms() {

        selectedContainer.innerHTML = "";


        countElement.textContent =
            selectedSymptoms.length;


        selectedSymptoms.forEach(symptom => {

            const element =
                document.createElement("span");


            element.className =
                "selected-symptom";


            element.innerHTML = `

                <span>
                    ${escapeHtml(symptom)}
                </span>

                <button
                    type="button"
                    aria-label="Remove ${escapeHtml(symptom)}"
                >
                    ×
                </button>

            `;


            const removeButton =
                element.querySelector("button");


            removeButton.addEventListener(
                "click",
                () => removeSymptom(symptom)
            );


            selectedContainer.appendChild(element);

        });

    }


    /* =====================================================
       ESCAPE HTML
       ===================================================== */

    function escapeHtml(value) {

        const div =
            document.createElement("div");

        div.textContent = value;

        return div.innerHTML;

    }


    /* =====================================================
       SUGGESTED SYMPTOMS
       ===================================================== */

    document
        .querySelectorAll(".symptom-chip")
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    addSymptom(
                        button.textContent
                    );

                }
            );

        });


    /* =====================================================
       SEARCH INPUT
       ===================================================== */

    if (searchInput) {

        searchInput.addEventListener(
            "keydown",
            event => {

                if (event.key === "Enter") {

                    event.preventDefault();


                    addSymptom(
                        searchInput.value
                    );


                    searchInput.value = "";

                }

            }
        );

    }


    /* =====================================================
       PREDICTION
       ===================================================== */

    if (predictButton) {

        predictButton.addEventListener(
            "click",
            async () => {

                errorElement.classList.add("hidden");


                /* -----------------------------------------
                   Validate
                   ----------------------------------------- */

                if (
                    selectedSymptoms.length === 0
                ) {

                    errorElement.textContent =
                        "Please select at least one symptom.";

                    errorElement.classList.remove(
                        "hidden"
                    );

                    return;

                }


                /* -----------------------------------------
                   Loading
                   ----------------------------------------- */

                predictButton.disabled = true;

                predictButton.textContent =
                    "Predicting...";


                try {

                    /* -------------------------------------
                       API REQUEST
                       ------------------------------------- */

                    const response =
                        await fetch(
                            "/api/v1/predict/",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify({
                                    symptoms:
                                        selectedSymptoms
                                })
                            }
                        );


                    const data =
                        await response.json();


                    /* -------------------------------------
                       API ERROR
                       ------------------------------------- */

                    if (!response.ok) {

                        throw new Error(
                            data.detail ||
                            "Prediction failed."
                        );

                    }


                    /* -------------------------------------
                       STORE RESULT
                       ------------------------------------- */

                    sessionStorage.setItem(
                        "medimatchPrediction",
                        JSON.stringify(data)
                    );


                    /* -------------------------------------
                       RESULT PAGE
                       ------------------------------------- */

                    window.location.href =
                        "/result";

                }


                catch (error) {

                    errorElement.textContent =
                        error.message ||
                        "Something went wrong.";

                    errorElement.classList.remove(
                        "hidden"
                    );

                }


                finally {

                    predictButton.disabled =
                        false;

                    predictButton.textContent =
                        "Predict Disease";

                }

            }
        );

    }

});