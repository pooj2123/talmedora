def classify_glucose(fasting, pp):

    fasting_status = "unknown"

    pp_status = "unknown"

    # FASTING
    if fasting is not None:

        if fasting < 100:

            fasting_status = "normal"

        elif 100 <= fasting <= 125:

            fasting_status = "pre-diabetic"

        else:

            fasting_status = "diabetic"

    # POST MEAL
    if pp is not None:

        if pp < 140:

            pp_status = "normal"

        elif 140 <= pp <= 199:

            pp_status = (
                "impaired glucose tolerance"
            )

        else:

            pp_status = "diabetic"

    return {

        "fasting_status":
        fasting_status,

        "pp_status":
        pp_status
    }