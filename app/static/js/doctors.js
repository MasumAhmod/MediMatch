document.addEventListener("DOMContentLoaded", () => {

    const searchInput =
        document.getElementById("doctor-search");

    const specializationFilter =
        document.getElementById("specialization-filter");

    const cityFilter =
        document.getElementById("city-filter");

    const feeFilter =
        document.getElementById("fee-filter");

    const filterButton =
        document.getElementById("doctor-filter-button");

    const doctorsContainer =
        document.getElementById("doctors-container");

    const loadingElement =
        document.getElementById("doctors-loading");

    const errorElement =
        document.getElementById("doctors-error");


    // =====================================================
    // GET SPECIALIZATION FROM URL
    // =====================================================

    const urlParams =
        new URLSearchParams(window.location.search);

    const urlSpecialization =
        urlParams.get("specialization");


    // =====================================================
    // LOAD SPECIALIZATIONS
    // =====================================================

    async function loadSpecializations() {

        try {

            const response =
                await fetch(
                    "/api/v1/specializations/"
                );

            if (!response.ok) {
                return;
            }

            const data =
                await response.json();

            specializationFilter.innerHTML = `
                <option value="">
                    Specialization
                </option>
            `;


            const specializations =
                data.specializations || [];


            specializations.forEach(item => {

                let specialization;


                if (typeof item === "string") {

                    specialization = item;

                } else {

                    specialization =
                        item.specialization ||
                        item.name ||
                        Object.values(item)[0];

                }


                if (!specialization) {
                    return;
                }


                const option =
                    document.createElement("option");

                option.value =
                    specialization;

                option.textContent =
                    specialization;


                specializationFilter.appendChild(
                    option
                );

            });


            // =================================================
            // SET SPECIALIZATION FROM URL
            // =================================================

            if (urlSpecialization) {

                specializationFilter.value =
                    urlSpecialization;

            }

        } catch (error) {

            console.error(
                "Failed to load specializations:",
                error
            );

        }

    }


    // =====================================================
    // DISPLAY DOCTORS
    // =====================================================

    function displayDoctors(doctors) {

        doctorsContainer.innerHTML = "";


        if (!doctors || doctors.length === 0) {

            doctorsContainer.innerHTML = `
                <div class="col-span-full
                            text-center
                            py-12
                            text-slate-500">

                    No doctors found for this
                    specialization.

                </div>
            `;

            return;
        }


        doctors.forEach(doctor => {

            const card =
                document.createElement("div");


            card.className =
                "bg-white border border-slate-100 " +
                "rounded-2xl p-6 shadow-sm " +
                "hover:shadow-lg transition";


            // =================================================
            // DOCTOR NAME
            // =================================================

            const doctorName =
                doctor.doctor_name ||
                "Unknown Doctor";


            // =================================================
            // SPECIALIZATION
            // =================================================

            const specialization =
                doctor.specialization ||
                "Medical Specialist";


            // =================================================
            // QUALIFICATION
            //
            // Your database uses "degree"
            // =================================================

            const qualification =
                doctor.degree ||
                doctor.qualification ||
                doctor.qualifications ||
                "Qualification not specified";


            // =================================================
            // HOSPITAL
            //
            // Your database uses "chamber_hospital"
            // =================================================

            const hospital =
                doctor.chamber_hospital ||
                doctor.hospital ||
                doctor.hospital_name ||
                doctor.current_workplace ||
                "Hospital not specified";


            // =================================================
            // CURRENT WORKPLACE
            // =================================================

            const currentWorkplace =
                doctor.current_workplace ||
                "";


            // =================================================
            // DESIGNATION
            // =================================================

            const designation =
                doctor.designation ||
                "";


            // =================================================
            // CITY
            // =================================================

            const city =
                doctor.city ||
                "";


            // =================================================
            // VISITING HOURS
            // =================================================

            const visitingHours =
                doctor.visiting_hours ||
                "";


            // =================================================
            // FEE
            // =================================================

            const fee =
                doctor.appointment_fee ??
                doctor.fee ??
                0;


            // =================================================
            // DOCTOR ID
            // =================================================

            const doctorId =
                doctor.doctor_id;


            // =================================================
            // DOCTOR CARD
            // =================================================

            card.innerHTML = `

                <div class="flex items-center gap-4">

                    <div
                        class="w-14 h-14
                               rounded-full
                               bg-blue-50
                               flex items-center
                               justify-center
                               text-2xl"
                    >
                        👨‍⚕️
                    </div>


                    <div>

                        <h3
                            class="text-lg
                                   font-bold
                                   text-slate-900"
                        >
                            ${escapeHTML(doctorName)}
                        </h3>


                        <p
                            class="text-sm
                                   text-blue-600
                                   font-medium"
                        >
                            ${escapeHTML(specialization)}
                        </p>

                    </div>

                </div>


                <div class="mt-5 space-y-2">

                    ${
                        designation
                        ? `
                        <p class="text-sm text-slate-600">

                            <span class="font-semibold">
                                Designation:
                            </span>

                            ${escapeHTML(designation)}

                        </p>
                        `
                        : ""
                    }


                    <p class="text-sm text-slate-600">

                        <span class="font-semibold">
                            Qualification:
                        </span>

                        ${escapeHTML(qualification)}

                    </p>


                    <p class="text-sm text-slate-600">

                        <span class="font-semibold">
                            Hospital:
                        </span>

                        ${escapeHTML(hospital)}

                    </p>


                    ${
                        city
                        ? `
                        <p class="text-sm text-slate-600">

                            <span class="font-semibold">
                                Location:
                            </span>

                            ${escapeHTML(city)}

                        </p>
                        `
                        : ""
                    }


                    ${
                        visitingHours
                        ? `
                        <p class="text-sm text-slate-600">

                            <span class="font-semibold">
                                Visiting Hours:
                            </span>

                            ${escapeHTML(visitingHours)}

                        </p>
                        `
                        : ""
                    }

                </div>


                <div
                    class="mt-5
                           flex items-center
                           justify-between"
                >

                    <p
                        class="font-bold
                               text-slate-800"
                    >
                        Fee: Tk. ${escapeHTML(fee)}
                    </p>


                    <a
                        href="/doctors/${doctorId}"
                        class="bg-blue-600
                               hover:bg-blue-700
                               text-white
                               px-4 py-2
                               rounded-lg
                               text-sm
                               font-semibold
                               transition"
                    >
                        View Profile
                    </a>

                </div>

            `;


            doctorsContainer.appendChild(card);

        });

    }


    // =====================================================
    // ESCAPE HTML
    // =====================================================

    function escapeHTML(value) {

        if (
            value === null ||
            value === undefined
        ) {

            return "";

        }


        return String(value)

            .replace(
                /&/g,
                "&amp;"
            )

            .replace(
                /</g,
                "&lt;"
            )

            .replace(
                />/g,
                "&gt;"
            )

            .replace(
                /"/g,
                "&quot;"
            )

            .replace(
                /'/g,
                "&#039;"
            );

    }


    // =====================================================
    // LOAD DOCTORS
    // =====================================================

    async function loadDoctors() {

        loadingElement.classList.remove(
            "hidden"
        );

        doctorsContainer.innerHTML = "";

        errorElement.classList.add(
            "hidden"
        );


        try {

            let response;


            // =================================================
            // SPECIALIZATION FROM PREDICTION RESULT
            // =================================================

            if (urlSpecialization) {

                const specialization =
                    encodeURIComponent(
                        urlSpecialization
                    );


                const url =
                    `/api/v1/doctors/filter` +
                    `?specialization=${specialization}`;


                response =
                    await fetch(url);

            }


            // =================================================
            // NORMAL FILTER
            // =================================================

            else {

                const params =
                    new URLSearchParams();


                const name =
                    searchInput
                        ? searchInput.value.trim()
                        : "";


                const specialization =
                    specializationFilter
                        ? specializationFilter.value
                        : "";


                const city =
                    cityFilter
                        ? cityFilter.value
                        : "";


                const fee =
                    feeFilter
                        ? feeFilter.value
                        : "";


                if (name) {

                    params.append(
                        "name",
                        name
                    );

                }


                if (specialization) {

                    params.append(
                        "specialization",
                        specialization
                    );

                }


                if (city) {

                    params.append(
                        "city",
                        city
                    );

                }


                if (fee) {

                    params.append(
                        "max_fee",
                        fee
                    );

                }


                if (
                    specialization ||
                    city ||
                    fee
                ) {

                    response =
                        await fetch(
                            `/api/v1/doctors/filter?${params.toString()}`
                        );

                }

                else if (name) {

                    response =
                        await fetch(
                            `/api/v1/doctors/search?name=${encodeURIComponent(name)}`
                        );

                }

                else {

                    response =
                        await fetch(
                            "/api/v1/doctors/"
                        );

                }

            }


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Failed to load doctors."
                );

            }


            displayDoctors(
                data.doctors || []
            );


        } catch (error) {

            console.error(
                "Failed to load doctors:",
                error
            );


            errorElement.textContent =
                error.message ||
                "Failed to load doctors.";


            errorElement.classList.remove(
                "hidden"
            );

        } finally {

            loadingElement.classList.add(
                "hidden"
            );

        }

    }


    // =====================================================
    // FILTER BUTTON
    // =====================================================

    if (filterButton) {

        filterButton.addEventListener(
            "click",
            () => {

                loadDoctors();

            }
        );

    }


    // =====================================================
    // ENTER KEY SEARCH
    // =====================================================

    if (searchInput) {

        searchInput.addEventListener(
            "keydown",
            event => {

                if (event.key === "Enter") {

                    event.preventDefault();

                    loadDoctors();

                }

            }
        );

    }


    // =====================================================
    // INITIAL LOAD
    // =====================================================

    async function initialize() {

        await loadSpecializations();

        await loadDoctors();

    }


    initialize();

});