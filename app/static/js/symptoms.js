document.addEventListener("DOMContentLoaded", () => {

    // =====================================================
    // ELEMENTS
    // =====================================================

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


    // =====================================================
    // STATE
    // =====================================================

    let selectedSymptoms = [];

    let naturalLanguageText = "";


    // =====================================================
    // ADD SYMPTOM
    // =====================================================

    function addSymptom(symptom) {

        symptom = symptom.trim();

        if (!symptom) {
            return;
        }

        const normalized =
            symptom.toLowerCase();


        // Prevent duplicate symptoms
        const alreadySelected =
            selectedSymptoms.some(
                item =>
                    item.toLowerCase() === normalized
            );


        if (alreadySelected) {
            return;
        }


        selectedSymptoms.push(symptom);


        // If user manually selects symptoms,
        // remove natural-language input.
        naturalLanguageText = "";


        renderSelectedSymptoms();
    }


    // =====================================================
    // REMOVE SYMPTOM
    // =====================================================

    function removeSymptom(symptom) {

        selectedSymptoms =
            selectedSymptoms.filter(
                item =>
                    item.toLowerCase() !==
                    symptom.toLowerCase()
            );

        renderSelectedSymptoms();
    }


    // =====================================================
    // RENDER SELECTED SYMPTOMS
    // =====================================================

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


            selectedContainer.appendChild(
                element
            );
        });
    }


    // =====================================================
    // SHOW NATURAL-LANGUAGE INPUT
    // =====================================================

    function showNaturalLanguage(text) {

        naturalLanguageText =
            text.trim();


        if (!naturalLanguageText) {
            return;
        }


        // Natural language has priority,
        // so clear manually selected symptoms.
        selectedSymptoms = [];


        selectedContainer.innerHTML = `
            <div class="natural-language-input">

                <span>
                    ${escapeHtml(naturalLanguageText)}
                </span>

                <button
                    type="button"
                    id="remove-natural-language"
                    aria-label="Remove description"
                >
                    ×
                </button>

            </div>
        `;


        countElement.textContent = "1";


        const removeButton =
            document.getElementById(
                "remove-natural-language"
            );


        if (removeButton) {

            removeButton.addEventListener(
                "click",
                () => {

                    naturalLanguageText = "";

                    selectedContainer.innerHTML = "";

                    countElement.textContent = "0";
                }
            );
        }
    }


    // =====================================================
    // ESCAPE HTML
    // =====================================================

    function escapeHtml(value) {

        const div =
            document.createElement("div");

        div.textContent = value;

        return div.innerHTML;
    }


    // =====================================================
    // SUGGESTED SYMPTOMS
    // =====================================================

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


    // =====================================================
    // SEARCH / NATURAL LANGUAGE INPUT
    // =====================================================

    if (searchInput) {

        searchInput.addEventListener(
            "keydown",
            event => {

                if (event.key !== "Enter") {
                    return;
                }


                event.preventDefault();


                const text =
                    searchInput.value.trim();


                if (!text) {
                    return;
                }


                /*
                 * If the user enters a sentence such as:
                 *
                 * "I have fever, headache and cough"
                 *
                 * send the entire sentence to FastAPI.
                 *
                 * symptom_extractor.py will extract:
                 *
                 * ["fever", "headache", "cough"]
                 */

                showNaturalLanguage(text);


                searchInput.value = "";
            }
        );
    }


    // =====================================================
    // PREDICT DISEASE
    // =====================================================

    if (predictButton) {

        predictButton.addEventListener(
            "click",
            async () => {

                // Clear previous error
                errorElement.classList.add(
                    "hidden"
                );


                // =================================================
                // VALIDATION
                // =================================================

                if (
                    !naturalLanguageText &&
                    selectedSymptoms.length === 0
                ) {

                    errorElement.textContent =
                        "Please describe your symptoms or select at least one symptom.";

                    errorElement.classList.remove(
                        "hidden"
                    );

                    return;
                }


                // =================================================
                // LOADING
                // =================================================

                predictButton.disabled = true;

                predictButton.textContent =
                    "Predicting...";


                try {

                    // =================================================
                    // BUILD REQUEST
                    // =================================================

                    let requestBody;


                    /*
                     * Natural-language input
                     */

                    if (naturalLanguageText) {

                        requestBody = {
                            text: naturalLanguageText
                        };

                    }


                    /*
                     * Direct symptom selection
                     */

                    else {

                        requestBody = {
                            symptoms:
                                selectedSymptoms
                        };

                    }


                    // =================================================
                    // API REQUEST
                    // =================================================

                    const response =
                        await fetch(
                            "/api/v1/predict/",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(
                                        requestBody
                                    )
                            }
                        );


                    // =================================================
                    // READ RESPONSE
                    // =================================================

                    const data =
                        await response.json();


                    // =================================================
                    // API ERROR
                    // =================================================

                    if (!response.ok) {

                        throw new Error(
                            data.detail ||
                            "Prediction failed."
                        );
                    }


                    // =================================================
                    // STORE RESULT
                    // =================================================

                    sessionStorage.setItem(
                        "medimatchPrediction",
                        JSON.stringify(data)
                    );


                    // =================================================
                    // RESULT PAGE
                    // =================================================

                    window.location.href =
                        "/result";

                }


                // =================================================
                // ERROR HANDLING
                // =================================================

                catch (error) {

                    errorElement.textContent =
                        error.message ||
                        "Something went wrong.";

                    errorElement.classList.remove(
                        "hidden"
                    );

                }


                // =================================================
                // FINALLY
                // =================================================

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