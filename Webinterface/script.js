$(document).ready(function () {
    $('#issueForm').on('submit', function (e) {
        e.preventDefault();
        submitForm();
    });

    $('#customerIssue').on('keypress', function (e) {
        if (e.which == 13) {
            e.preventDefault();
            submitForm();
        }
    });

    function submitForm() {
        const issue = $('#customerIssue').val().trim();

        // Validation: check if the input contains at least three words
        const words = issue.split(/\s+/);
        const wordCount = words.length;
        if (wordCount < 3) {
            $('#response').html('<div class="alert alert-danger">Error: Please enter at least three words.</div>').addClass('visible');
            return;
        }

        // Validation: check for nonsensical input using a simple heuristic
        const isGibberish = words.some(word => {
            return /^[a-zA-Z]+$/.test(word) && /([a-zA-Z])\1{2,}/.test(word);
        });
        if (isGibberish) {
            $('#response').html('<div class="alert alert-danger">Error: Please enter a valid sentence without repeated characters.</div>').addClass('visible');
            return;
        }

        $('#buttonContainer').hide();
        $('#loadingSpinner').show();

        $.ajax({
            url: 'https://70guswvc7h.execute-api.eu-north-1.amazonaws.com/default/preprocess',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ text: issue }),
            success: function (response) {
                $('#loadingSpinner').hide();
                $('#buttonContainer').show();

                const result = JSON.parse(response.body);
                const prediction = result.classification_result;
                let message = `<h5>Predicted Service: ${prediction.predicted_service}</h5>
                               <h5>Department: ${prediction.department}</h5>
                               <h6>Confidence:</h6>`;

                for (const [key, value] of Object.entries(prediction.confidence)) {
                    message += `<div class="mb-2">
                                    <span>${key}:</span>
                                    <div class="progress">
                                        <div class="progress-bar" role="progressbar" style="width: ${value * 100}%;" aria-valuenow="${value * 100}" aria-valuemin="0" aria-valuemax="100">${(value * 100).toFixed(2)}%</div>
                                    </div>
                                </div>`;
                }

                $('#response').html(message).addClass('visible');
            },
            error: function (error) {
                $('#loadingSpinner').hide();
                $('#buttonContainer').show();
                $('#response').html('<div class="alert alert-danger">Error: ' + error.responseText + '</div>').addClass('visible');
            }
        });
    }

    $('#cancelButton').on('click', function () {
        $('#customerIssue').val('');
        $('#response').removeClass('visible').html('');
    });
});
