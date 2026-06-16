function createSkillChart(matchedCount, missingCount){

    const ctx = document
        .getElementById("skillChart")
        .getContext("2d");

    new Chart(ctx, {
        type: "doughnut",

        data: {

            labels: [
                "Matched Skills",
                "Missing Skills"
            ],

            datasets: [{
                data: [
                    matchedCount,
                    missingCount
                ],

                backgroundColor: [
                    "#22c55e",
                    "#ef4444"
                ]
            }]
        }
    });

}