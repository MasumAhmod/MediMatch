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
                <div style="grid-column: 1 / -1; text-align: center; padding: 3rem 1rem; color: #64748b; font-size: 0.95rem;">
                    No doctors found matching your criteria.
                </div>
            `;

            return;
        }

        doctors.forEach(doctor => {

            const card =
                document.createElement("div");

            card.style.cssText =
                "background: #ffffff; border: 1px solid #e2e8f0; border-radius: 1rem; padding: 1.25rem; box-shadow: 0 4px 18px rgba(15, 23, 42, 0.04); display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;";

            card.addEventListener("mouseenter", () => {
                card.style.transform = "translateY(-3px)";
                card.style.boxShadow = "0 12px 28px rgba(37, 99, 235, 0.08)";
                card.style.borderColor = "#bfdbfe";
            });

            card.addEventListener("mouseleave", () => {
                card.style.transform = "translateY(0)";
                card.style.boxShadow = "0 4px 18px rgba(15, 23, 42, 0.04)";
                card.style.borderColor = "#e2e8f0";
            });

            const doctorName =
                doctor.doctor_name ||
                "Unknown Doctor";

            const specialization =
                doctor.specialization ||
                "Medical Specialist";

            const qualification =
                doctor.degree ||
                doctor.qualification ||
                doctor.qualifications ||
                "Qualification not specified";

            const hospital =
                doctor.chamber_hospital ||
                doctor.hospital ||
                doctor.hospital_name ||
                doctor.current_workplace ||
                "Hospital not specified";

            const currentWorkplace =
                doctor.current_workplace ||
                "";

            const designation =
                doctor.designation ||
                "";

            const city =
                doctor.city ||
                "";

            const visitingHours =
                doctor.visiting_hours ||
                "";

            const fee =
                doctor.appointment_fee ??
                doctor.fee ??
                0;

            const doctorId =
                doctor.doctor_id;

            card.innerHTML = `
                <div>
                    <div style="display: flex; align-items: center; gap: 0.85rem;">
                        <div
                            style="width: 48px; height: 48px; border-radius: 50%; background: #eff6ff; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; flex-shrink: 0; border: 1px solid #dbeafe;"
                        >
                            👨‍⚕️
                        </div>

                        <div style="min-width: 0; flex: 1;">
                            <h3
                                style="font-size: 1.05rem; font-weight: 750; color: #0f172a; word-break: break-word; line-height: 1.25; margin: 0;"
                            >
                                ${escapeHTML(doctorName)}
                            </h3>

                            <p
                                style="font-size: 0.82rem; color: #2563eb; font-weight: 600; word-break: break-word; margin-top: 0.2rem;"
                            >
                                ${escapeHTML(specialization)}
                            </p>
                        </div>
                    </div>

                    <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.4rem; font-size: 0.82rem; color: #475569;">
                        ${
                            designation
                            ? `
                            <p style="margin: 0; word-break: break-word;">
                                <strong style="color: #334155;">Designation:</strong>
                                ${escapeHTML(designation)}
                            </p>
                            `
                            : ""
                        }

                        <p style="margin: 0; word-break: break-word;">
                            <strong style="color: #334155;">Qualification:</strong>
                            ${escapeHTML(qualification)}
                        </p>

                        <p style="margin: 0; word-break: break-word;">
                            <strong style="color: #334155;">Hospital:</strong>
                            ${escapeHTML(hospital)}
                        </p>

                        ${
                            city
                            ? `
                            <p style="margin: 0; word-break: break-word;">
                                <strong style="color: #334155;">Location:</strong>
                                ${escapeHTML(city)}
                            </p>
                            `
                            : ""
                        }

                        ${
                            visitingHours
                            ? `
                            <p style="margin: 0; word-break: break-word;">
                                <strong style="color: #334155;">Visiting Hours:</strong>
                                ${escapeHTML(visitingHours)}
                            </p>
                            `
                            : ""
                        }
                    </div>
                </div>

                <div
                    style="margin-top: 1.25rem; padding-top: 0.85rem; border-top: 1px solid #f1f5f9; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 0.75rem;"
                >
                    <p
                        style="font-weight: 800; color: #0f172a; font-size: 0.95rem; white-space: nowrap; margin: 0;"
                    >
                        Fee: Tk. ${escapeHTML(fee)}
                    </p>

                    <a
                        href="/doctors/${doctorId}"
                        class="btn btn-primary"
                        style="padding: 0.45rem 1rem; min-height: 38px; font-size: 0.82rem;"
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
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

    }


    // =====================================================
    // LOAD DOCTORS
    // =====================================================

    async function loadDoctors() {

        loadingElement.classList.remove("hidden");
        doctorsContainer.innerHTML = "";
        errorElement.classList.add("hidden");

        try {

            let response;

            if (urlSpecialization) {

                const specialization =
                    encodeURIComponent(urlSpecialization);

                const url =
                    `/api/v1/doctors/filter?specialization=${specialization}`;

                response =
                    await fetch(url);

            } else {

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
                    params.append("name", name);
                }

                if (specialization) {
                    params.append("specialization", specialization);
                }

                if (city) {
                    params.append("city", city);
                }

                if (fee) {
                    params.append("max_fee", fee);
                }

                if (specialization || city || fee) {

                    response =
                        await fetch(
                            `/api/v1/doctors/filter?${params.toString()}`
                        );

                } else if (name) {

                    response =
                        await fetch(
                            `/api/v1/doctors/search?name=${encodeURIComponent(name)}`
                        );

                } else {

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

            errorElement.classList.remove("hidden");

        } finally {

            loadingElement.classList.add("hidden");

        }

    }


    // =====================================================
    // EVENTS
    // =====================================================

    if (filterButton) {

        filterButton.addEventListener("click", () => {
            loadDoctors();
        });

    }

    if (searchInput) {

        searchInput.addEventListener("keydown", event => {

            if (event.key === "Enter") {
                event.preventDefault();
                loadDoctors();
            }

        });

    }

    async function initialize() {

        await loadSpecializations();
        await loadDoctors();

    }

    initialize();

});