document.addEventListener("DOMContentLoaded", () => {

    const container =
        document.getElementById(
            "doctors-container"
        );

    const loading =
        document.getElementById(
            "doctors-loading"
        );

    const errorElement =
        document.getElementById(
            "doctors-error"
        );


    // ==========================================
    // Get URL doctor ID
    // ==========================================

    const pathParts =
        window.location.pathname
            .split("/")
            .filter(Boolean);


    const doctorId =
        pathParts[0] === "doctor"
            ? pathParts[1]
            : null;


    if (doctorId) {

        loadDoctorProfile(
            doctorId
        );

        return;

    }


    if (container) {

        loadDoctors();

    }


    // ==========================================
    // Load doctors
    // ==========================================

    async function loadDoctors(
        params = {}
    ) {

        try {

            loading.classList.remove(
                "hidden"
            );

            errorElement.classList.add(
                "hidden"
            );


            const query =
                new URLSearchParams();


            Object.entries(params)
                .forEach(([key, value]) => {

                    if (value) {

                        query.append(
                            key,
                            value
                        );

                    }

                });


            let url =
                "/api/v1/doctors/";


            if (query.toString()) {

                url +=
                    "?" +
                    query.toString();

            }


            const response =
                await fetch(url);


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Unable to load doctors."
                );

            }


            renderDoctors(
                data.doctors || []
            );


        } catch (error) {

            errorElement.textContent =
                error.message;

            errorElement.classList.remove(
                "hidden"
            );

        } finally {

            loading.classList.add(
                "hidden"
            );

        }

    }


    // ==========================================
    // Render doctors
    // ==========================================

    function renderDoctors(doctors) {

        container.innerHTML = "";


        if (!doctors.length) {

            container.innerHTML = `
                <div class="col-span-full text-center py-12 text-slate-500">
                    No doctors found.
                </div>
            `;

            return;

        }


        doctors.forEach(doctor => {

            const card =
                document.createElement("div");

            card.className =
                "bg-white border border-slate-100 rounded-2xl overflow-hidden shadow-sm hover:shadow-lg transition";


            card.innerHTML = `

                <div class="h-56 bg-slate-100 flex items-center justify-center">

                    <div class="w-full h-full flex items-center justify-center text-slate-400">

                        <span class="text-6xl">
                            👨‍⚕️
                        </span>

                    </div>

                </div>


                <div class="p-5">

                    <h3 class="font-bold text-lg">
                        ${escapeHtml(
                            doctor.doctor_name || ""
                        )}
                    </h3>


                    <p class="text-sm text-blue-600 mt-1">
                        ${escapeHtml(
                            doctor.specialization || ""
                        )}
                    </p>


                    <p class="text-sm text-slate-500 mt-3">
                        ${escapeHtml(
                            doctor.degree || ""
                        )}
                    </p>


                    <p class="text-sm text-slate-500 mt-2">
                        ${escapeHtml(
                            doctor.chamber_hospital || ""
                        )}
                    </p>


                    <p class="text-sm font-semibold text-slate-700 mt-3">
                        Fee: ৳${doctor.appointment_fee ?? "N/A"}
                    </p>


                    <a
                        href="/doctor/${doctor.doctor_id}"
                        class="block text-center mt-5 bg-blue-50 hover:bg-blue-100 text-blue-700 py-2.5 rounded-lg font-semibold text-sm"
                    >
                        View Profile
                    </a>

                </div>

            `;


            container.appendChild(card);

        });

    }


    // ==========================================
    // Load doctor profile
    // ==========================================

    async function loadDoctorProfile(id) {

        const profile =
            document.getElementById(
                "doctor-profile"
            );


        if (!profile) {
            return;
        }


        try {

            const response =
                await fetch(
                    `/api/v1/doctors/${id}`
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Doctor not found."
                );

            }


            const doctor =
                data.doctor;


            profile.innerHTML = `

                <div class="bg-white border rounded-2xl overflow-hidden">

                    <div class="grid lg:grid-cols-[280px_1fr_260px] gap-0">


                        <div class="bg-slate-100 min-h-72 flex items-center justify-center">

                            <span class="text-8xl">
                                👨‍⚕️
                            </span>

                        </div>


                        <div class="p-8">

                            <p class="text-sm text-blue-600 font-semibold">
                                ${escapeHtml(
                                    doctor.specialization || ""
                                )}
                            </p>


                            <h1 class="text-3xl font-bold mt-2">
                                ${escapeHtml(
                                    doctor.doctor_name || ""
                                )}
                            </h1>


                            <p class="mt-3 text-slate-600">
                                ${escapeHtml(
                                    doctor.degree || ""
                                )}
                            </p>


                            <p class="mt-2 text-slate-600">
                                ${escapeHtml(
                                    doctor.designation || ""
                                )}
                            </p>


                            <p class="mt-5 text-sm text-slate-500">
                                ${escapeHtml(
                                    doctor.current_workplace || ""
                                )}
                            </p>

                        </div>


                        <div class="bg-blue-50 p-8">

                            <p class="text-sm font-semibold text-slate-600">
                                Appointment Fee
                            </p>


                            <p class="text-3xl font-bold text-teal-600 mt-2">
                                ৳${doctor.appointment_fee ?? "N/A"}
                            </p>


                            <a
                                href="tel:${doctor.appointment_phone || ""}"
                                class="block text-center mt-6 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold"
                            >
                                Call Doctor
                            </a>

                        </div>

                    </div>


                    <div class="grid md:grid-cols-3 border-t">

                        <div class="p-6 border-b md:border-b-0 md:border-r">

                            <h3 class="font-semibold">
                                Visiting Hours
                            </h3>

                            <p class="text-sm text-slate-500 mt-2">
                                ${escapeHtml(
                                    doctor.visiting_hours || "Not available"
                                )}
                            </p>

                        </div>


                        <div class="p-6 border-b md:border-b-0 md:border-r">

                            <h3 class="font-semibold">
                                Chamber
                            </h3>

                            <p class="text-sm text-slate-500 mt-2">
                                ${escapeHtml(
                                    doctor.chamber_hospital || "Not available"
                                )}
                            </p>

                            <p class="text-sm text-slate-500 mt-1">
                                ${escapeHtml(
                                    doctor.city || ""
                                )}
                            </p>

                        </div>


                        <div class="p-6">

                            <h3 class="font-semibold">
                                Contact
                            </h3>

                            <p class="text-sm text-slate-500 mt-2">
                                ${escapeHtml(
                                    doctor.appointment_phone || "Not available"
                                )}
                            </p>

                        </div>

                    </div>

                </div>

            `;


        } catch (error) {

            profile.innerHTML = `

                <div class="p-6 bg-red-50 text-red-700 rounded-lg">
                    ${escapeHtml(error.message)}
                </div>

            `;

        }

    }


    // ==========================================
    // Filter
    // ==========================================

    const filterButton =
        document.getElementById(
            "doctor-filter-button"
        );


    if (filterButton) {

        filterButton.addEventListener(
            "click",
            () => {

                const specialization =
                    document.getElementById(
                        "specialization-filter"
                    ).value;


                const city =
                    document.getElementById(
                        "city-filter"
                    ).value;


                const maxFee =
                    document.getElementById(
                        "fee-filter"
                    ).value;


                loadDoctors({

                    specialization:
                        specialization,

                    city:
                        city,

                    max_fee:
                        maxFee

                });

            }
        );

    }


    // ==========================================
    // HTML escape
    // ==========================================

    function escapeHtml(value) {

        if (value === null ||
            value === undefined) {

            return "";

        }


        return String(value)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");

    }

});