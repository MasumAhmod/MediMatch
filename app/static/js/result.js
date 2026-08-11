document.addEventListener("DOMContentLoaded", () => {

    // =====================================================
    // ELEMENTS
    // =====================================================

    const diseaseElement =
        document.getElementById("result-disease");

    const specializationElement =
        document.getElementById("result-specialization");

    const viewDoctorsButton =
        document.getElementById("view-doctors-button");


    // =====================================================
    // GET PREDICTION
    // =====================================================

    const storedPrediction =
        sessionStorage.getItem("medimatchPrediction");


    if (!storedPrediction) {

        diseaseElement.textContent =
            "No prediction found.";

        specializationElement.textContent =
            "No specialist found.";

        viewDoctorsButton.href =
            "/doctors";

        return;
    }


    // =====================================================
    // PARSE PREDICTION
    // =====================================================

    let prediction;

    try {

        prediction =
            JSON.parse(storedPrediction);

    } catch (error) {

        console.error(
            "Invalid prediction data:",
            error
        );

        diseaseElement.textContent =
            "Unable to load prediction.";

        specializationElement.textContent =
            "Unable to load specialist.";

        return;
    }


    console.log(
        "Prediction received:",
        prediction
    );


    // =====================================================
    // GET DISEASE
    // =====================================================

    const disease =
        prediction.disease ||
        prediction.predicted_disease ||
        prediction.prediction ||
        prediction.result ||
        "Unknown Disease";


    // =====================================================
    // GET SPECIALIZATION
    // =====================================================

    const specialization =
        prediction.specialization ||
        prediction.specialist ||
        prediction.recommended_specialization ||
        prediction.recommendedSpecialization ||
        "";


    // =====================================================
    // DISPLAY RESULT
    // =====================================================

    diseaseElement.textContent =
        disease;


    specializationElement.textContent =
        specialization || "Not available";


    // =====================================================
    // VIEW DOCTORS BUTTON
    // =====================================================

    if (specialization) {

        const encodedSpecialization =
            encodeURIComponent(
                specialization.trim()
            );


        viewDoctorsButton.href =
            `/doctors?specialization=${encodedSpecialization}`;


        console.log(
            "Doctors URL:",
            viewDoctorsButton.href
        );

    } else {

        viewDoctorsButton.href =
            "/doctors";

    }

});