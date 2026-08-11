document.addEventListener(
    "DOMContentLoaded",
    async () => {


        // =====================================================
        // ELEMENT
        // =====================================================

        const profileContainer =
            document.getElementById(
                "doctor-profile"
            );


        if (!profileContainer) {

            console.error(
                "Doctor profile container not found."
            );

            return;

        }


        // =====================================================
        // GET DOCTOR ID
        // =====================================================

        const pathParts =
            window.location.pathname
                .split("/")
                .filter(Boolean);


        const doctorId =
            pathParts[pathParts.length - 1];


        if (
            !doctorId ||
            !/^\d+$/.test(doctorId)
        ) {

            showError(
                "Invalid doctor ID."
            );

            return;

        }


        // =====================================================
        // LOAD DOCTOR
        // =====================================================

        async function loadDoctor() {

            try {

                const response =
                    await fetch(
                        `/api/v1/doctors/${doctorId}`
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
                    data.doctor ||
                    data;


                displayDoctor(
                    doctor
                );


            }
            catch (error) {

                console.error(
                    "Failed to load doctor:",
                    error
                );


                showError(
                    error.message ||
                    "Failed to load doctor profile."
                );

            }

        }


        // =====================================================
        // DISPLAY DOCTOR
        // =====================================================

        function displayDoctor(
            doctor
        ) {


            // -------------------------------------------------
            // BASIC INFORMATION
            // -------------------------------------------------

            const doctorName =
                doctor.doctor_name ||
                doctor.name ||
                doctor.full_name ||
                "Unknown Doctor";


            const specialization =
                doctor.specialization ||
                doctor.speciality ||
                doctor.specialty ||
                "Medical Specialist";


            const designation =
                doctor.designation ||
                doctor.position ||
                doctor.current_position ||
                doctor.title ||
                "Medical Professional";


            // -------------------------------------------------
            // QUALIFICATION
            // -------------------------------------------------

            const qualification =
                doctor.qualification ||
                doctor.qualifications ||
                doctor.Qualification ||
                doctor.Qualifications ||
                doctor.degree ||
                doctor.education ||
                doctor.educational_qualification ||
                "Not specified";


            // -------------------------------------------------
            // WORKPLACE
            // -------------------------------------------------

            const workplace =
                doctor.current_workplace ||
                doctor.currentWorkplace ||
                doctor.workplace ||
                doctor.current_hospital ||
                doctor.hospital ||
                doctor.hospital_name ||
                "Not specified";


            // -------------------------------------------------
            // CHAMBER
            // -------------------------------------------------

            const chamber =
                doctor.chamber_hospital ||
                doctor.chamber_hospital_name ||
                doctor.chamber ||
                doctor.chamber_name ||
                doctor.chamber_hospital ||
                doctor.hospital_name ||
                "Not specified";


            // -------------------------------------------------
            // CITY
            // -------------------------------------------------

            const city =
                doctor.city ||
                doctor.location ||
                doctor.address ||
                "Sylhet";


            // -------------------------------------------------
            // VISITING HOURS
            // -------------------------------------------------

            const visitingHours =
                doctor.visiting_hours ||
                doctor.visiting_hour ||
                doctor.visiting_time ||
                doctor.visitingTime ||
                "Not specified";


            // -------------------------------------------------
            // PHONE
            // -------------------------------------------------

            const phone =
                doctor.appointment_phone ||
                doctor.appointmentPhone ||
                doctor.phone ||
                doctor.contact ||
                doctor.contact_number ||
                doctor.mobile ||
                "Not specified";


            // -------------------------------------------------
            // FEE
            // -------------------------------------------------

            const fee =
                doctor.appointment_fee ??
                doctor.appointmentFee ??
                doctor.fee ??
                doctor.consultation_fee ??
                0;


            // =================================================
            // RENDER
            // =================================================

            profileContainer.innerHTML = `

                <!-- =========================================
                     HERO
                ========================================== -->

                <div class="doctor-hero-card">

                    <div class="doctor-avatar-large">

                        👨‍⚕️

                    </div>


                    <div class="doctor-hero-info">

                        <div class="doctor-specialist-badge">

                            <span>●</span>

                            VERIFIED SPECIALIST

                        </div>


                        <h1 class="doctor-name">

                            ${escapeHTML(
                                doctorName
                            )}

                        </h1>


                        <p class="doctor-specialization">

                            ${escapeHTML(
                                specialization
                            )}

                        </p>


                        <p class="doctor-designation">

                            ${escapeHTML(
                                designation
                            )}

                        </p>

                    </div>

                </div>


                <!-- =========================================
                     MAIN GRID
                ========================================== -->

                <div class="doctor-profile-grid">


                    <!-- =====================================
                         LEFT
                    ====================================== -->

                    <div class="doctor-main-column">


                        <!-- PROFESSIONAL INFORMATION -->

                        <div class="doctor-info-card">


                            <div class="doctor-card-header">

                                <div class="doctor-card-icon">
                                    🎓
                                </div>


                                <div>

                                    <h2>
                                        Professional Information
                                    </h2>

                                    <p>
                                        Doctor's qualifications
                                        and professional details
                                    </p>

                                </div>

                            </div>


                            <div class="doctor-info-list">


                                <div class="doctor-info-row">

                                    <div class="doctor-info-label">

                                        <span class="info-icon">
                                            🎓
                                        </span>

                                        Qualification

                                    </div>


                                    <div class="doctor-info-value">

                                        ${escapeHTML(
                                            qualification
                                        )}

                                    </div>

                                </div>


                                <div class="doctor-info-row">

                                    <div class="doctor-info-label">

                                        <span class="info-icon">
                                            🏥
                                        </span>

                                        Current Workplace

                                    </div>


                                    <div class="doctor-info-value">

                                        ${escapeHTML(
                                            workplace
                                        )}

                                    </div>

                                </div>


                                <div class="doctor-info-row">

                                    <div class="doctor-info-label">

                                        <span class="info-icon">
                                            🏨
                                        </span>

                                        Chamber / Hospital

                                    </div>


                                    <div class="doctor-info-value">

                                        ${escapeHTML(
                                            chamber
                                        )}

                                    </div>

                                </div>


                                <div class="doctor-info-row">

                                    <div class="doctor-info-label">

                                        <span class="info-icon">
                                            📍
                                        </span>

                                        Location

                                    </div>


                                    <div class="doctor-info-value">

                                        ${escapeHTML(
                                            city
                                        )}

                                    </div>

                                </div>


                            </div>


                            <!-- VISITING HOURS -->

                            <div class="visiting-hours-box">

                                <div class="visiting-hours-icon">
                                    🕒
                                </div>


                                <div>

                                    <span>
                                        Visiting Hours
                                    </span>

                                    <strong>

                                        ${escapeHTML(
                                            visitingHours
                                        )}

                                    </strong>

                                </div>

                            </div>


                        </div>


                        <!-- CONTACT INFORMATION -->

                        <div class="doctor-info-card">


                            <div class="doctor-card-header">

                                <div class="doctor-card-icon">
                                    📞
                                </div>


                                <div>

                                    <h2>
                                        Contact Information
                                    </h2>

                                    <p>
                                        Appointment contact details
                                    </p>

                                </div>

                            </div>


                            <div class="doctor-info-list">


                                <div class="doctor-info-row">

                                    <div class="doctor-info-label">

                                        <span class="info-icon">
                                            📞
                                        </span>

                                        Appointment Phone

                                    </div>


                                    <div class="doctor-info-value">

                                        ${escapeHTML(
                                            phone
                                        )}

                                    </div>

                                </div>


                            </div>


                        </div>


                        <!-- NOTE -->

                        <div class="doctor-profile-note">

                            <span>
                                ℹ️
                            </span>


                            <p>

                                Doctor information is provided
                                for informational purposes.
                                Please verify availability
                                and visiting hours before
                                visiting.

                            </p>

                        </div>


                    </div>


                    <!-- =====================================
                         RIGHT SIDEBAR
                    ====================================== -->

                    <div class="doctor-sidebar">


                        <!-- APPOINTMENT INFORMATION -->

                        <div class="appointment-card">


                            <div class="appointment-card-top">

                                <div class="appointment-small-title">

                                    APPOINTMENT INFORMATION

                                </div>


                                <div class="appointment-icon">

                                    📅

                                </div>

                            </div>


                            <h2>

                                Consultation Fee

                            </h2>


                            <p class="appointment-description">

                                Standard appointment fee
                                for consultation with
                                this doctor.

                            </p>


                            <div class="appointment-fee">

                                <span>

                                    Appointment Fee

                                </span>


                                <strong>

                                    Tk.
                                    ${formatFee(fee)}

                                </strong>

                            </div>


                            <div class="appointment-phone">

                                <div class="phone-icon">

                                    📞

                                </div>


                                <div>

                                    <small>

                                        Appointment Phone

                                    </small>


                                    <strong>

                                        ${escapeHTML(
                                            phone
                                        )}

                                    </strong>

                                </div>

                            </div>


                        </div>


                        <!-- QUICK INFORMATION -->

                        <div class="doctor-quick-card">


                            <h3>

                                Quick Information

                            </h3>


                            <div class="quick-item">

                                <span>
                                    🩺
                                </span>


                                <div>

                                    <small>
                                        Specialization
                                    </small>

                                    <strong>

                                        ${escapeHTML(
                                            specialization
                                        )}

                                    </strong>

                                </div>

                            </div>


                            <div class="quick-item">

                                <span>
                                    📍
                                </span>


                                <div>

                                    <small>
                                        Location
                                    </small>

                                    <strong>

                                        ${escapeHTML(
                                            city
                                        )}

                                    </strong>

                                </div>

                            </div>


                            <div class="quick-item">

                                <span>
                                    🕒
                                </span>


                                <div>

                                    <small>
                                        Visiting Hours
                                    </small>

                                    <strong>

                                        ${escapeHTML(
                                            visitingHours
                                        )}

                                    </strong>

                                </div>

                            </div>


                            <div class="quick-item">

                                <span>
                                    🏥
                                </span>


                                <div>

                                    <small>
                                        Hospital
                                    </small>

                                    <strong>

                                        ${escapeHTML(
                                            chamber
                                        )}

                                    </strong>

                                </div>

                            </div>


                        </div>


                    </div>


                </div>

            `;

        }


        // =====================================================
        // FORMAT FEE
        // =====================================================

        function formatFee(
            fee
        ) {

            const number =
                Number(fee);


            if (
                Number.isNaN(number)
            ) {

                return escapeHTML(
                    fee
                );

            }


            return number.toLocaleString(
                "en-BD",
                {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                }
            );

        }


        // =====================================================
        // ESCAPE HTML
        // =====================================================

        function escapeHTML(
            value
        ) {

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
        // ERROR
        // =====================================================

        function showError(
            message
        ) {

            profileContainer.innerHTML = `

                <div class="doctor-profile-error">

                    <div class="doctor-error-icon">

                        ⚠️

                    </div>


                    <h2>

                        Unable to Load Doctor

                    </h2>


                    <p>

                        ${escapeHTML(
                            message
                        )}

                    </p>


                    <a
                        href="/doctors"
                        class="doctor-back-button"
                    >

                        ← Back to Doctors

                    </a>

                </div>

            `;

        }


        // =====================================================
        // INITIAL LOAD
        // =====================================================

        await loadDoctor();

    }
);