document.addEventListener("DOMContentLoaded", () => {

    const diseaseElement =
        document.getElementById("result-disease");

    const specializationElement =
        document.getElementById(
            "result-specialization"
        );


    const stored =
        sessionStorage.getItem(
            "medimatchPrediction"
        );


    if (!stored) {

        diseaseElement.textContent =
            "No prediction available.";

        specializationElement.textContent =
            "Please perform a prediction first.";

        return;

    }


    try {

        const result =
            JSON.parse(stored);


        diseaseElement.textContent =
            result.disease ||
            "Unknown";


        specializationElement.textContent =
            result.specialization ||
            "Not available";


    } catch (error) {

        console.error(
            "Failed to load prediction:",
            error
        );

    }

});